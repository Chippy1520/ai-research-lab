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

  function ytId(url) {
    const m = String(url).match(/(?:v=|youtu\.be\/)([A-Za-z0-9_-]{11})/);
    return m ? m[1] : null;
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

  function applyView() {
    if (world) world.setAttribute("transform", `translate(${view.x} ${view.y}) scale(${view.s})`);
  }

  let home = new Map();

  function layoutHome() {
    const W = Math.max(svg.clientWidth, 320);
    const H = Math.max(svg.clientHeight, 320);
    const cx = W / 2;
    const cy = H / 2;
    const S = Math.min(W, H);
    const ring = [0, S * 0.2, S * 0.35, S * 0.5, S * 0.6];
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
      const inner = sweep * 0.82;
      ch.forEach((c, i) => {
        const a = ch.length === 1 ? angle : angle - inner / 2 + (i * inner) / Math.max(ch.length - 1, 1);
        walk(c.id, a, inner / Math.max(ch.length, 1), depth + 1);
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

  function isOpen(id) {
    if (id === focus) return true;
    if (byId[id]?.parent === focus) return true;
    return pathTo(focus).some((n) => n.id === id);
  }

  function el(name, attrs) {
    const n = document.createElementNS("http://www.w3.org/2000/svg", name);
    for (const [k, v] of Object.entries(attrs || {})) n.setAttribute(k, v);
    return n;
  }

  function draw() {
    world = el("g");
    applyView();
    const open = new Set();
    pathTo(focus).forEach((n) => open.add(n.id));
    (kids[focus] || []).forEach((n) => open.add(n.id));

    for (const n of graph.nodes) {
      const p = n.parent;
      if (!p || !home.has(n.id) || !home.has(p)) continue;
      const a = home.get(p);
      const b = home.get(n.id);
      const live = open.has(n.id) && open.has(p);
      world.appendChild(el("path", {
        class: "mm-edge" + (live ? (n.id === active ? " on" : " spine") : " ghost"),
        d: `M ${a.x} ${a.y} L ${b.x} ${b.y}`,
      }));
    }

    const drawNode = (n) => {
      const p = home.get(n.id);
      if (!p) return;
      const ghost = !open.has(n.id);
      const g = el("g", {
        class: `mm-node ${n.kind}${n.id === active || n.id === focus ? " active" : ""}${ghost ? " ghost" : ""}`,
        transform: `translate(${p.x} ${p.y})`,
      });
      g.dataset.id = n.id;
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
        t.textContent = n.label;
        g.appendChild(t);
      }
      if (!ghost) {
        g.addEventListener("click", (ev) => {
          ev.stopPropagation();
          onOrb(n.id);
        });
      }
      world.appendChild(g);
    };

    for (const n of graph.nodes) {
      if (!open.has(n.id)) drawNode(n);
    }
    for (const n of graph.nodes) {
      if (open.has(n.id)) drawNode(n);
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
    const res = n.resources || [];
    const vids = res.filter((r) => r.type === "video" || /youtu/.test(r.url || ""));
    const rest = res.filter((r) => !vids.includes(r));
    const firstYt = vids.map((v) => ytId(v.url)).find(Boolean);
    const dirs = n.research_directions || [];
    const nb = neighbors(id).filter((x) => x.id !== n.parent && x.parent !== n.id);
    const childList = kids[id] || [];
    const relatedJobs = jobsFor(n);
    const intern = relatedJobs.filter((j) => j.seniority === "internship");
    document.body.classList.add("mm-sheet-open");
    const canUp = !!(n.parent && byId[n.parent]);
    body.innerHTML = `
      ${canUp ? `<p><button type="button" class="mm-navbtn" id="mm-panel-back">← Back</button></p>` : ""}
      <div class="mm-kicker">${KIND[n.kind] || n.kind} · layer ${n.layer ?? "—"}</div>
      <h2>${n.label}</h2>
      <p>${n.brief || ""}</p>
      ${firstYt ? `<h3>Watch</h3><div class="mm-yt"><iframe src="https://www.youtube-nocookie.com/embed/${firstYt}" title="Lecture" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe></div>` : ""}
      ${n.why ? `<h3>Why it is on the map</h3><p>${n.why}</p>` : ""}
      ${childList.length ? `<h3>Inside this layer</h3><ul class="mm-res">${childList.map((x) => `<li><a href="#" data-go="${x.id}">${x.label}</a> <small>${x.kind}</small></li>`).join("")}</ul>` : ""}
      <h3>Linked</h3>
      <ul class="mm-res">${nb.map((x) => `<li><a href="#" data-go="${x.id}">${x.label}</a> <small>${x.kind}</small></li>`).join("") || "<li class='mm-empty'>No extra links</li>"}</ul>
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
    draw();
    syncNav();
    if (open) openPanel(id);
  }

  function onOrb(id) {
    const n = byId[id];
    if (!n) return;
    if (id === focus) {
      openPanel(id);
      return;
    }
    if (id === n.parent || (byId[focus] && id === byId[focus].parent)) {
      setFocus(id);
      return;
    }
    if ((kids[id] || []).length) setFocus(id);
    else {
      active = id;
      openPanel(id);
      draw();
    }
  }

  svg.addEventListener("pointerdown", (e) => {
    if (e.target.closest(".mm-node")) return;
    drag = { x: e.clientX - view.x, y: e.clientY - view.y, sx: e.clientX, sy: e.clientY };
    dragged = false;
    svg.setPointerCapture(e.pointerId);
  });
  svg.addEventListener("pointermove", (e) => {
    if (!drag) return;
    if (Math.hypot(e.clientX - drag.sx, e.clientY - drag.sy) > 8) dragged = true;
    view.x = e.clientX - drag.x;
    view.y = e.clientY - drag.y;
    applyView();
  });
  svg.addEventListener("pointerup", () => {
    if (drag && !dragged) goBack();
    drag = null;
  });
  svg.addEventListener("wheel", (e) => {
    e.preventDefault();
    const next = Math.min(2.4, Math.max(0.4, view.s * (e.deltaY > 0 ? 0.92 : 1.08)));
    const rect = svg.getBoundingClientRect();
    const px = e.clientX - rect.left;
    const py = e.clientY - rect.top;
    const wx = (px - view.x) / view.s;
    const wy = (py - view.y) / view.s;
    view.s = next;
    view.x = px - wx * view.s;
    view.y = py - wy * view.s;
    applyView();
  }, { passive: false });

  if (sheetToggle) sheetToggle.addEventListener("click", () => document.body.classList.toggle("mm-sheet-open"));
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
      if ((kids[hit.id] || []).length) setFocus(hit.id);
      else setFocus(hit.parent || hit.id);
      if (!kids[hit.id]?.length) {
        active = hit.id;
        openPanel(hit.id);
        draw();
      }
    }, 160);
  });

  window.addEventListener("resize", () => {
    layoutHome();
    fitHome();
    draw();
  });

  Promise.all([
    fetch("data/mindmap.json").then((r) => r.json()),
    fetch("data/jobs.json").then((r) => r.json()).catch(() => ({ openings: [] })),
  ]).then(([g, j]) => {
    graph = g;
    jobs = j;
    index();
    const start = () => {
      if (svg.clientWidth < 40) {
        requestAnimationFrame(start);
        return;
      }
      layoutHome();
      fitHome();
      setFocus(g.center || "embodied-ai");
      document.body.classList.remove("mm-sheet-open");
    };
    start();
  }).catch((err) => {
    body.innerHTML = `<p>Failed to load mind map: ${err}</p>`;
  });
})();
