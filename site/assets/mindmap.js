(() => {
  const svg = document.getElementById("mm-svg");
  const crumb = document.getElementById("mm-crumb");
  const search = document.getElementById("mm-search");
  const body = document.getElementById("mm-panel-body");
  const sheetToggle = document.getElementById("mm-sheet-toggle");
  const backBtn = document.getElementById("mm-back");
  const topBtn = document.getElementById("mm-top");
  if (!svg) return;

  const KIND = {
    hub: "field",
    domain: "domain",
    area: "cluster — a subfield",
    concept: "idea",
    method: "algorithm",
    paper: "paper",
    framework: "code",
    lab: "lab",
  };
  const FILL = {
    hub: "#243028",
    domain: "#cfe8d4",
    area: "#dcecc8",
    concept: "#ddd4ee",
    method: "#f3ddb0",
    paper: "#c9dff0",
    framework: "#f1cfc4",
    lab: "#eceae2",
  };
  const STROKE = {
    hub: "#7dcea0",
    domain: "#2d6a45",
    area: "#4a7a3a",
    concept: "#6b4ea0",
    method: "#b57a12",
    paper: "#2a6f97",
    framework: "#a24c38",
    lab: "#606660",
  };
  const R = { hub: 28, domain: 22, area: 18, default: 14 };

  let graph = { nodes: [], edges: [], center: "embodied-ai" };
  let jobs = { openings: [] };
  let entities = { organizations: [], people: [], associations: [], contributions: [] };
  const careerEnabled = new URLSearchParams(window.location.search).get("career") === "1";
  let byId = {};
  let kids = {};
  let focus = null;
  let active = null;
  const view = { x: 0, y: 0, s: 1 };
  let world = null;
  let drag = null;
  let dragged = false;

  function phone() {
    return window.matchMedia("(max-width: 860px)").matches;
  }

  function chromeTop() {
    const heading = document.querySelector(".mm-heading");
    const toolbar = document.querySelector(".mm-toolbar");
    const anchor = heading && heading.offsetParent ? heading : toolbar;
    return (anchor ? anchor.getBoundingClientRect().bottom : 56) + 12;
  }

  function index() {
    byId = Object.fromEntries(graph.nodes.map((n) => [n.id, n]));
    kids = {};
    for (const n of graph.nodes) {
      const p = n.parent;
      if (!p) continue;
      (kids[p] ||= []).push(n);
    }
  }

  function pathTo(id) {
    const out = [];
    let cur = byId[id];
    const seen = new Set();
    while (cur && !seen.has(cur.id)) {
      seen.add(cur.id);
      out.unshift(cur);
      cur = cur.parent ? byId[cur.parent] : null;
    }
    return out;
  }

  function neighbors(id) {
    const s = new Set();
    for (const e of graph.edges) {
      if (e.from === id) s.add(e.to);
      if (e.to === id) s.add(e.from);
    }
    return [...s].map((i) => byId[i]).filter(Boolean);
  }

  function relatedEdges(id) {
    const pairs = new Map();
    for (const edge of graph.edges) {
      if (edge.from !== id && edge.to !== id) continue;
      const from = byId[edge.from], to = byId[edge.to];
      if (!from || !to || from.parent === to.id || to.parent === from.id || ["contains", "includes"].includes(edge.rel)) continue;
      const other = edge.from === id ? edge.to : edge.from;
      if (!pairs.has(other)) pairs.set(other, { other, claims: [] });
      pairs.get(other).claims.push(`${from.label} → ${edge.rel.replaceAll("-", " ")} → ${to.label}`);
    }
    return [...pairs.values()];
  }

  function ytEmbed(url) {
    const u = String(url);
    const vid = u.match(/(?:v=|youtu\.be\/|embed\/)([A-Za-z0-9_-]{11})/);
    const pl = u.match(/[?&]list=([A-Za-z0-9_-]+)/);
    if (pl && !vid) return `videoseries?list=${pl[1]}`;
    if (vid) return vid[1];
    return null;
  }

  // Public facts only. Career state is never fetched by this page.
  function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>"']/g, (c) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
    }[c]));
  }

  function httpsUrl(value) {
    try {
      const url = new URL(value);
      return url.protocol === "https:" && !url.username && !url.password ? url.href : null;
    } catch { return null; }
  }

  function publicLink(url, label) {
    const safe = httpsUrl(url);
    return safe ? `<a href="${escapeHtml(safe)}" target="_blank" rel="noopener noreferrer">${escapeHtml(label)}</a>` : escapeHtml(label);
  }

  function evidence(record) {
    return `<small class="mm-evidence">${(record.sources || []).map((s) => publicLink(s.url, s.title)).join(" · ")} · verified ${escapeHtml(record.verified_on)}</small>`;
  }

  function mapLink(id) {
    const node = byId[id];
    return node ? `<a href="#node=${escapeHtml(encodeURIComponent(id))}" data-go="${escapeHtml(id)}">${escapeHtml(node.label)}</a>` : escapeHtml(id);
  }

  function normalizeEntities(data) {
    const result = {};
    for (const key of ["organizations", "people", "associations", "contributions"]) {
      result[key] = Array.isArray(data?.[key]) ? data[key].filter((x) => x && typeof x === "object") : [];
    }
    return result;
  }

  function personCard(person, claims, organization, member = false) {
    const initials = person.name.split(/\s+/).map(s => s[0]).slice(0, 2).join("");
    const linkedin = httpsUrl(person.linkedin_url);
    const sources = [person, ...claims];
    const liIcon = '<svg viewBox="0 0 24 24" width="15" height="15" aria-hidden="true"><path fill="currentColor" d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45zM22.23 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.46c.98 0 1.77-.77 1.77-1.73V1.73C24 .77 23.21 0 22.23 0z"/></svg>';
    return `<article class="mm-person-card">
      <header><span class="mm-avatar" aria-hidden="true">${escapeHtml(initials)}</span><div><span class="mm-person-kind">${member ? "Organization member" : "Contributor"}</span><h4>${escapeHtml(person.name)}</h4>${organization ? `<span class="mm-person-org">${publicLink(organization.url, organization.name)}</span>` : ""}</div></header>
      <p class="mm-person-role">${escapeHtml(person.role)}</p>
      <div class="mm-person-work"><strong>Connection to this work</strong><p>${member ? "Affiliation verified; individual authorship of this work is not established." : claims.map(c => escapeHtml(c.relationship)).join("<br>")}</p></div>
      <div class="mm-person-actions">${linkedin ? `<a class="mm-linkedin" href="${escapeHtml(linkedin)}" target="_blank" rel="noopener noreferrer">${liIcon} LinkedIn</a>` : '<span class="mm-profile-missing">LinkedIn not verified</span>'}${publicLink(person.profile_url, "Research profile")}</div>
      <details class="mm-provenance"><summary>Sources & verification · ${escapeHtml(person.verified_on)}</summary>${sources.map(evidence).join("")}</details>
    </article>`;
  }

  function entityPanel(node) {
    const orgs = new Map(entities.organizations.map((o) => [o.id, o]));
    const people = new Map(entities.people.map((p) => [p.id, p]));
    const sourced = (r) => Array.isArray(r.sources) && r.sources.some((s) => httpsUrl(s.url)) && r.verified_on;
    const direct = entities.associations.filter((a) => a.node_id === node.id && !a.via_node_id && orgs.has(a.organization_id) && sourced(a));
    const labOrgs = entities.organizations.filter((o) => node.kind === "lab" && o.map_node_id === node.id);
    const directIds = new Set([...direct.map((a) => a.organization_id), ...labOrgs.map((o) => o.id)]);
    const orgTitle = (o) => `${publicLink(o.url, o.name)} <small>${escapeHtml(o.kind)}</small>${o.map_node_id && o.map_node_id !== node.id ? ` · ${mapLink(o.map_node_id)}` : ""}`;
    const neighborIds = new Set(neighbors(node.id).map((n) => n.id));
    const related = new Map();
    for (const a of entities.associations) {
      const via = a.node_id === node.id ? a.via_node_id : a.node_id;
      if (!via || !neighborIds.has(via) || !orgs.has(a.organization_id) || directIds.has(a.organization_id) || !sourced(a)) continue;
      // Never walk beyond one explicit graph edge, nor relay an indirect claim.
      if (a.node_id !== node.id && a.via_node_id) continue;
      if (!related.has(a.organization_id) && related.size < 4) related.set(a.organization_id, []);
      const paths = related.get(a.organization_id);
      if (paths && !paths.some((p) => p.via === via) && paths.length < 3) paths.push({ via, association: a });
    }
    const orgRows = [...directIds].map((id) => {
      const claims = direct.filter((a) => a.organization_id === id);
      return `<li>${orgTitle(orgs.get(id))}${claims.map((a) => `<div>${escapeHtml(a.relationship)}</div>${evidence(a)}`).join("")}${!claims.length ? '<div>Organization represented by this lab node; official website linked above.</div>' : ""}</li>`;
    }).join("");
    const contributions = entities.contributions.filter((c) => c.node_id === node.id && people.has(c.person_id) && sourced(people.get(c.person_id)) && sourced(c));
    const contributorIds = [...new Set(contributions.map((c) => c.person_id))];
    const memberRows = entities.people.filter((p) => directIds.has(p.organization_id) && !contributorIds.includes(p.id) && sourced(p)).slice(0, 6);
    return `<section class="mm-entities" aria-label="Organizations and contributors">
      <h3>Organizations & contributors</h3>
      ${orgRows ? `<ul class="mm-res">${orgRows}</ul>` : '<p class="mm-empty">No verified organization link yet</p>'}
      ${related.size ? `<h4>Related-work examples — not developers of this node</h4><ul class="mm-res">${[...related].map(([id, paths]) => `<li>${orgTitle(orgs.get(id))}${paths.map(({ via, association: a }) => `<div>Via ${mapLink(via)}: ${escapeHtml(a.relationship)}</div>${evidence(a)}`).join("")}</li>`).join("")}</ul>` : ""}
      ${contributorIds.length ? `<h4>People behind the work</h4><div class="mm-people">${contributorIds.map(id => personCard(people.get(id), contributions.filter(c => c.person_id === id), orgs.get(people.get(id).organization_id))).join("")}</div>` : '<p class="mm-empty">Individual contributors not verified yet.</p>'}
      ${memberRows.length ? `<details class="mm-members"><summary>More from the organization · ${memberRows.length}</summary><div class="mm-people">${memberRows.map(p => personCard(p, [], orgs.get(p.organization_id), true)).join("")}</div></details>` : ""}
      ${careerEnabled ? `<p><a class="mm-private-link" href="http://127.0.0.1:8767/#node=${escapeHtml(encodeURIComponent(node.id))}" target="_blank" rel="noopener noreferrer">Open local/private career companion ↗</a><small class="mm-evidence">Local service required; no private data is loaded here.</small></p>` : ""}
    </section>`;
  }

  function nodeFromHash() {
    return new URLSearchParams(window.location.hash.slice(1)).get("node");
  }

  function updateNodeUrl(id) {
    const hash = `#node=${encodeURIComponent(id)}`;
    if (window.location.hash !== hash) window.history.replaceState(null, "", hash);
  }

  function selectLinkedNode() {
    const id = nodeFromHash();
    if (!id || !byId[id]) return false;
    const node = byId[id];
    setFocus((kids[id] || []).length ? id : (node.parent || id), false);
    openPanel(id);
    draw();
    camera();
    return true;
  }

  function jobsFor(node) {
    if (!node.company_id && node.kind !== "lab") return [];
    const name = (node.label || "").toLowerCase();
    const aliases = {
      "figure-ai": "figure",
      apptronik: "apptronik",
      agility: "agility",
      "physical-intelligence": "physical",
      "generalist-ai": "generalist",
      "skild-ai": "skild",
      "tesla-optimus": "tesla",
      "boston-dynamics": "boston",
      "1x": "1x",
    };
    const key = aliases[node.company_id] || name.split(" ")[0];
    return (jobs.openings || []).filter((o) => (o.company || "").toLowerCase().includes(key));
  }

  function applyView(arrange = true) {
    if (!world) return;
    world.setAttribute("transform", `translate(${view.x} ${view.y}) scale(${view.s})`);
    world.querySelectorAll('.mm-node:not(.ghost) text').forEach(t => {
      t.style.fontSize = `${Math.max(16, (phone() ? 13.5 : 13) / view.s)}px`;
      t.style.strokeWidth = `${4 / view.s}px`;
    });
    world.querySelectorAll('.mm-hit').forEach(hit => hit.setAttribute('r', Math.max(24, 22 / view.s)));
    if (arrange) arrangeLabels();
  }

  function arrangeLabels() {
    // Labels may move; the graph seats and parent topology never do.
    const labels = [...world.querySelectorAll('.mm-node:not(.ghost) text')];
    labels.forEach(t => t.removeAttribute('transform'));
    world.querySelectorAll('.mm-label-leader').forEach(line => line.remove());
    const placed = [], rect = svg.getBoundingClientRect();
    const top = chromeTop();
    labels.sort((a, b) => a.getBoundingClientRect().top - b.getBoundingClientRect().top);
    for (const t of labels) {
      const b = t.getBoundingClientRect();
      let dx = Math.max(rect.left + 12 - b.left, Math.min(0, rect.right - 12 - b.right)), dy = 0;
      for (let i = 0; i < 40; i++) {
        const offset = i ? Math.ceil(i / 2) * 15 * (i % 2 ? 1 : -1) : 0;
        const candidate = { left: b.left + dx, right: b.right + dx, top: b.top + offset, bottom: b.bottom + offset };
        if (candidate.top < top || candidate.bottom > rect.bottom - 72) continue;
        if (placed.some(p => candidate.left < p.right + 6 && candidate.right > p.left - 6 && candidate.top < p.bottom + 5 && candidate.bottom > p.top - 5)) continue;
        dy = offset; break;
      }
      t.setAttribute('transform', `translate(${dx / view.s} ${dy / view.s})`);
      placed.push({ left: b.left + dx, right: b.right + dx, top: b.top + dy, bottom: b.bottom + dy });
      if (Math.abs(dy) > 5 || Math.abs(dx) > 5) {
        const line = el('line', { class: 'mm-label-leader', x1: 0, y1: 0, x2: dx / view.s, y2: (Number(t.getAttribute('y')) + dy / view.s), stroke: '#b3ac9a', 'stroke-width': .7 / view.s, 'pointer-events': 'none' });
        t.parentNode.insertBefore(line, t);
      }
    }
  }

  let home = new Map();

  function layoutHome() {
    // Stable world coordinates: resizing changes the camera, not the topology.
    const cx = 650, cy = 650;
    const ring = [0, 205, 370, 555, 720];
    const weight = (id) => Math.max(2, (kids[id] || []).reduce((sum, child) => sum + weight(child.id), 0));
    home = new Map();
    const hubId = graph.center || "embodied-ai";

    function walk(id, angle, sweep, depth) {
      const n = byId[id];
      if (!n) return;
      const rad = ring[Math.min(depth, ring.length - 1)];
      home.set(id, {
        x: cx + Math.cos(angle) * rad,
        y: cy + Math.sin(angle) * rad,
        r: R[n.kind] || R.default,
        a: angle,
      });
      const ch = kids[id] || [];
      if (!ch.length) return;
      if (depth === 0) {
        ch.forEach((c, i) => {
          const a = -Math.PI / 2 + (i * 2 * Math.PI) / ch.length;
          walk(c.id, a, (2 * Math.PI) / ch.length, 1);
        });
        return;
      }
      const inner = sweep * 0.94;
      const total = ch.reduce((sum, child) => sum + weight(child.id), 0);
      let start = angle - inner / 2;
      ch.forEach((c, i) => {
        const share = inner * weight(c.id) / total;
        walk(c.id, start + share / 2, share, depth + 1);
        if (!(kids[c.id] || []).length) {
          const p = home.get(c.id);
          const radius = ring[Math.min(depth + 1, ring.length - 1)] + (i % 3) * 55;
          p.x = cx + Math.cos(p.a) * radius;
          p.y = cy + Math.sin(p.a) * radius;
        }
        start += share;
      });
    }
    walk(hubId, 0, Math.PI * 2, 0);
    home.set(hubId, { x: cx, y: cy, r: R.hub, a: 0 });
  }

  function fitHome() {
    if (!home.size) return;
    let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    for (const p of home.values()) {
      x0 = Math.min(x0, p.x - 36);
      y0 = Math.min(y0, p.y - 36);
      x1 = Math.max(x1, p.x + 36);
      y1 = Math.max(y1, p.y + 44);
    }
    const W = svg.clientWidth || 900;
    const H = svg.clientHeight || 640;
    const s = Math.min(W / Math.max(x1 - x0, 1), H / Math.max(y1 - y0, 1)) * 0.9;
    view.s = Math.min(1.35, Math.max(0.25, s));
    view.x = W / 2 - ((x0 + x1) / 2) * view.s;
    view.y = H / 2 - ((y0 + y1) / 2) * view.s;
    applyView();
  }

  function seats() {
    const map = new Map(home);
    const origin = home.get(focus);
    const ch = kids[focus] || [];
    // Keep hub/domain seats fixed. Only unpack the last layer of a cluster.
    if (!origin || ch.length < 2 || ch.some(c => (kids[c.id] || []).length)) return map;
    const n = ch.length;
    const rad = Math.max(210, (n * 125) / (2 * Math.PI));
    const base = origin.a ?? 0;
    ch.forEach((c, i) => {
      const a = base + (i + 0.5) * 2 * Math.PI / n;
      map.set(c.id, {
        x: origin.x + Math.cos(a) * rad,
        y: origin.y + Math.sin(a) * rad,
        r: R[c.kind] || R.default,
        a,
      });
    });
    return map;
  }

  function fitIds(map, ids) {
    let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    for (const id of ids) {
      const p = map.get(id);
      if (!p) continue;
      x0 = Math.min(x0, p.x - 56);
      y0 = Math.min(y0, p.y - 56);
      x1 = Math.max(x1, p.x + 56);
      y1 = Math.max(y1, p.y + 64);
    }
    if (!Number.isFinite(x0)) return;
    const W = svg.clientWidth || 900;
    const H = svg.clientHeight || 640;
    const s = Math.min(W / Math.max(x1 - x0, 1), H / Math.max(y1 - y0, 1)) * 0.82;
    view.s = Math.min(1.8, Math.max(0.35, s));
    view.x = W / 2 - ((x0 + x1) / 2) * view.s;
    view.y = H / 2 - ((y0 + y1) / 2) * view.s;
    applyView();
  }

  function camera() {
    if (!world) return;
    // Fit actual labels, not just circles; reserve space for the editorial chrome.
    const rect = svg.getBoundingClientRect();
    const top = chromeTop() - rect.top;
    const W = Math.max(100, rect.width - 36);
    const H = Math.max(120, rect.height - top - (phone() ? 68 : 84));
    view.s = 1;
    world.querySelectorAll('.mm-node text').forEach(t => t.removeAttribute('transform'));
    world.querySelectorAll('.mm-label-leader').forEach(line => line.remove());
    for (let i = 0; i < 8; i++) {
      applyView(false);
      let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
      let nodes = phone()
        ? world.querySelectorAll('.mm-node:not(.ghost):not(.related)')
        : world.querySelectorAll('.mm-node:not(.ghost)');
      if (!nodes.length) nodes = world.querySelectorAll('.mm-node:not(.ghost)');
      nodes.forEach(node => {
        const b = node.getBBox(), m = node.transform.baseVal.getItem(0).matrix;
        x0 = Math.min(x0, b.x + m.e); y0 = Math.min(y0, b.y + m.f);
        x1 = Math.max(x1, b.x + b.width + m.e); y1 = Math.max(y1, b.y + b.height + m.f);
      });
      if (!Number.isFinite(x0)) return;
      view.s = Math.min(1, W / (x1 - x0), H / (y1 - y0));
      view.x = rect.width / 2 - (x0 + x1) / 2 * view.s;
      view.y = top + H / 2 - (y0 + y1) / 2 * view.s;
    }
    applyView();
  }

  function el(name, attrs) {
    const n = document.createElementNS("http://www.w3.org/2000/svg", name);
    for (const [k, v] of Object.entries(attrs || {})) n.setAttribute(k, v);
    return n;
  }

  function draw() {
    const seat = seats();
    world = el("g");
    applyView();
    const open = new Set();
    pathTo(focus).forEach((n) => open.add(n.id));
    (kids[focus] || []).forEach((n) => open.add(n.id));
    if (active) open.add(active);
    const cross = relatedEdges(active || focus);
    const related = new Set(cross.map(e => e.other));

    for (const n of graph.nodes) {
      const p = n.parent;
      if (!p || !seat.has(n.id) || !seat.has(p)) continue;
      const a = seat.get(p);
      const b = seat.get(n.id);
      const live = open.has(n.id) && open.has(p);
      world.appendChild(el("path", {
        class: "mm-edge" + (live ? (n.id === active ? " on" : " spine") : " ghost"),
        d: `M ${a.x} ${a.y} L ${b.x} ${b.y}`,
      }));
    }

    // Reveal semantic connections only around the selected node, not all at once.
    for (const edge of cross) {
      const a = seat.get(active || focus), b = seat.get(edge.other);
      if (!a || !b) continue;
      const dx = b.x - a.x, dy = b.y - a.y;
      const path = el("path", {
        class: "mm-edge cross",
        d: `M ${a.x} ${a.y} Q ${(a.x + b.x) / 2 - dy * 0.12} ${(a.y + b.y) / 2 + dx * 0.12} ${b.x} ${b.y}`,
      });
      const title = el("title");
      title.textContent = edge.claims.join("\n");
      path.appendChild(title);
      path.dataset.from = active || focus;
      path.dataset.to = edge.other;
      world.appendChild(path);
    }

    const drawNode = (n) => {
      const p = seat.get(n.id);
      if (!p) return;
      const ghost = !open.has(n.id) && !related.has(n.id);
      const g = el("g", {
        class: `mm-node ${n.kind}${n.id === active || n.id === focus ? " active" : ""}${ghost ? " ghost" : ""}`,
        transform: `translate(${p.x} ${p.y})`,
      });
      g.dataset.id = n.id;
      if (related.has(n.id) && !open.has(n.id)) g.classList.add("related");
      const title = el("title");
      title.textContent = [n.label, ...cross.filter(e => e.other === n.id).flatMap(e => e.claims)].join("\n");
      g.appendChild(title);
      if (!ghost) {
        g.appendChild(el('circle', { class: 'mm-hit', r: 24, fill: 'transparent', stroke: 'none' }));
        g.setAttribute("role", "button");
        g.setAttribute("tabindex", "0");
        g.setAttribute("aria-label", n.label);
        g.addEventListener("keydown", e => {
          if (e.key === "Enter" || e.key === " ") { e.preventDefault(); onOrb(n.id); }
        });
      }
      if (n.id === focus) {
        g.appendChild(el("circle", {
          r: p.r + 6,
          fill: "none",
          stroke: "#243028",
          "stroke-width": 1.25,
        }));
      }
      g.appendChild(el("circle", {
        r: ghost ? Math.max(8, p.r - 4) : p.r,
        fill: ghost ? "none" : (FILL[n.kind] || FILL.lab),
        stroke: ghost ? "#b5b0a6" : (STROKE[n.kind] || STROKE.lab),
        "stroke-width": ghost ? 1.1 : n.id === focus ? 2.2 : 1.6,
        "stroke-dasharray": ghost ? "3 3" : "",
      }));
      const labelDeepGhost = ghost && (n.layer || 0) >= 3;
      if (!labelDeepGhost) {
        const t = el("text", { y: (ghost ? Math.max(8, p.r - 4) : p.r) + 15 });
        const words = n.label.split(' '), lines = [''];
        words.forEach(word => {
          if ((lines[lines.length - 1] + ' ' + word).trim().length > 22 && lines[lines.length - 1]) lines.push('');
          lines[lines.length - 1] = (lines[lines.length - 1] + ' ' + word).trim();
        });
        lines.forEach((line, i) => {
          const span = el('tspan', { x: 0, dy: i ? '1.15em' : 0 });
          span.textContent = line; t.appendChild(span);
        });
        g.appendChild(t);
      }
      if (!ghost) {
        g.addEventListener("click", (ev) => {
          ev.stopPropagation();
          if (dragged) return;
          onOrb(n.id);
        });
      }
      world.appendChild(g);
    };

    for (const n of graph.nodes) {
      if (!open.has(n.id) && !related.has(n.id)) drawNode(n);
    }
    for (const n of graph.nodes) {
      if (open.has(n.id) || related.has(n.id)) drawNode(n);
    }

    svg.replaceChildren(world);
    renderCrumb();
  }

  function renderCrumb() {
    const path = pathTo(focus);
    crumb.innerHTML = "";
    path.forEach((n, i) => {
      if (i) {
        const s = document.createElement("span");
        s.textContent = "/";
        crumb.appendChild(s);
      }
      const b = document.createElement("button");
      b.type = "button";
      b.textContent = n.label;
      b.addEventListener("click", () => setFocus(n.id, false));
      crumb.appendChild(b);
    });
    const title = document.getElementById("mm-title");
    if (title) title.textContent = byId[focus]?.label || "";
  }

  function openPanel(id) {
    const n = byId[id];
    if (!n) return;
    active = id;
    updateNodeUrl(id);
    const res = n.resources || [];
    const vids = res.filter((r) => r.type === "video" || /youtu/.test(r.url || ""));
    const rest = res.filter((r) => !vids.includes(r));
    const firstYt = vids.map((v) => ytEmbed(v.url)).find(Boolean);
    const dirs = n.research_directions || [];
    const childList = kids[id] || [];
    const relatedJobs = jobsFor(n);
    const intern = relatedJobs.filter((j) => j.seniority === "internship");
    document.getElementById('mm-sheet-label').textContent = n.label;
    const canUp = !!(n.parent && byId[n.parent]);
    body.innerHTML = `
      ${canUp ? `<p><button type="button" class="mm-navbtn" id="mm-panel-back">← Back</button></p>` : ""}
      <div class="mm-kicker">${KIND[n.kind] || n.kind} · layer ${n.layer ?? "—"}</div>
      <h2>${n.label}</h2>
      <p>${n.brief || ""}</p>
      ${entityPanel(n)}
      ${firstYt ? `<h3>Watch</h3><div class="mm-yt"><iframe src="https://www.youtube-nocookie.com/embed/${firstYt}" title="Lecture" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe></div>` : ""}
      ${n.why ? `<h3>Why it is on the map</h3><p>${n.why}</p>` : ""}
      ${childList.length ? `<h3>Inside this layer</h3><ul class="mm-res">${childList.map((x) => `<li><a href="#" data-go="${x.id}">${x.label}</a> <small>${x.kind}</small></li>`).join("")}</ul>` : ""}
      <h3>Cross-connections · ${relatedEdges(id).length}</h3>
      <ul class="mm-res mm-relations">${relatedEdges(id).map(e => `<li>${mapLink(e.other)}<small>${e.claims.map(escapeHtml).join("<br>")}</small></li>`).join("") || "<li class='mm-empty'>No extra links</li>"}</ul>
      <h3>Resources</h3>
      <ul class="mm-res">${[...vids, ...rest].map((r) => `<li><a href="${r.url}">${r.title}</a></li>`).join("") || "<li class='mm-empty'>None yet</li>"}</ul>
      ${dirs.length ? `<h3>Research directions</h3><ul class="mm-res">${dirs.map((d) => `<li>${d}</li>`).join("")}</ul>` : ""}
      <h3>Jobs & internships</h3>
      ${
        relatedJobs.length
          ? `<ul class="mm-jobs">${relatedJobs.slice(0, 12).map((j) => `<li><a href="${j.url}">${j.title}</a><small>${j.company} · ${j.location || ""} · ${j.seniority}</small></li>`).join("")}${intern.length ? `<li class="mm-empty">${intern.length} internship(s).</li>` : ""}</ul>`
          : `<p class="mm-empty">${n.kind === "lab" ? "No tracked official openings in the last jobs scrape." : "Jobs attach to lab nodes."}</p>`
      }
    `;
    body.querySelectorAll("[data-go]").forEach((a) => {
      a.addEventListener("click", (e) => {
        e.preventDefault();
        onOrb(a.dataset.go);
      });
    });
    const pb = document.getElementById("mm-panel-back");
    if (pb) pb.addEventListener("click", goBack);
    body.scrollTop = 0;
  }

  function syncNav() {
    const f = byId[focus];
    const up = !!(f && f.parent && byId[f.parent]);
    if (backBtn) backBtn.disabled = !up;
    if (topBtn) topBtn.disabled = !f || f.id === graph.center;
  }

  function goBack() {
    const f = byId[focus];
    if (f?.parent && byId[f.parent]) setFocus(f.parent);
  }

  function goTop() {
    setFocus(graph.center || "embodied-ai");
  }

  function setFocus(id, open = true) {
    if (!byId[id]) return;
    focus = id;
    active = id;
    updateNodeUrl(id);
    if (open) openPanel(id);
    draw();
    camera();
    syncNav();
  }

  function onOrb(id) {
    const n = byId[id];
    if (!n) return;
    if (id === focus) {
      setFocus(id);
      return;
    }
    if (id === n.parent || (byId[focus] && id === byId[focus].parent)) {
      setFocus(id);
      return;
    }
    if ((kids[id] || []).length) setFocus(id);
    else {
      if (focus !== n.parent && byId[n.parent]) focus = n.parent;
      active = id;
      openPanel(id);
      draw();
      camera();
      syncNav();
    }
  }

  const pointers = new Map();
  let pinch = null;
  const gesture = () => {
    const [a, b] = [...pointers.values()];
    return b ? { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2, d: Math.hypot(b.x - a.x, b.y - a.y) } : a;
  };
  function zoomAt(scale, x, y) {
    const next = Math.min(3, Math.max(.08, scale));
    view.x = x - (x - view.x) * next / view.s;
    view.y = y - (y - view.y) * next / view.s;
    view.s = next; applyView();
  }
  svg.addEventListener('pointerdown', e => {
    if (e.button !== 0) return;
    const rect = svg.getBoundingClientRect();
    pointers.set(e.pointerId, { x: e.clientX - rect.left, y: e.clientY - rect.top });
    if (pointers.size === 1) {
      dragged = false;
      drag = { ...gesture(), vx: view.x, vy: view.y, node: e.target.closest('.mm-node') };
    } else { pinch = gesture(); dragged = true; }
    // Capture on the original target so a stationary node tap retains its click target.
    e.target.setPointerCapture(e.pointerId);
  });
  svg.addEventListener('pointermove', e => {
    if (!pointers.has(e.pointerId)) return;
    const rect = svg.getBoundingClientRect();
    pointers.set(e.pointerId, { x: e.clientX - rect.left, y: e.clientY - rect.top });
    const g = gesture();
    if (pointers.size > 1 && pinch) {
      zoomAt(view.s * g.d / Math.max(1, pinch.d), pinch.x, pinch.y);
      view.x += g.x - pinch.x; view.y += g.y - pinch.y;
      pinch = g; dragged = true;
    } else if (drag) {
      if (Math.hypot(g.x - drag.x, g.y - drag.y) > 6) dragged = true;
      if (dragged) { view.x = drag.vx + g.x - drag.x; view.y = drag.vy + g.y - drag.y; }
    }
    applyView();
  });
  function endPointer(e) {
    if (!pointers.has(e.pointerId)) return;
    pointers.delete(e.pointerId);
    if (!pointers.size && drag && !dragged && !drag.node && e.type === 'pointerup') goBack();
    pinch = null;
    drag = pointers.size ? { ...gesture(), vx: view.x, vy: view.y } : null;
  }
  ['pointerup', 'pointercancel', 'lostpointercapture'].forEach(type => svg.addEventListener(type, endPointer));
  svg.addEventListener("wheel", (e) => {
    e.preventDefault();
    const next = view.s * (e.deltaY > 0 ? 0.92 : 1.08);
    const rect = svg.getBoundingClientRect();
    const px = e.clientX - rect.left;
    const py = e.clientY - rect.top;
    zoomAt(next, px, py);
  }, { passive: false });

  if (sheetToggle) {
    let ignoreClick = false;
    const onSheet = (e) => {
      e.stopPropagation();
      const open = document.body.classList.toggle("mm-sheet-open");
      sheetToggle.setAttribute("aria-expanded", String(open));
      const action = sheetToggle.querySelector(".mm-sheet-action");
      if (action) action.textContent = open ? "Close ↓" : "Details ↑";
      requestAnimationFrame(() => camera());
    };
    sheetToggle.addEventListener("click", (e) => {
      if (ignoreClick) { e.preventDefault(); return; }
      onSheet(e);
    });
    sheetToggle.addEventListener("touchend", (e) => {
      e.preventDefault();
      ignoreClick = true;
      onSheet(e);
      setTimeout(() => { ignoreClick = false; }, 80);
    }, { passive: false });
  }
  document.getElementById('mm-fit').addEventListener('click', camera);
  for (const [id, factor] of [['mm-zoom-in', 1.25], ['mm-zoom-out', .8]]) {
    document.getElementById(id).addEventListener('click', () => zoomAt(view.s * factor, svg.clientWidth / 2, svg.clientHeight / 2));
  }
  if (backBtn) backBtn.addEventListener("click", goBack);
  if (topBtn) topBtn.addEventListener("click", goTop);
  window.addEventListener("keydown", (e) => {
    if (e.key === "Escape" || e.key === "Backspace") {
      if (e.target === search) return;
      e.preventDefault();
      goBack();
    }
    if (e.key === "Home" && e.target !== search) goTop();
  });

  let searchT = 0;
  search.addEventListener("input", () => {
    clearTimeout(searchT);
    searchT = setTimeout(() => {
      const q = (search.value || "").trim().toLowerCase();
      if (!q) return;
      const hit = graph.nodes.find((n) => n.label.toLowerCase().includes(q) || n.id.includes(q));
      if (!hit) return;
      onOrb(hit.id);
    }, 160);
  });

  window.addEventListener("resize", () => {
    layoutHome();
    draw();
    camera();
  });

  window.addEventListener("hashchange", selectLinkedNode);

  Promise.all([
    fetch("data/mindmap.json?v=entities1").then((r) => r.json()),
    fetch("data/jobs.json?v=entities1").then((r) => r.json()).catch(() => ({ openings: [] })),
    fetch("data/entities.json?v=entities1").then((r) => {
      if (!r.ok) throw new Error("Entities unavailable");
      return r.json();
    }).catch(() => null),
  ]).then(([g, j, e]) => {
    graph = g;
    jobs = j;
    entities = normalizeEntities(e);
    index();
    const start = () => {
      if (svg.clientWidth < 40) {
        requestAnimationFrame(start);
        return;
      }
      layoutHome();
      fitHome();
      if (!selectLinkedNode()) {
        setFocus(g.center || "embodied-ai");
        document.body.classList.remove("mm-sheet-open");
      }
    };
    start();
    document.fonts.ready.then(camera);
  }).catch((err) => {
    body.innerHTML = `<p>Failed to load mind map: ${escapeHtml(err)}</p>`;
  });
})();
