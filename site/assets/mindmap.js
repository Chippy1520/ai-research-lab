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

  function layout() {
    const W = Math.max(svg.clientWidth, 320);
    const H = Math.max(svg.clientHeight, 320);
    const mobile = phone();
    const cy = H / 2 + 8;
    const f = byId[focus];
    const children = kids[focus] || [];
    const path = pathTo(focus);
    const pos = new Map();
    const left = mobile ? 56 : 88;
    const step = Math.min(mobile ? 92 : 130, (W * 0.42) / Math.max(path.length, 1));
    path.forEach((n, i) => {
      const last = i === path.length - 1;
      pos.set(n.id, {
        x: left + i * step,
        y: cy,
        r: last ? (R[n.kind] || 18) + 6 : 14,
        spine: true,
        focus: last,
      });
    });
    const fp = pos.get(focus) || { x: W * 0.45, y: cy, r: 28 };
    const n = children.length;
    const colX = fp.x + (mobile ? 118 : 188);
    const gap = Math.min(64, Math.max(42, (H - 160) / Math.max(n, 1)));
    const span = gap * Math.max(n - 1, 0);
    children.forEach((c, i) => {
      const t = n === 1 ? 0.5 : i / (n - 1);
      const y = n === 1 ? cy : cy - span / 2 + i * gap;
      const bow = Math.sin((t - 0.5) * Math.PI) * (mobile ? 18 : 36);
      pos.set(c.id, { x: colX + bow, y, r: R[c.kind] || R.default });
    });

    const parentId = f?.parent;
    const ghosts = parentId
      ? (kids[parentId] || []).filter((s) => s.id !== focus)
      : [];
    const pp = parentId ? pos.get(parentId) : null;
    if (pp && ghosts.length) {
      const gGap = Math.min(40, Math.max(28, (H * 0.42) / ghosts.length));
      const gSpan = gGap * Math.max(ghosts.length - 1, 0);
      ghosts.forEach((s, i) => {
        const y = ghosts.length === 1 ? pp.y + 56 : pp.y + 48 + i * gGap - gSpan / 4;
        pos.set(s.id, { x: pp.x + (mobile ? 8 : 12), y, r: 11, ghost: true });
      });
    }
    return { pos, ghosts };
  }

  function el(name, attrs) {
    const n = document.createElementNS("http://www.w3.org/2000/svg", name);
    for (const [k, v] of Object.entries(attrs || {})) n.setAttribute(k, v);
    return n;
  }

  function draw() {
    const { pos, ghosts } = layout();
    world = el("g");
    applyView();
    const children = kids[focus] || [];
    const path = pathTo(focus);
    const fp = pos.get(focus);
    const f = byId[focus];
    const pp = f?.parent ? pos.get(f.parent) : null;

    for (let i = 1; i < path.length; i++) {
      const a = pos.get(path[i - 1].id);
      const b = pos.get(path[i].id);
      if (!a || !b) continue;
      world.appendChild(el("path", {
        class: "mm-edge spine",
        d: `M ${a.x} ${a.y} L ${b.x} ${b.y}`,
      }));
    }
    for (const g of ghosts) {
      const p = pos.get(g.id);
      if (!pp || !p) continue;
      world.appendChild(el("path", {
        class: "mm-edge ghost",
        d: `M ${pp.x} ${pp.y} L ${p.x} ${p.y}`,
      }));
    }
    for (const c of children) {
      const p = pos.get(c.id);
      if (!fp || !p) continue;
      const midX = (fp.x + p.x) / 2;
      world.appendChild(el("path", {
        class: "mm-edge" + (c.id === active ? " on" : ""),
        d: `M ${fp.x} ${fp.y} C ${midX} ${fp.y}, ${midX} ${p.y}, ${p.x} ${p.y}`,
      }));
    }

    const drawNode = (n, p) => {
      const g = el("g", {
        class: `mm-node ${n.kind}${n.id === active || p.focus ? " active" : ""}${p.spine && !p.focus ? " ancestor" : ""}${p.ghost ? " ghost" : ""}`,
        transform: `translate(${p.x} ${p.y})`,
      });
      g.dataset.id = n.id;
      if (p.focus) {
        g.appendChild(el("circle", {
          r: p.r + 6,
          fill: "none",
          stroke: "#243028",
          "stroke-width": 1.25,
        }));
      }
      g.appendChild(el("circle", {
        r: p.r,
        fill: p.ghost ? "none" : (FILL[n.kind] || FILL.lab),
        stroke: p.ghost ? "#9aa39a" : (STROKE[n.kind] || STROKE.lab),
        "stroke-width": p.ghost ? 1.2 : p.focus ? 2.2 : 1.6,
        "stroke-dasharray": p.ghost ? "3 3" : "",
      }));
      const t = el("text", { y: p.r + 16 });
      t.textContent = n.label;
      g.appendChild(t);
      if (!p.ghost) {
        g.addEventListener("click", (ev) => {
          ev.stopPropagation();
          onOrb(n.id);
        });
      }
      world.appendChild(g);
    };

    path.forEach((n) => {
      if (pos.has(n.id)) drawNode(n, pos.get(n.id));
    });
    for (const g of ghosts) drawNode(g, pos.get(g.id));
    for (const c of children) drawNode(c, pos.get(c.id));

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
    view.x = 0;
    view.y = 0;
    view.s = 1;
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

  window.addEventListener("resize", () => draw());

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
      setFocus(g.center || "embodied-ai");
      document.body.classList.remove("mm-sheet-open");
    };
    start();
  }).catch((err) => {
    body.innerHTML = `<p>Failed to load mind map: ${err}</p>`;
  });
})();
