import MindElixir, { SIDE } from "https://cdn.jsdelivr.net/npm/mind-elixir@5.13.0/dist/MindElixir.js";

const KIND = {
  hub: "hub — the field",
  domain: "branch of the field",
  concept: "idea, not a paper",
  method: "algorithm you implement",
  paper: "one specific paper",
  framework: "code or stack you run",
  lab: "lab or company (jobs attach)",
};

const STYLE = {
  hub: { background: "#243028", color: "#f4f1ea", fontSize: "18" },
  domain: { background: "#cfe8d4", color: "#1b1f1c", fontSize: "15" },
  paper: { background: "#c9dff0", color: "#1b1f1c" },
  method: { background: "#f3ddb0", color: "#1b1f1c" },
  concept: { background: "#ddd4ee", color: "#1b1f1c" },
  framework: { background: "#f1cfc4", color: "#1b1f1c" },
  lab: { background: "#eceae2", color: "#1b1f1c" },
};

const panel = document.getElementById("mm-panel");
const body = document.getElementById("mm-panel-body") || panel;
const search = document.getElementById("mm-search");
const filters = document.getElementById("mm-filters");
const fitBtn = document.getElementById("mm-fit");
const sheetToggle = document.getElementById("mm-sheet-toggle");
const host = document.getElementById("mm-map");

let graph = { nodes: [], edges: [] };
let jobs = { openings: [] };
let mind = null;
let domainFilter = "all";
let active = null;

function phone() {
  return window.matchMedia("(max-width: 860px)").matches;
}

function nodeById(id) {
  return graph.nodes.find((n) => n.id === id);
}

function neighbors(id) {
  const s = new Set();
  for (const e of graph.edges) {
    if (e.from === id) s.add(e.to);
    if (e.to === id) s.add(e.from);
  }
  return [...s].map(nodeById).filter(Boolean);
}

function leaf(n, expanded) {
  return {
    id: n.id,
    topic: n.label,
    tags: [n.kind],
    style: STYLE[n.kind] || STYLE.concept,
    expanded: expanded !== false,
    children: [],
  };
}

function toTree() {
  const q = (search.value || "").trim().toLowerCase();
  const match = (n) =>
    !q ||
    n.label.toLowerCase().includes(q) ||
    (n.brief || "").toLowerCase().includes(q) ||
    n.id.includes(q);

  const hub = graph.nodes.find((n) => n.id === graph.center) || graph.nodes[0];
  const domains = graph.nodes.filter((n) => n.kind === "domain");
  const shownDomains =
    domainFilter === "all" ? domains : domains.filter((d) => d.domain === domainFilter || d.id === domainFilter);

  const children = shownDomains.map((d) => {
    const kids = graph.nodes.filter(
      (n) => n.kind !== "hub" && n.kind !== "domain" && n.domain === d.domain && match(n)
    );
    const groups = { method: [], concept: [], paper: [], framework: [], lab: [], other: [] };
    for (const k of kids) (groups[k.kind] || groups.other).push(k);
    const nested = [];
    for (const kind of ["concept", "method", "paper", "framework", "lab", "other"]) {
      for (const k of groups[kind]) nested.push(leaf(k, !q ? false : true));
    }
    if (q && !nested.length && !match(d)) return null;
    return {
      ...leaf(d, true),
      children: nested,
    };
  }).filter(Boolean);

  return {
    nodeData: {
      ...leaf(hub, true),
      children,
    },
  };
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
  const n = nodeById(id);
  if (!n) return;
  active = id;
  document.body.classList.add("mm-sheet-open");
  const res = n.resources || [];
  const vids = res.filter((r) => r.type === "video" || /youtu/.test(r.url || ""));
  const rest = res.filter((r) => !vids.includes(r));
  const firstYt = vids.map((v) => ytId(v.url)).find(Boolean);
  const dirs = n.research_directions || [];
  const nb = neighbors(id);
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
        ? `<ul class="mm-jobs">${relatedJobs.slice(0, 12).map((j) => `<li><a href="${j.url}">${j.title}</a><small>${j.company} · ${j.location || ""} · ${j.seniority}</small></li>`).join("")}${intern.length ? `<li class="mm-empty">${intern.length} internship(s).</li>` : ""}</ul>`
        : `<p class="mm-empty">${n.kind === "lab" ? "No tracked official openings in the last jobs scrape." : "Not a hiring node — open a lab branch."}</p>`
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

function mount() {
  if (!host) return;
  const data = toTree();
  const side = SIDE ?? MindElixir.SIDE ?? 2;
  if (!mind) {
    mind = new MindElixir({
      el: host,
      direction: side,
      draggable: false,
      contextMenu: false,
      toolBar: true,
      nodeMenu: false,
      keypress: false,
      editable: false,
      locale: "en",
      overflowHidden: false,
      primaryNodeHorizontalGap: phone() ? 40 : 70,
      primaryNodeVerticalGap: phone() ? 12 : 18,
    });
    const bus = mind.bus;
    const onSelect = (arg) => {
      const node = Array.isArray(arg) ? arg[0] : arg?.node || arg;
      const id = node?.id || node?.nodeObj?.id;
      if (id) openNode(id);
    };
    if (bus?.addListener) {
      bus.addListener("selectNodes", onSelect);
      bus.addListener("selectNode", onSelect);
      bus.addListener("click", onSelect);
    }
    host.addEventListener("click", (e) => {
      const el = e.target.closest("[data-nodeid], me-tpc, .tpc, .map-topic");
      if (!el) return;
      const id = el.getAttribute("data-nodeid") || el.nodeObj?.id;
      if (id) openNode(id);
    });
    mind.init(data);
  } else if (mind.refresh) {
    mind.refresh(data);
  } else {
    mind.init(data);
  }
  if (mind.toCenter) mind.toCenter();
  else if (mind.scaleFit) mind.scaleFit();
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
      mount();
    });
    filters.appendChild(b);
  });
}

if (fitBtn) {
  fitBtn.addEventListener("click", () => {
    if (mind?.toCenter) mind.toCenter();
    else if (mind?.scaleFit) mind.scaleFit();
  });
}
if (sheetToggle) sheetToggle.addEventListener("click", () => document.body.classList.toggle("mm-sheet-open"));

let searchT = 0;
search.addEventListener("input", () => {
  clearTimeout(searchT);
  searchT = setTimeout(mount, 140);
});

Promise.all([
  fetch("data/mindmap.json").then((r) => r.json()),
  fetch("data/jobs.json").then((r) => r.json()).catch(() => ({ openings: [] })),
]).then(([g, j]) => {
  graph = g;
  jobs = j;
  chips();
  mount();
  openNode(g.center);
  document.body.classList.remove("mm-sheet-open");
}).catch((err) => {
  body.innerHTML = `<p>Failed to load mind map: ${err}</p>`;
});
