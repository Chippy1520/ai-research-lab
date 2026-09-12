(() => {
  const svg = document.getElementById("mm-svg");
  const crumb = document.getElementById("mm-crumb");
  const search = document.getElementById("mm-search");
  const body = document.getElementById("mm-panel-body");
  const sheetToggle = document.getElementById("mm-sheet-toggle");
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
  const R = { hub: 36, domain: 26, area: 22, default: 14 };

  let graph = { nodes: [], edges: [], center: "embodied-ai" };
  let jobs = { openings: [] };
  let byId = {};
  let kids = {};
  let focus = null;
  let active = null;
  const view = { x: 0, y: 0, s: 1 };
  let world = null;
  let drag = null;

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

  function layout() {
    const W = svg.clientWidth || 900;
    const H = svg.clientHeight || 640;
    const cx = W / 2;
    const cy = H / 2 + (phone() ? 10 : 20);
    const f = byId[focus];
    const children = kids[focus] || [];
    const pos = new Map();
    pos.set(focus, { x: cx, y: cy, r: R[f?.kind] || R.default });

    if (f?.parent && byId[f.parent]) {
      pos.set(f.parent, { x: cx, y: cy - Math.min(H * 0.28, 160), r: 16, up: true });
    }

    const n = children.length;
    const ring0 = Math.max(phone() ? 110 : 150, Math.min(W, H) * 0.28);
    const per = n > 10 ? Math.ceil(n / 2) : n;
    children.forEach((c, i) => {
      const ring = n > 10 ? Math.floor(i / per) : 0;
      const slot = n > 10 ? i % per : i;
      const count = n > 10 ? (ring === 0 ? per : n - per) : n;
      const a = -Math.PI / 2 + (slot * 2 * Math.PI) / Math.max(count, 1) + ring * 0.18;
      const rad = ring0 + ring * (phone() ? 70 : 90);
      pos.set(c.id, { x: cx + Math.cos(a) * rad, y: cy + Math.sin(a) * rad, r: R[c.kind] || R.default });
    });
    return pos;
  }

  function el(name, attrs) {
    const n = document.createElementNS("http://www.w3.org/2000/svg", name);
    for (const [k, v] of Object.entries(attrs || {})) n.setAttribute(k, v);
    return n;
  }

  function draw() {
    const pos = layout();
    const f = byId[focus];
    world = el("g");
    applyView();

    const children = kids[focus] || [];
    const fp = pos.get(focus);
    for (const c of children) {
      const p = pos.get(c.id);
      const e = el("path", {
        class: "mm-edge" + (c.id === active ? " on" : ""),
        d: `M ${fp.x} ${fp.y} Q ${(fp.x + p.x) / 2} ${(fp.y + p.y) / 2 - 12} ${p.x} ${p.y}`,
      });
      world.appendChild(e);
    }
    if (f?.parent && pos.has(f.parent)) {
      const u = pos.get(f.parent);
      world.appendChild(el("path", {
        class: "mm-edge",
        d: `M ${u.x} ${u.y} L ${fp.x} ${fp.y}`,
      }));
    }

    const drawNode = (n, p) => {
      const g = el("g", {
        class: `mm-node ${n.kind}${n.id === active ? " active" : ""}${(kids[n.id] || []).length ? " has-kids" : ""}`,
        transform: `translate(${p.x} ${p.y})`,
      });
      g.dataset.id = n.id;
      const c = el("circle", { r: p.r });
      g.appendChild(c);
      const t = el("text", { y: p.r + 14 });
      t.textContent = p.up ? "↑ " + n.label : n.label;
      g.appendChild(t);
      g.addEventListener("click", (ev) => {
        ev.stopPropagation();
        onOrb(n.id);
      });
      world.appendChild(g);
    };

    if (f?.parent && byId[f.parent] && pos.has(f.parent)) drawNode(byId[f.parent], pos.get(f.parent));
    for (const c of children) drawNode(c, pos.get(c.id));
    if (f) drawNode(f, fp);

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
    body.innerHTML = `
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
    body.scrollTop = 0;
  }

  function setFocus(id, open = true) {
    if (!byId[id]) return;
    focus = id;
    view.x = 0;
    view.y = 0;
    view.s = 1;
    draw();
    if (open) openPanel(id);
  }

  function onOrb(id) {
    const n = byId[id];
    if (!n) return;
    if (id === focus) {
      openPanel(id);
      draw();
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
    drag = { x: e.clientX - view.x, y: e.clientY - view.y };
    svg.setPointerCapture(e.pointerId);
  });
  svg.addEventListener("pointermove", (e) => {
    if (!drag) return;
    view.x = e.clientX - drag.x;
    view.y = e.clientY - drag.y;
    applyView();
  });
  svg.addEventListener("pointerup", () => { drag = null; });
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

  window.addEventListener("resize", () => draw());

  Promise.all([
    fetch("data/mindmap.json").then((r) => r.json()),
    fetch("data/jobs.json").then((r) => r.json()).catch(() => ({ openings: [] })),
  ]).then(([g, j]) => {
    graph = g;
    jobs = j;
    index();
    setFocus(g.center || "embodied-ai");
    document.body.classList.remove("mm-sheet-open");
  }).catch((err) => {
    body.innerHTML = `<p>Failed to load mind map: ${err}</p>`;
  });
})();
