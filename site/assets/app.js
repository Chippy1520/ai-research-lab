"use strict";

const state = { ecosystem: null, jobs: null, manifest: null };
const $ = (selector) => document.querySelector(selector);

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>'"]/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;"
  }[char]));
}

function formatFunding(value) {
  if (value === null || value === undefined) return "Undisclosed";
  return value >= 1000 ? `$${(value / 1000).toFixed(value % 1000 ? 2 : 0)}B` : `$${value}M`;
}

function renderMetrics() {
  const m = state.manifest;
  $("#company-count").textContent = m.company_count;
  $("#humanoid-count").textContent = m.humanoid_count;
  $("#opening-count").textContent = m.opening_count;
  $("#early-count").textContent = m.early_career_count;
  $("#as-of").textContent = `DATA ${m.ecosystem_as_of}`;
  $("#jobs-checked").textContent = `CHECKED ${m.jobs_last_checked}`;
  $("#all-job-count").textContent = `(${m.opening_count})`;
}

function renderTimeline() {
  const companies = [...state.ecosystem.companies].sort((a, b) => a.founded - b.founded);
  $("#timeline").innerHTML = companies.map((company) => `
    <div class="time-node"><time>${company.founded}</time><b>${escapeHtml(company.name)}</b></div>
  `).join("");
}

function companyCard(company) {
  const source = company.sources?.[0];
  return `<article class="company-card">
    <header><h3>${escapeHtml(company.name)}</h3><span class="year">${company.founded}</span></header>
    <span class="tag">${escapeHtml(company.category)}</span>
    <p class="focus">${escapeHtml(company.focus)}</p>
    <div class="company-meta">
      <div><span>US base / HQ</span><b>${escapeHtml(company.hq_city)}, ${escapeHtml(company.hq_state)}</b></div>
      <div><span>Capital observation</span><b>${escapeHtml(company.valuation_label)}</b></div>
      <div><span>Funding observation</span><b>${formatFunding(company.funding_usd_millions)}</b></div>
      <div><span>Stage</span><b>${escapeHtml(company.stage)}</b></div>
    </div>
    <div class="company-links">
      <a href="${escapeHtml(company.careers_url)}" target="_blank" rel="noreferrer">CAREERS ↗</a>
      ${source ? `<a href="${escapeHtml(source.url)}" target="_blank" rel="noreferrer">EVIDENCE ↗</a>` : ""}
    </div>
  </article>`;
}

function renderCompanies() {
  const search = $("#company-search").value.toLowerCase().trim();
  const category = $("#company-filter").value;
  const companies = state.ecosystem.companies.filter((company) => {
    const haystack = [company.name, company.focus, company.hq_city, company.hq_state, company.stage].join(" ").toLowerCase();
    return (!search || haystack.includes(search)) && (category === "all" || company.category === category);
  });
  $("#company-grid").innerHTML = companies.length
    ? companies.map(companyCard).join("")
    : '<p class="empty">No companies match this filter.</p>';
}

function prepareCompanyFilters() {
  const categories = [...new Set(state.ecosystem.companies.map((company) => company.category))].sort();
  $("#company-filter").insertAdjacentHTML("beforeend", categories.map((category) => `<option value="${escapeHtml(category)}">${escapeHtml(category)}</option>`).join(""));
  $("#company-search").addEventListener("input", renderCompanies);
  $("#company-filter").addEventListener("change", renderCompanies);
}

function companyCountForHub(hubName) {
  return state.ecosystem.companies.filter((company) => company.cluster === hubName).length;
}

function showHub(hub, button) {
  document.querySelectorAll(".hub-node").forEach((node) => node.classList.remove("active"));
  button?.classList.add("active");
  const count = companyCountForHub(hub.name);
  $("#hub-detail").innerHTML = `
    <h3>${escapeHtml(hub.name)}</h3>
    <div class="cluster-count">${count} TRACKED COMPANIES / US BASES</div>
    <p>${escapeHtml(hub.thesis)}</p>
    <h4>Institutional anchors</h4><ul>${hub.institutions.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>
    <h4>Representative organizations</h4><p>${hub.organizations.map(escapeHtml).join(" · ")}</p>
    <h4>Likely evolution</h4><p>${escapeHtml(hub.outlook)}</p>`;
}

