(() => {
  const svg = document.getElementById("mm-svg");
  const panel = document.getElementById("mm-panel");
  const search = document.getElementById("mm-search");
  const filters = document.getElementById("mm-filters");
  const hint = document.getElementById("mm-hint");
  if (!svg || !panel) return;

  const view = { x: 0, y: 0, s: 1 };
  let graph = { nodes: [], edges: [] };
  let jobs = { openings: [] };
  let active = null;
  let domainFilter = "all";
  let positions = new Map();

  const KIND = {
    hub: "dark — the field this map is about",
    domain: "green — a branch of the field",
    concept: "lilac — an idea, not a paper",
    method: "gold — an algorithm you can implement",
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
    const W = svg.clientWidth || 900;
    const H = svg.clientHeight || 700;
    const cx = W / 2;
    const cy = H / 2 - 10;
    const byId = Object.fromEntries(graph.nodes.map((n) => [n.id, n]));
    const domains = graph.nodes.filter((n) => n.kind === "domain");
    positions = new Map();
    const hub = byId[graph.center] || graph.nodes[0];
    if (hub) positions.set(hub.id, { x: cx, y: cy, r: R.hub });
    domains.forEach((d, i) => {
      const a = -Math.PI / 2 + (i * 2 * Math.PI) / Math.max(domains.length, 1);
      positions.set(d.id, {
        x: cx + Math.cos(a) * 240,
        y: cy + Math.sin(a) * 240,
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
      kids.forEach((n, i) => {
        const spread = Math.min(1.1, 0.22 * kids.length);
        const a = base.a - spread / 2 + (kids.length === 1 ? 0 : (i * spread) / (kids.length - 1));
        const ring = 400 + (i % 3) * 48;
        positions.set(n.id, {
          x: cx + Math.cos(a) * ring,
          y: cy + Math.sin(a) * ring,
          r: R.default,
        });
      });
    });
    for (const n of graph.nodes) {
      if (!positions.has(n.id)) positions.set(n.id, { x: cx, y: cy + 80, r: R.default });
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

  function draw() {
    layout();
    const visId = new Set(graph.nodes.filter(visible).map((n) => n.id));
    const nb = active ? neighbors(active) : new Set();
    const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
    g.setAttribute("transform", `translate(${view.x} ${view.y}) scale(${view.s})`);

    const eg = document.createElementNS("http://www.w3.org/2000/svg", "g");
    for (const e of graph.edges) {
      if (!visId.has(e.from) || !visId.has(e.to)) continue;
      const a = positions.get(e.from);
      const b = positions.get(e.to);
      const p = document.createElementNS("http://www.w3.org/2000/svg", "line");
      p.setAttribute("x1", a.x);
      p.setAttribute("y1", a.y);
      p.setAttribute("x2", b.x);
      p.setAttribute("y2", b.y);
      p.setAttribute("class", "mm-edge" + (active && (e.from === active || e.to === active) ? " on" : ""));
      eg.appendChild(p);
    }
    g.appendChild(eg);

    const ng = document.createElementNS("http://www.w3.org/2000/svg", "g");
    const order = [...graph.nodes].sort((a, b) => (a.id === active ? 1 : 0) - (b.id === active ? 1 : 0));
    for (const n of order) {
      if (!visId.has(n.id)) continue;
      const p = positions.get(n.id);
      const wrap = document.createElementNS("http://www.w3.org/2000/svg", "g");
      wrap.setAttribute("class", `mm-node ${n.kind}${n.id === active ? " active" : ""}`);
      wrap.dataset.id = n.id;
      const c = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      c.setAttribute("cx", p.x);
      c.setAttribute("cy", p.y);
      c.setAttribute("r", p.r + (n.id === active || nb.has(n.id) ? 3 : 0));
      wrap.appendChild(c);
      const t = document.createElementNS("http://www.w3.org/2000/svg", "text");
      t.setAttribute("x", p.x);
      t.setAttribute("y", p.y + p.r + 14);
      t.setAttribute("text-anchor", "middle");
      t.textContent = n.label;
      wrap.appendChild(t);
      wrap.addEventListener("click", (ev) => {
        ev.stopPropagation();
        openNode(n.id);
      });
      ng.appendChild(wrap);
    }
    g.appendChild(ng);
    svg.replaceChildren(g);
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

  function openNode(id) {
    const n = graph.nodes.find((x) => x.id === id);
    if (!n) return;
    active = id;
    draw();
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
    draw();
  });
  svg.addEventListener("pointerup", () => {
    drag = null;
  });
  svg.addEventListener("wheel", (e) => {
    e.preventDefault();
    const next = Math.min(2.2, Math.max(0.45, view.s * (e.deltaY > 0 ? 0.92 : 1.08)));
    view.s = next;
    draw();
  }, { passive: false });

  search.addEventListener("input", draw);
  window.addEventListener("resize", draw);

  Promise.all([
    fetch("data/mindmap.json").then((r) => r.json()),
    fetch("data/jobs.json").then((r) => r.json()).catch(() => ({ openings: [] })),
  ]).then(([g, j]) => {
    graph = g;
    jobs = j;
    chips();
    draw();
    openNode(g.center);
    if (hint) hint.textContent = `Updated ${g.updated} · ${g.nodes.length} concepts · drag / scroll to pan-zoom`;
  }).catch((err) => {
    panel.innerHTML = `<p>Failed to load mind map: ${err}</p>`;
  });
})();
