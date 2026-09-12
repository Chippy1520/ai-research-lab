(() => {
  const svg = document.getElementById("mm-svg");
  const panel = document.getElementById("mm-panel");
  const search = document.getElementById("mm-search");
  const filters = document.getElementById("mm-filters");
  const hint = document.getElementById("mm-hint");
  if (!svg || !panel) return;

  const view = { x: 0, y: 0, s: 0.55 };
  let graph = { nodes: [], edges: [] };
  let jobs = { openings: [] };
  let active = null;
  let domainFilter = "all";
  let positions = new Map();
  let world = null;
  let laid = { w: 0, h: 0 };

  const KIND = {
    hub: "dark — the field this map is about",
    domain: "green — a branch of the field",
    concept: "lilac — an idea, not a paper",
    method: "gold — an algorithm you implement",
    paper: "blue — one specific paper",
    framework: "terracotta — code or stack you run",
    lab: "grey — a lab or company (jobs attach here)",
  };
  const R = { hub: 28, domain: 20, default: 14 };

  function neighbors(id) {
    const s = new Set();
    for (const e of graph.edges) {
      if (e.from === id) s.add(e.to);
      if (e.to === id) s.add(e.from);
    }
    return s;
  }

  function layout() {
    const W = svg.clientWidth || 1100;
    const H = svg.clientHeight || 820;
    if (positions.size && laid.w === W && laid.h === H) return;
    laid = { w: W, h: H };
    const cx = W / 2;
    const cy = H / 2;
    const S = Math.min(W, H);
    const domains = graph.nodes.filter((n) => n.kind === "domain");
    positions = new Map();
    const hub = graph.nodes.find((n) => n.id === graph.center) || graph.nodes[0];
    if (hub) positions.set(hub.id, { x: cx, y: cy, r: R.hub });
    const domainR = Math.max(300, S * 0.36);
    domains.forEach((d, i) => {
      const a = -Math.PI / 2 + (i * 2 * Math.PI) / Math.max(domains.length, 1);
      positions.set(d.id, {
        x: cx + Math.cos(a) * domainR,
        y: cy + Math.sin(a) * domainR,
        r: R.domain,
        a,
      });
    });
    const grouped = {};
    for (const n of graph.nodes) {
      if (n.kind === "hub" || n.kind === "domain") continue;
      (grouped[n.domain] ||= []).push(n);
    }
    domains.forEach((d) => {
      const kids = grouped[d.domain] || [];
      const base = positions.get(d.id);
      const sector = (2 * Math.PI) / Math.max(domains.length, 1);
      const spread = sector * 0.9;
      const rings = Math.max(3, Math.ceil(kids.length / 5));
      kids.forEach((n, i) => {
        const ring = i % rings;
        const slot = Math.floor(i / rings);
        const slots = Math.ceil(kids.length / rings);
        const a = base.a - spread / 2 + (slots === 1 ? spread / 2 : (slot * spread) / (slots - 1));
        const rad = domainR + 150 + ring * 95 + (slot % 2) * 22;
        positions.set(n.id, {
          x: cx + Math.cos(a) * rad,
          y: cy + Math.sin(a) * rad,
          r: R.default,
        });
      });
    });
    for (const n of graph.nodes) {
      if (!positions.has(n.id)) positions.set(n.id, { x: cx, y: cy + 90, r: R.default });
    }
  }

  function visible(n) {
    if (domainFilter !== "all" && n.domain !== domainFilter && n.kind !== "hub") return false;
    const q = (search.value || "").trim().toLowerCase();
    if (!q) return true;
    return (
      n.label.toLowerCase().includes(q) ||
      (n.brief || "").toLowerCase().includes(q) ||
      n.id.includes(q)
    );
  }

  function applyView() {
    if (world) world.setAttribute("transform", `translate(${view.x} ${view.y}) scale(${view.s})`);
  }

  function fitIds(ids) {
    const pts = ids.map((id) => positions.get(id)).filter(Boolean);
    if (!pts.length) return;
    let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    for (const p of pts) {
      x0 = Math.min(x0, p.x - 40);
      y0 = Math.min(y0, p.y - 40);
      x1 = Math.max(x1, p.x + 40);
      y1 = Math.max(y1, p.y + 50);
    }
    const W = svg.clientWidth || 900;
    const H = svg.clientHeight || 700;
    const pad = 48;
    const bw = Math.max(x1 - x0 + pad * 2, 160);
    const bh = Math.max(y1 - y0 + pad * 2, 160);
    const s = Math.min(W / bw, H / bh, 1.85);
    view.s = s;
    view.x = W / 2 - ((x0 + x1) / 2) * s;
    view.y = H / 2 - ((y0 + y1) / 2) * s;
    applyView();
  }

  function paintFocus() {
    const nb = active ? neighbors(active) : new Set();
    svg.querySelectorAll(".mm-node").forEach((el) => {
      const id = el.dataset.id;
      el.classList.toggle("active", id === active);
      el.classList.toggle("near", nb.has(id));
    });
    svg.querySelectorAll(".mm-edge").forEach((el) => {
      const on = active && (el.dataset.from === active || el.dataset.to === active);
      el.classList.toggle("on", !!on);
    });
  }

  function draw() {
    layout();
    const visId = new Set(graph.nodes.filter(visible).map((n) => n.id));
    world = document.createElementNS("http://www.w3.org/2000/svg", "g");
    applyView();

    const eg = document.createElementNS("http://www.w3.org/2000/svg", "g");
    for (const e of graph.edges) {
      if (!visId.has(e.from) || !visId.has(e.to)) continue;
      const a = positions.get(e.from);
      const b = positions.get(e.to);
      const p = document.createElementNS("http://www.w3.org/2000/svg", "path");
      const mx = (a.x + b.x) / 2;
      const my = (a.y + b.y) / 2;
      p.setAttribute("d", `M ${a.x} ${a.y} Q ${mx} ${my} ${b.x} ${b.y}`);
      p.setAttribute("class", "mm-edge");
      p.dataset.from = e.from;
      p.dataset.to = e.to;
      eg.appendChild(p);
    }
    world.appendChild(eg);

    const ng = document.createElementNS("http://www.w3.org/2000/svg", "g");
    for (const n of graph.nodes) {
      if (!visId.has(n.id)) continue;
      const p = positions.get(n.id);
      const wrap = document.createElementNS("http://www.w3.org/2000/svg", "g");
      wrap.setAttribute("class", `mm-node ${n.kind}`);
      wrap.dataset.id = n.id;
      wrap.setAttribute("transform", `translate(${p.x} ${p.y})`);
      const c = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      c.setAttribute("r", p.r);
      wrap.appendChild(c);
      const t = document.createElementNS("http://www.w3.org/2000/svg", "text");
      t.setAttribute("y", p.r + 14);
      t.setAttribute("text-anchor", "middle");
      t.textContent = n.label;
      wrap.appendChild(t);
      wrap.addEventListener("click", (ev) => {
        ev.stopPropagation();
        openNode(n.id);
      });
      ng.appendChild(wrap);
    }
    world.appendChild(ng);
    svg.replaceChildren(world);
    paintFocus();
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

  function openNode(id, zoom = true) {
    const n = graph.nodes.find((x) => x.id === id);
    if (!n) return;
    active = id;
    paintFocus();
    if (zoom) fitIds([id, ...neighbors(id)]);
    const res = n.resources || [];
    const vids = res.filter((r) => r.type === "video" || /youtu/.test(r.url || ""));
    const rest = res.filter((r) => !vids.includes(r));
    const firstYt = vids.map((v) => ytId(v.url)).find(Boolean);
    const dirs = n.research_directions || [];
    const nb = [...neighbors(id)]
      .map((i) => graph.nodes.find((x) => x.id === i))
      .filter(Boolean);
    const relatedJobs = jobsFor(n);
    const intern = relatedJobs.filter((j) => j.seniority === "internship");
    panel.innerHTML = `
      <div class="mm-kicker">${KIND[n.kind] || n.kind} · ${n.domain}</div>
      <h2>${n.label}</h2>
      <p>${n.brief || ""}</p>
      ${firstYt ? `<h3>Watch</h3><div class="mm-yt"><iframe src="https://www.youtube-nocookie.com/embed/${firstYt}" title="Lecture" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe></div>` : ""}
      ${n.why ? `<h3>Why it is on the map</h3><p>${n.why}</p>` : ""}
      <h3>Neighbors</h3>
      <ul class="mm-res">${nb.map((x) => `<li><a href="#" data-go="${x.id}">${x.label}</a> <small>${x.kind}</small></li>`).join("") || "<li class='mm-empty'>Isolated</li>"}</ul>
      <h3>Resources</h3>
      <ul class="mm-res">${[...vids, ...rest].map((r) => `<li><a href="${r.url}">${r.title}</a></li>`).join("") || "<li class='mm-empty'>None yet</li>"}</ul>
      ${dirs.length ? `<h3>Research directions</h3><ul class="mm-res">${dirs.map((d) => `<li>${d}</li>`).join("")}</ul>` : ""}
      <h3>Jobs & internships</h3>
      ${
        relatedJobs.length
          ? `<ul class="mm-jobs">${relatedJobs.slice(0, 12).map((j) => `<li><a href="${j.url}">${j.title}</a><small>${j.company} · ${j.location || ""} · ${j.seniority}</small></li>`).join("")}${intern.length ? `<li class="mm-empty">${intern.length} internship(s) in this slice of the desk.</li>` : ""}</ul>`
          : `<p class="mm-empty">${n.kind === "lab" ? "No tracked official openings in the last jobs scrape." : "Not a hiring node — open a lab on the outer ring."}</p>`
      }
    `;
    panel.querySelectorAll("[data-go]").forEach((a) => {
      a.addEventListener("click", (e) => {
        e.preventDefault();
        openNode(a.dataset.go);
      });
    });
  }

  function chips() {
    const raw = [...new Set(graph.nodes.map((n) => n.domain))];
    const domains = ["all", ...raw.filter((d) => d === "foundations"), ...raw.filter((d) => d !== "all" && d !== "foundations" && d !== "hub")];
    filters.innerHTML = "";
    domains.forEach((d) => {
      const b = document.createElement("button");
      b.className = "mm-chip" + (d === domainFilter ? " on" : "");
      b.type = "button";
      b.textContent = d;
      b.addEventListener("click", () => {
        domainFilter = d;
        chips();
        draw();
      });
      filters.appendChild(b);
    });
  }

  let drag = null;
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
  svg.addEventListener("pointerup", () => {
    drag = null;
  });
  svg.addEventListener("wheel", (e) => {
    e.preventDefault();
    const next = Math.min(2.4, Math.max(0.28, view.s * (e.deltaY > 0 ? 0.92 : 1.08)));
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

  let searchT = 0;
  search.addEventListener("input", () => {
    clearTimeout(searchT);
    searchT = setTimeout(draw, 120);
  });
  window.addEventListener("resize", () => {
    laid = { w: 0, h: 0 };
    draw();
  });

  Promise.all([
    fetch("data/mindmap.json").then((r) => r.json()),
    fetch("data/jobs.json").then((r) => r.json()).catch(() => ({ openings: [] })),
  ]).then(([g, j]) => {
    graph = g;
    jobs = j;
    chips();
    draw();
    openNode(g.center, false);
    if (hint) hint.textContent = `Updated ${g.updated} · ${g.nodes.length} concepts · click a node to zoom its neighborhood`;
  }).catch((err) => {
    panel.innerHTML = `<p>Failed to load mind map: ${err}</p>`;
  });
})();
