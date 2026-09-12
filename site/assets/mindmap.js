(() => {
  const stage = document.getElementById("mm-stage");
  const host = document.getElementById("mm-cy");
  const panel = document.getElementById("mm-panel");
  const body = document.getElementById("mm-panel-body") || panel;
  const search = document.getElementById("mm-search");
  const filters = document.getElementById("mm-filters");
  const hint = document.getElementById("mm-hint");
  const fitBtn = document.getElementById("mm-fit");
  const sheetToggle = document.getElementById("mm-sheet-toggle");
  if (!host || typeof cytoscape !== "function") {
    if (panel) panel.innerHTML = "<p>Cytoscape.js failed to load. Check the CDN.</p>";
    return;
  }

  const KIND = {
    hub: "dark — the field this map is about",
    domain: "green — a branch of the field",
    concept: "lilac — an idea, not a paper",
    method: "gold — an algorithm you implement",
    paper: "blue — one specific paper",
    framework: "terracotta — code or stack you run",
    lab: "grey — a lab or company (jobs attach here)",
  };
  const FILL = {
    hub: "#243028",
    domain: "#cfe8d4",
    paper: "#c9dff0",
    method: "#f3ddb0",
    concept: "#ddd4ee",
    framework: "#f1cfc4",
    lab: "#eceae2",
  };
  const STROKE = {
    hub: "#7dcea0",
    domain: "#2d6a45",
    paper: "#2a6f97",
    method: "#b57a12",
    concept: "#6b4ea0",
    framework: "#a24c38",
    lab: "#606660",
  };
  const R = { hub: 34, domain: 22, default: 12 };

  let graph = { nodes: [], edges: [] };
  let jobs = { openings: [] };
  let cy = null;
  let active = null;
  let domainFilter = "all";

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
    const domainR = Math.max(phone() ? 140 : 280, S * (phone() ? 0.28 : 0.34));
    domains.forEach((d, i) => {
      const a = -Math.PI / 2 + (i * 2 * Math.PI) / Math.max(domains.length, 1);
      pos.set(d.id, { x: cx + Math.cos(a) * domainR, y: cy + Math.sin(a) * domainR, a });
    });
    const grouped = {};
    for (const n of graph.nodes) {
      if (n.kind === "hub" || n.kind === "domain") continue;
      (grouped[n.domain] ||= []).push(n);
    }
    const ringGap = phone() ? 72 : 92;
    domains.forEach((d) => {
      const kids = grouped[d.domain] || [];
      const base = pos.get(d.id);
      const sector = (2 * Math.PI) / Math.max(domains.length, 1);
      const spread = sector * 0.88;
      const rings = Math.max(3, Math.ceil(kids.length / (phone() ? 4 : 5)));
      kids.forEach((n, i) => {
        const ring = i % rings;
        const slot = Math.floor(i / rings);
        const slots = Math.ceil(kids.length / rings);
        const a = base.a - spread / 2 + (slots === 1 ? spread / 2 : (slot * spread) / Math.max(slots - 1, 1));
        const rad = domainR + (phone() ? 90 : 140) + ring * ringGap + (slot % 2) * 16;
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
      return {
        data: { id: n.id, label: n.label, kind: n.kind },
        position: { x: p.x, y: p.y },
      };
    });
    const edges = graph.edges
      .filter((e) => vis.has(e.from) && vis.has(e.to))
      .map((e, i) => ({ data: { id: `e${i}`, source: e.from, target: e.to } }));
    return [...nodes, ...edges];
  }

  function stylesheet() {
    const fs = phone() ? 11 : 12;
    return [
      {
        selector: "node",
        style: {
          label: "data(label)",
          "text-valign": "bottom",
          "text-halign": "center",
          "text-margin-y": 6,
          "font-family": "Manrope, system-ui, sans-serif",
          "font-size": fs,
          "font-weight": 600,
          color: "#1b1f1c",
          "text-wrap": "wrap",
          "text-max-width": phone() ? 72 : 90,
          "min-zoomed-font-size": 8,
          width: 24,
          height: 24,
          "background-color": "#eceae2",
          "border-width": 2,
          "border-color": "#606660",
        },
      },
      { selector: "node[kind = 'hub']", style: { width: 56, height: 56, "font-size": 14, color: "#f4f1ea", "text-valign": "center", "text-margin-y": 0, "background-color": FILL.hub, "border-color": STROKE.hub } },
      { selector: "node[kind = 'domain']", style: { width: 38, height: 38, "background-color": FILL.domain, "border-color": STROKE.domain } },
      { selector: "node[kind = 'paper']", style: { "background-color": FILL.paper, "border-color": STROKE.paper } },
      { selector: "node[kind = 'method']", style: { "background-color": FILL.method, "border-color": STROKE.method } },
      { selector: "node[kind = 'concept']", style: { "background-color": FILL.concept, "border-color": STROKE.concept } },
      { selector: "node[kind = 'framework']", style: { "background-color": FILL.framework, "border-color": STROKE.framework } },
      { selector: "node[kind = 'lab']", style: { "background-color": FILL.lab, "border-color": STROKE.lab } },
      { selector: "edge", style: { width: 1.2, "line-color": "#c8c2b4", "curve-style": "haystack", opacity: 0.55, "target-arrow-shape": "none" } },
      { selector: "node.active", style: { "border-width": 4 } },
      { selector: "node.near", style: { "border-width": 3 } },
      { selector: "edge.on", style: { width: 2.4, "line-color": "#2d6a45", opacity: 1 } },
    ];
  }

  function mountCy(fitAll) {
    const pos = layoutPositions();
    const elements = elementsFromGraph(pos);
    if (cy) {
      cy.json({ elements });
      cy.style(stylesheet());
      if (fitAll) cy.fit(undefined, phone() ? 24 : 40);
      paintFocus();
      return;
    }
    cy = cytoscape({
      container: host,
      elements,
      style: stylesheet(),
      layout: { name: "preset", fit: false },
      minZoom: 0.22,
      maxZoom: 2.6,
      wheelSensitivity: 0.22,
      autoungrabify: true,
      boxSelectionEnabled: false,
      textureOnViewport: true,
      motionBlur: false,
      pixelRatio: "auto",
    });
    cy.on("tap", "node", (evt) => {
      openNode(evt.target.id());
    });
    if (fitAll) cy.fit(undefined, phone() ? 24 : 40);
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
    if (zoom) {
      const nbh = cy.getElementById(id).closedNeighborhood();
      cy.animate({ fit: { eles: nbh, padding: phone() ? 36 : 48 }, duration: 220, easing: "ease-out" });
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
    body.querySelectorAll("[data-go]").forEach((a) => {
      a.addEventListener("click", (e) => {
        e.preventDefault();
        openNode(a.dataset.go);
      });
    });
    body.scrollTop = 0;
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
        mountCy(true);
      });
      filters.appendChild(b);
    });
  }

  if (fitBtn) {
    fitBtn.addEventListener("click", () => {
      if (!cy) return;
      cy.animate({ fit: { padding: phone() ? 24 : 40 }, duration: 200 });
    });
  }
  if (sheetToggle) {
    sheetToggle.addEventListener("click", () => {
      document.body.classList.toggle("mm-sheet-open");
    });
  }

  let searchT = 0;
  search.addEventListener("input", () => {
    clearTimeout(searchT);
    searchT = setTimeout(() => mountCy(true), 140);
  });

  let resizeT = 0;
  window.addEventListener("resize", () => {
    clearTimeout(resizeT);
    resizeT = setTimeout(() => {
      if (cy) cy.resize();
      mountCy(true);
    }, 120);
  });

  Promise.all([
    fetch("data/mindmap.json").then((r) => r.json()),
    fetch("data/jobs.json").then((r) => r.json()).catch(() => ({ openings: [] })),
  ]).then(([g, j]) => {
    graph = g;
    jobs = j;
    chips();
    mountCy(true);
    openNode(g.center, { zoom: false, sheet: false });
    if (hint) hint.textContent = `${g.nodes.length} concepts · pinch / tap`;
  }).catch((err) => {
    body.innerHTML = `<p>Failed to load mind map: ${err}</p>`;
  });
})();
