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

  function layoutPositions() {
    const W = host.clientWidth || 900;
    const H = host.clientHeight || 640;
    const cx = W / 2;
    const cy = H / 2;
    const S = Math.min(W, H);
    const domains = graph.nodes.filter((n) => n.kind === "domain");
    const pos = new Map();
    const hub = graph.nodes.find((n) => n.id === graph.center) || graph.nodes[0];
    if (hub) pos.set(hub.id, { x: cx, y: cy });
    const domainR = Math.max(phone() ? 120 : 240, S * 0.28);
    domains.forEach((d, i) => {
      const a = -Math.PI / 2 + (i * 2 * Math.PI) / Math.max(domains.length, 1);
      pos.set(d.id, { x: cx + Math.cos(a) * domainR, y: cy + Math.sin(a) * domainR, a });
    });
    const grouped = {};
    for (const n of graph.nodes) {
      if (n.kind === "hub" || n.kind === "domain") continue;
      (grouped[n.domain] ||= []).push(n);
    }
    domains.forEach((d) => {
      const kids = grouped[d.domain] || [];
      const base = pos.get(d.id);
      const sector = (2 * Math.PI) / Math.max(domains.length, 1);
      const spread = sector * 0.9;
      const rings = Math.max(3, Math.ceil(kids.length / 5));
      kids.forEach((n, i) => {
        const ring = i % rings;
        const slot = Math.floor(i / rings);
        const slots = Math.ceil(kids.length / rings);
        const a = base.a - spread / 2 + (slots === 1 ? spread / 2 : (slot * spread) / Math.max(slots - 1, 1));
        const rad = domainR + 100 + ring * 78 + (slot % 2) * 14;
        pos.set(n.id, { x: cx + Math.cos(a) * rad, y: cy + Math.sin(a) * rad });
      });
    });
    for (const n of graph.nodes) {
      if (!pos.has(n.id)) pos.set(n.id, { x: cx, y: cy + 80 });
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
      .map((e, i) => ({ data: { id: `e${i}`, source: e.from, target: e.to } }));
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
          "text-margin-y": 4,
          "font-family": "Manrope, system-ui, sans-serif",
          "font-size": 11,
          "font-weight": 500,
          color: "#c8c8c8",
          "text-outline-width": 2,
          "text-outline-color": "#191919",
          "text-wrap": "wrap",
          "text-max-width": 86,
          "min-zoomed-font-size": 9,
          width: 14,
          height: 14,
          "background-color": "#9a9a9a",
          "border-width": 0,
          "overlay-padding": 6,
          "overlay-opacity": 0,
        },
      },
      { selector: "node[kind = 'hub']", style: { width: 28, height: 28, "font-size": 13, color: "#eee", "background-color": FILL.hub, "overlay-color": FILL.hub, "overlay-opacity": 0.25, "overlay-padding": 10 } },
      { selector: "node[kind = 'domain']", style: { width: 20, height: 20, "background-color": FILL.domain, "overlay-color": FILL.domain, "overlay-opacity": 0.18, "overlay-padding": 7 } },
      { selector: "node[kind = 'paper']", style: { "background-color": FILL.paper } },
      { selector: "node[kind = 'method']", style: { "background-color": FILL.method } },
      { selector: "node[kind = 'concept']", style: { "background-color": FILL.concept } },
      { selector: "node[kind = 'framework']", style: { "background-color": FILL.framework } },
      { selector: "node[kind = 'lab']", style: { "background-color": FILL.lab } },
      { selector: "edge", style: { width: 1, "line-color": "#5a5a5a", "curve-style": "haystack", "haystack-radius": 0.6, opacity: 0.35, "target-arrow-shape": "none" } },
      { selector: "node.active", style: { width: 22, height: 22, "overlay-opacity": 0.35, "overlay-padding": 10, "overlay-color": "#8a5cf5" } },
      { selector: "node.near", style: { "overlay-opacity": 0.2, "overlay-padding": 6 } },
      { selector: "edge.on", style: { width: 1.8, "line-color": "#8a5cf5", opacity: 0.85 } },
      { selector: ".faded", style: { opacity: 0.08 } },
    ];
  }

  function setModeButtons() {
    if (globalBtn) globalBtn.classList.toggle("on", mode === "global");
    if (localBtn) localBtn.classList.toggle("on", mode === "local");
  }

  function applyLocal() {
    if (!cy) return;
    cy.batch(() => {
      cy.elements().removeClass("faded");
      if (mode !== "local" || !active) {
        cy.elements().style("display", "element");
        return;
      }
      const n = cy.getElementById(active);
      if (!n.nonempty()) return;
      const keep = n.closedNeighborhood();
      cy.elements().forEach((el) => {
        el.style("display", keep.contains(el) ? "element" : "none");
      });
    });
  }

  function coseOnce(eles) {
    const target = eles || cy.elements(":visible");
    target.layout({
      name: "cose",
      animate: false,
      randomize: false,
      numIter: 600,
      nodeRepulsion: function (n) { return n.data("kind") === "hub" ? 12000 : 4500; },
      idealEdgeLength: 72,
      gravity: 0.4,
      nestingFactor: 1.2,
      coolingFactor: 0.92,
      minTemp: 1,
    }).run();
  }

  function mountCy(fitAll) {
    const pos = layoutPositions();
    const elements = elementsFromGraph(pos);
    if (cy) {
      cy.json({ elements });
      cy.style(stylesheet());
      coseOnce();
      applyLocal();
      if (fitAll) cy.fit(cy.elements(":visible"), phone() ? 28 : 48);
      paintFocus();
      return;
    }
    cy = cytoscape({
      container: host,
      elements,
      style: stylesheet(),
      layout: { name: "preset", fit: false },
      minZoom: 0.18,
      maxZoom: 3,
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
    cy.on("tap", (evt) => {
      if (evt.target === cy && mode === "global") {
        cy.elements().removeClass("faded");
      }
    });
    cy.on("mouseover", "node", (evt) => {
      if (mode !== "global") return;
      const keep = evt.target.closedNeighborhood();
      cy.elements().addClass("faded");
      keep.removeClass("faded");
    });
    cy.on("mouseout", "node", () => {
      if (mode !== "global") return;
      cy.elements().removeClass("faded");
      paintFocus();
    });
    coseOnce();
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
    applyLocal();
    paintFocus();
    if (zoom) {
      const shown = mode === "local" ? cy.getElementById(id).closedNeighborhood() : cy.getElementById(id).closedNeighborhood();
      if (mode === "local") coseOnce(shown);
      cy.animate({ fit: { eles: shown, padding: phone() ? 40 : 56 }, duration: 240, easing: "ease-out" });
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
    cy.elements().style("display", "element");
    cy.elements().removeClass("faded");
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

  if (fitBtn) fitBtn.addEventListener("click", () => { if (cy) cy.fit(cy.elements(":visible"), phone() ? 28 : 48); });
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
    searchT = setTimeout(() => { mode = "global"; setModeButtons(); mountCy(true); }, 140);
  });

  let resizeT = 0;
  window.addEventListener("resize", () => {
    clearTimeout(resizeT);
    resizeT = setTimeout(() => { if (cy) cy.resize(); mountCy(true); }, 150);
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
    if (hint) hint.textContent = `${g.nodes.length} notes · Global / Local`;
  }).catch((err) => {
    body.innerHTML = `<p>Failed to load mind map: ${err}</p>`;
  });
})();
