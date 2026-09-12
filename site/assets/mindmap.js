(() => {
  const host = document.getElementById("mm-cy");
  const panel = document.getElementById("mm-panel");
  const body = document.getElementById("mm-panel-body") || panel;
  const search = document.getElementById("mm-search");
  const filters = document.getElementById("mm-filters");
  const hint = document.getElementById("mm-hint");
  const fitBtn = document.getElementById("mm-fit");
  const globalBtn = document.getElementById("mm-global");
  const localBtn = document.getElementById("mm-local");
  const sheetToggle = document.getElementById("mm-sheet-toggle");
  if (!host || typeof cytoscape !== "function") {
    if (panel) panel.innerHTML = "<p>Cytoscape.js failed to load. Check the CDN.</p>";
    return;
  }

  const KIND = {
    hub: "the vault — this field",
    domain: "folder — a branch",
    concept: "note — an idea",
    method: "note — an algorithm",
    paper: "note — one paper",
    framework: "note — code you run",
    lab: "note — a lab (jobs attach)",
  };
  const FILL = {
    hub: "#8a5cf5",
    domain: "#3dd68c",
    paper: "#4aa3df",
    method: "#e6b422",
    concept: "#c4b5fd",
    framework: "#e07a5f",
    lab: "#9a9a9a",
  };

  let graph = { nodes: [], edges: [] };
  let jobs = { openings: [] };
  let cy = null;
  let active = null;
  let domainFilter = "all";
  let mode = "global";
  const byId = () => Object.fromEntries(graph.nodes.map((n) => [n.id, n]));

  function phone() {
    return window.matchMedia("(max-width: 860px)").matches;
  }

  function neighbors(id) {
    const s = new Set();
    for (const e of graph.edges) {
      if (e.from === id) s.add(e.to);
      if (e.to === id) s.add(e.from);
    }
    return s;
  }

  function edgeRole(from, to) {
    const map = byId();
    const a = map[from];
    const b = map[to];
    if (!a || !b) return "cross";
    if (a.kind === "hub" || b.kind === "hub") return "spine";
    if (a.kind === "domain" || b.kind === "domain") return "branch";
    return "cross";
  }

  function layoutPositions() {
    const W = Math.max(host.clientWidth || 900, 640);
    const H = Math.max(host.clientHeight || 640, 480);
    const cx = W / 2;
    const cy = H / 2;
    const S = Math.min(W, H);
    const domains = graph.nodes.filter((n) => n.kind === "domain");
    const pos = new Map();
    const hub = graph.nodes.find((n) => n.id === graph.center) || graph.nodes[0];
    if (hub) pos.set(hub.id, { x: cx, y: cy, lock: true });

    const domainR = Math.max(phone() ? 150 : 260, S * 0.36);
    domains.forEach((d, i) => {
      const a = -Math.PI / 2 + (i * 2 * Math.PI) / Math.max(domains.length, 1);
      pos.set(d.id, {
        x: cx + Math.cos(a) * domainR,
        y: cy + Math.sin(a) * domainR,
        a,
        lock: true,
      });
    });

    const grouped = {};
    for (const n of graph.nodes) {
      if (n.kind === "hub" || n.kind === "domain") continue;
      (grouped[n.domain] ||= []).push(n);
    }

    const ringGap = phone() ? 88 : 120;
    domains.forEach((d) => {
      const kids = grouped[d.domain] || [];
      const base = pos.get(d.id);
      const sector = (2 * Math.PI) / Math.max(domains.length, 1);
      const spread = sector * 0.72;
      const perRing = phone() ? 5 : 6;
      const rings = Math.max(1, Math.ceil(kids.length / perRing));
      kids.forEach((n, i) => {
        const ring = Math.floor(i / perRing);
        const slot = i % perRing;
        const onRing = Math.min(perRing, kids.length - ring * perRing);
        const a = base.a - spread / 2 + (onRing === 1 ? spread / 2 : ((slot + 0.5) * spread) / onRing);
        const rad = domainR + 70 + ring * ringGap;
        pos.set(n.id, { x: cx + Math.cos(a) * rad, y: cy + Math.sin(a) * rad });
      });
    });

    for (const n of graph.nodes) {
      if (!pos.has(n.id)) pos.set(n.id, { x: cx, y: cy + 90 });
    }

    const minD = phone() ? 52 : 68;
    const ids = [...pos.keys()];
    for (let iter = 0; iter < 50; iter++) {
      for (let i = 0; i < ids.length; i++) {
        for (let j = i + 1; j < ids.length; j++) {
          const A = pos.get(ids[i]);
          const B = pos.get(ids[j]);
          let dx = B.x - A.x;
          let dy = B.y - A.y;
          const d = Math.hypot(dx, dy) || 0.01;
          if (d >= minD) continue;
          const push = (minD - d) / 2;
          dx /= d;
          dy /= d;
          if (!A.lock) {
            A.x -= dx * push;
            A.y -= dy * push;
          }
          if (!B.lock) {
            B.x += dx * push;
            B.y += dy * push;
          }
        }
      }
    }
    return pos;
  }

  function visibleNode(n) {
    if (domainFilter !== "all" && n.domain !== domainFilter && n.kind !== "hub") return false;
    const q = (search.value || "").trim().toLowerCase();
    if (!q) return true;
    return n.label.toLowerCase().includes(q) || (n.brief || "").toLowerCase().includes(q) || n.id.includes(q);
  }

  function elementsFromGraph(pos) {
    const vis = new Set(graph.nodes.filter(visibleNode).map((n) => n.id));
    const nodes = graph.nodes.filter((n) => vis.has(n.id)).map((n) => {
      const p = pos.get(n.id);
      return { data: { id: n.id, label: n.label, kind: n.kind }, position: { x: p.x, y: p.y } };
    });
    const edges = graph.edges
      .filter((e) => vis.has(e.from) && vis.has(e.to))
      .map((e, i) => ({ data: { id: `e${i}`, source: e.from, target: e.to, role: edgeRole(e.from, e.to) } }));
    return [...nodes, ...edges];
  }

  function stylesheet() {
    return [
      {
        selector: "node",
        style: {
          label: "data(label)",
          "text-valign": "bottom",
          "text-halign": "center",
          "text-margin-y": 6,
          "font-family": "Manrope, system-ui, sans-serif",
          "font-size": 11,
          "font-weight": 500,
          color: "#d0d0d0",
          "text-outline-width": 3,
          "text-outline-color": "#191919",
          "text-wrap": "none",
          "min-zoomed-font-size": 12,
          width: 12,
          height: 12,
          "background-color": "#9a9a9a",
          "border-width": 0,
        },
      },
      {
        selector: "node[kind = 'hub']",
        style: {
          width: 32,
          height: 32,
          "font-size": 15,
          "font-weight": 700,
          color: "#fff",
          "min-zoomed-font-size": 4,
          "background-color": FILL.hub,
          "overlay-color": FILL.hub,
          "overlay-opacity": 0.28,
          "overlay-padding": 12,
          "z-index": 20,
        },
      },
      {
        selector: "node[kind = 'domain']",
        style: {
          width: 20,
          height: 20,
          "font-size": 12,
          "font-weight": 700,
          "min-zoomed-font-size": 6,
          "background-color": FILL.domain,
          "overlay-color": FILL.domain,
          "overlay-opacity": 0.2,
          "overlay-padding": 8,
          "z-index": 15,
        },
      },
      { selector: "node[kind = 'paper']", style: { "background-color": FILL.paper } },
      { selector: "node[kind = 'method']", style: { "background-color": FILL.method } },
      { selector: "node[kind = 'concept']", style: { "background-color": FILL.concept } },
      { selector: "node[kind = 'framework']", style: { "background-color": FILL.framework } },
      { selector: "node[kind = 'lab']", style: { "background-color": FILL.lab } },
      { selector: "edge", style: { width: 1, "line-color": "#444", "curve-style": "haystack", "haystack-radius": 0.8, opacity: 0.15, "target-arrow-shape": "none" } },
      { selector: "edge[role = 'spine']", style: { width: 1.6, "line-color": "#8a5cf5", opacity: 0.45 } },
      { selector: "edge[role = 'branch']", style: { width: 1.1, "line-color": "#5a5a5a", opacity: 0.28 } },
      { selector: "edge[role = 'cross']", style: { opacity: 0.07 } },
      { selector: "node.active", style: { width: 22, height: 22, "overlay-opacity": 0.4, "overlay-padding": 10, "overlay-color": "#8a5cf5", "min-zoomed-font-size": 1, "z-index": 30 } },
      { selector: "node.near", style: { "min-zoomed-font-size": 1, "z-index": 18 } },
      { selector: "node.label-on", style: { "min-zoomed-font-size": 1, "z-index": 40, "font-size": 12 } },
      { selector: "edge.on", style: { width: 2, "line-color": "#8a5cf5", opacity: 0.9 } },
      { selector: ".faded", style: { opacity: 0.07 } },
    ];
  }

  function setModeButtons() {
    if (globalBtn) globalBtn.classList.toggle("on", mode === "global");
    if (localBtn) localBtn.classList.toggle("on", mode === "local");
  }

  function applyRadialPositions() {
    const pos = layoutPositions();
    cy.nodes().forEach((n) => {
      const p = pos.get(n.id());
      if (p) n.position({ x: p.x, y: p.y });
    });
  }

  function showAll() {
    if (!cy) return;
    cy.elements().style("display", "element");
    cy.elements().removeClass("faded");
  }

  function layoutLocal(id) {
    const n = cy.getElementById(id);
    if (!n.nonempty()) return;
    const keep = n.closedNeighborhood();
    cy.elements().forEach((el) => {
      el.style("display", keep.contains(el) ? "element" : "none");
    });
    keep.layout({
      name: "concentric",
      animate: false,
      fit: false,
      minNodeSpacing: phone() ? 42 : 56,
      equidistant: true,
      startAngle: -Math.PI / 2,
      concentric: (node) => (node.id() === id ? 100 : node.data("kind") === "domain" || node.data("kind") === "hub" ? 40 : 10),
      levelWidth: () => 1,
    }).run();
    cy.fit(keep, phone() ? 36 : 64);
  }

  function mountCy(fitAll) {
    const pos = layoutPositions();
    const elements = elementsFromGraph(pos);
    if (cy) {
      cy.json({ elements });
      cy.style(stylesheet());
      showAll();
      if (fitAll) cy.fit(undefined, phone() ? 28 : 48);
      paintFocus();
      return;
    }
    cy = cytoscape({
      container: host,
      elements,
      style: stylesheet(),
      layout: { name: "preset", fit: false },
      minZoom: 0.15,
      maxZoom: 3.2,
      wheelSensitivity: 0.2,
      autoungrabify: false,
      boxSelectionEnabled: false,
      textureOnViewport: true,
      motionBlur: false,
      pixelRatio: "auto",
    });
    cy.on("tap", "node", (evt) => {
      mode = "local";
      setModeButtons();
      openNode(evt.target.id());
    });
    cy.on("mouseover", "node", (evt) => {
      evt.target.addClass("label-on");
      if (mode !== "global") return;
      const keep = evt.target.closedNeighborhood();
      cy.elements().addClass("faded");
      keep.removeClass("faded");
    });
    cy.on("mouseout", "node", (evt) => {
      evt.target.removeClass("label-on");
      if (mode !== "global") return;
      cy.elements().removeClass("faded");
      paintFocus();
    });
    if (fitAll) cy.fit(undefined, phone() ? 28 : 48);
  }

  function paintFocus() {
    if (!cy) return;
    cy.batch(() => {
      cy.nodes().removeClass("active near");
      cy.edges().removeClass("on");
      if (!active) return;
      const n = cy.getElementById(active);
      if (!n.nonempty()) return;
      n.addClass("active");
      n.closedNeighborhood().nodes().addClass("near");
      n.connectedEdges().addClass("on");
    });
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

  function openNode(id, opts = {}) {
    const zoom = opts.zoom !== false;
    const sheet = opts.sheet !== false;
    const n = graph.nodes.find((x) => x.id === id);
    if (!n || !cy) return;
    active = id;
    paintFocus();
    if (mode === "local" && zoom) layoutLocal(id);
    else if (zoom) {
      const nbh = cy.getElementById(id).closedNeighborhood();
      cy.animate({ fit: { eles: nbh, padding: phone() ? 40 : 56 }, duration: 220, easing: "ease-out" });
    }
    if (sheet) document.body.classList.add("mm-sheet-open");

    const res = n.resources || [];
    const vids = res.filter((r) => r.type === "video" || /youtu/.test(r.url || ""));
    const rest = res.filter((r) => !vids.includes(r));
    const firstYt = vids.map((v) => ytId(v.url)).find(Boolean);
    const dirs = n.research_directions || [];
    const nb = [...neighbors(id)].map((i) => graph.nodes.find((x) => x.id === i)).filter(Boolean);
    const relatedJobs = jobsFor(n);
    const intern = relatedJobs.filter((j) => j.seniority === "internship");
    body.innerHTML = `
      <div class="mm-kicker">${KIND[n.kind] || n.kind} · ${n.domain}</div>
      <h2>${n.label}</h2>
      <p>${n.brief || ""}</p>
      ${firstYt ? `<h3>Watch</h3><div class="mm-yt"><iframe src="https://www.youtube-nocookie.com/embed/${firstYt}" title="Lecture" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe></div>` : ""}
      ${n.why ? `<h3>Why it is on the map</h3><p>${n.why}</p>` : ""}
      <h3>Linked</h3>
      <ul class="mm-res">${nb.map((x) => `<li><a href="#" data-go="${x.id}">${x.label}</a> <small>${x.kind}</small></li>`).join("") || "<li class='mm-empty'>Isolated</li>"}</ul>
      <h3>Resources</h3>
      <ul class="mm-res">${[...vids, ...rest].map((r) => `<li><a href="${r.url}">${r.title}</a></li>`).join("") || "<li class='mm-empty'>None yet</li>"}</ul>
      ${dirs.length ? `<h3>Research directions</h3><ul class="mm-res">${dirs.map((d) => `<li>${d}</li>`).join("")}</ul>` : ""}
      <h3>Jobs & internships</h3>
      ${
        relatedJobs.length
          ? `<ul class="mm-jobs">${relatedJobs.slice(0, 12).map((j) => `<li><a href="${j.url}">${j.title}</a><small>${j.company} · ${j.location || ""} · ${j.seniority}</small></li>`).join("")}${intern.length ? `<li class="mm-empty">${intern.length} internship(s) in this slice of the desk.</li>` : ""}</ul>`
          : `<p class="mm-empty">${n.kind === "lab" ? "No tracked official openings in the last jobs scrape." : "Not a hiring node — open a lab."}</p>`
      }
    `;
    body.querySelectorAll("[data-go]").forEach((a) => {
      a.addEventListener("click", (e) => {
        e.preventDefault();
        mode = "local";
        setModeButtons();
        openNode(a.dataset.go);
      });
    });
    body.scrollTop = 0;
  }

  function showGlobal() {
    mode = "global";
    setModeButtons();
    if (!cy) return;
    showAll();
    applyRadialPositions();
    cy.fit(undefined, phone() ? 28 : 48);
    paintFocus();
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
        mode = "global";
        setModeButtons();
        chips();
        mountCy(true);
      });
      filters.appendChild(b);
    });
  }

  if (fitBtn) {
    fitBtn.addEventListener("click", () => {
      if (!cy) return;
      if (mode === "global") applyRadialPositions();
      cy.fit(cy.elements(":visible"), phone() ? 28 : 48);
    });
  }
  if (globalBtn) globalBtn.addEventListener("click", showGlobal);
  if (localBtn) {
    localBtn.addEventListener("click", () => {
      if (!active) return;
      mode = "local";
      setModeButtons();
      openNode(active);
    });
  }
  if (sheetToggle) sheetToggle.addEventListener("click", () => document.body.classList.toggle("mm-sheet-open"));

  let searchT = 0;
  search.addEventListener("input", () => {
    clearTimeout(searchT);
    searchT = setTimeout(() => {
      mode = "global";
      setModeButtons();
      mountCy(true);
    }, 140);
  });

  let resizeT = 0;
  window.addEventListener("resize", () => {
    clearTimeout(resizeT);
    resizeT = setTimeout(() => {
      if (cy) cy.resize();
      if (mode === "global") mountCy(true);
    }, 150);
  });

  Promise.all([
    fetch("data/mindmap.json").then((r) => r.json()),
    fetch("data/jobs.json").then((r) => r.json()).catch(() => ({ openings: [] })),
  ]).then(([g, j]) => {
    graph = g;
    jobs = j;
    chips();
    setModeButtons();
    mountCy(true);
    openNode(g.center, { zoom: false, sheet: false });
    if (hint) hint.textContent = "Zoom in for paper names · click for local graph";
  }).catch((err) => {
    body.innerHTML = `<p>Failed to load mind map: ${err}</p>`;
  });
})();