function renderMap() {
  const stage = $("#map-stage");
  const hubs = state.ecosystem.hubs;
  hubs.forEach((hub, index) => {
    const x = Math.max(4, Math.min(96, ((hub.longitude + 125) / 59) * 100));
    const y = Math.max(6, Math.min(94, ((50 - hub.latitude) / 26) * 100));
    const count = Math.max(1, companyCountForHub(hub.name));
    const button = document.createElement("button");
    button.className = "hub-node";
    button.style.left = `${x}%`;
    button.style.top = `${y}%`;
    if (x < 8) button.classList.add("edge-left");
    if (x > 92) button.classList.add("edge-right");
    button.style.setProperty("--count", count);
    button.setAttribute("aria-label", `Inspect ${hub.name}`);
    button.innerHTML = `<i></i><span>${escapeHtml(hub.name)}</span>`;
    button.addEventListener("click", () => showHub(hub, button));
    stage.appendChild(button);
    if (index === 0) showHub(hub, button);
  });
  $("#evolution-thesis").textContent = state.ecosystem.evolution_thesis;
}

function jobCard(job) {
  return `<article class="job-card">
    <span class="company">${escapeHtml(job.company)} · ${escapeHtml(job.seniority).toUpperCase()}</span>
    <h4>${escapeHtml(job.title)}</h4>
    <span class="location">${escapeHtml(job.location)}</span>
    ${job.qualification_excerpt ? `<details><summary>Qualification excerpt</summary><p>${escapeHtml(job.qualification_excerpt)}</p></details>` : ""}
    <a href="${escapeHtml(job.url)}" target="_blank" rel="noreferrer">OPEN OFFICIAL POSTING ↗</a>
  </article>`;
}

function renderEarlyJobs() {
  const early = state.jobs.openings.filter((job) => ["internship", "new graduate"].includes(job.seniority));
  $("#early-jobs").innerHTML = early.length ? early.map(jobCard).join("") : '<p class="empty">No verified early-career roles in the latest scan.</p>';
}

function renderSignals() {
  const signals = state.jobs.requirement_signals || [];
  const maximum = Math.max(1, ...signals.map((signal) => signal.company_mentions));
  $("#signals").innerHTML = signals.slice(0, 9).map((signal) => `
    <div class="signal-row"><b>${escapeHtml(signal.skill)}</b><div class="signal-track"><i style="width:${(signal.company_mentions / maximum) * 100}%"></i></div><span class="signal-count">${signal.company_mentions} co · ${signal.role_mentions} roles</span></div>
  `).join("");
  $("#portfolio-actions").innerHTML = signals.slice(0, 3).map((signal) => `<div class="action-item"><b>${escapeHtml(signal.skill)}</b><br>${escapeHtml(signal.portfolio_response)}</div>`).join("");
}

function renderAllJobs() {
  const search = $("#job-search").value.toLowerCase().trim();
  const jobs = state.jobs.openings.filter((job) => !search || [job.company, job.title, job.location, job.seniority].join(" ").toLowerCase().includes(search)).slice(0, 100);
  $("#job-list").innerHTML = jobs.map((job) => `<div class="job-row"><b>${escapeHtml(job.title)}</b><span>${escapeHtml(job.company)}</span><span>${escapeHtml(job.location)}</span><a href="${escapeHtml(job.url)}" target="_blank" rel="noreferrer">OPEN ↗</a></div>`).join("");
}

async function renderReport(path) {
  const response = await fetch(path);
  if (!response.ok) throw new Error(`Report request failed: ${response.status}`);
  const markdown = await response.text();
  $("#report").innerHTML = window.marked ? window.marked.parse(markdown) : `<pre>${escapeHtml(markdown)}</pre>`;
}

async function prepareReports() {
  const reports = state.manifest.reports;
  $("#report-select").innerHTML = reports.map((report) => `<option value="${escapeHtml(report.path)}">${escapeHtml(report.date)}</option>`).join("");
  $("#report-select").addEventListener("change", (event) => renderReport(event.target.value).catch(showError));
  if (reports.length) await renderReport(reports[0].path);
}

function showError(error) {
  const banner = $("#error-banner");
  banner.hidden = false;
  banner.textContent = `Unable to load intelligence data: ${error.message}. Reload the page or inspect the source repository.`;
  console.error(error);
}

async function initialize() {
  const [ecosystemResponse, jobsResponse, manifestResponse] = await Promise.all([
    fetch("data/ecosystem.json"), fetch("data/jobs.json"), fetch("data/manifest.json")
  ]);
  if (![ecosystemResponse, jobsResponse, manifestResponse].every((response) => response.ok)) throw new Error("One or more data files are unavailable");
  [state.ecosystem, state.jobs, state.manifest] = await Promise.all([
    ecosystemResponse.json(), jobsResponse.json(), manifestResponse.json()
  ]);
  renderMetrics();
  renderTimeline();
  prepareCompanyFilters();
  renderCompanies();
  renderMap();
  renderEarlyJobs();
  renderSignals();
  renderAllJobs();
  $("#job-search").addEventListener("input", renderAllJobs);
  await prepareReports();
  if (window.location.hash) {
    document.querySelector(window.location.hash)?.scrollIntoView();
  }
}

initialize().catch(showError);
