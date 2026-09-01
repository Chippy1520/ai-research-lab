"use strict";

const curriculumState = { payload: null, manifest: null };
const q = (selector) => document.querySelector(selector);

function safe(value) {
  return String(value ?? "").replace(/[&<>'"]/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;"
  }[character]));
}

function currentModule() {
  const day = curriculumState.payload.state.current_day;
  return curriculumState.payload.modules.find((module) => module.metadata.day === day)
    || curriculumState.payload.modules[0];
}

function currentResearch() {
  const day = curriculumState.payload.state.current_day;
  return curriculumState.payload.research_log.entries.find((entry) => entry.day === day);
}

function renderMetrics() {
  const metrics = curriculumState.manifest.curriculum;
  q("#current-day").textContent = String(metrics.current_day).padStart(2, "0");
  q("#mapped-lessons").textContent = metrics.mapped_lessons;
  q("#generated-modules").textContent = metrics.generated_modules;
  q("#research-sources").textContent = metrics.research_sources;
  q("#curriculum-updated").textContent = `PLAN ${curriculumState.payload.plan.updated_on}`;
}

function videoEmbed(url) {
  const match = String(url).match(/(?:youtu\.be\/|v=|embed\/)([A-Za-z0-9_-]{11})/);
  if (!match) return `<a href="${safe(url)}" target="_blank" rel="noreferrer">Open video ↗</a>`;
  return `<iframe class="video-frame" src="https://www.youtube-nocookie.com/embed/${match[1]}" title="Technical lecture" loading="lazy" allowfullscreen></iframe>`;
}

function tableBlock(records) {
  if (!Array.isArray(records) || !records.length) return "";
  const columns = Object.keys(records[0]);
  return `<table class="article-table"><thead><tr>${columns.map((column) => `<th>${safe(column)}</th>`).join("")}</tr></thead><tbody>${records.map((record) => `<tr>${columns.map((column) => `<td>${safe(record[column])}</td>`).join("")}</tr>`).join("")}</tbody></table>`;
}

function articleBlock(block) {
  switch (block.type) {
    case "header": return `<h2>${safe(block.content)}</h2>`;
    case "subheader": return `<h3>${safe(block.content)}</h3>`;
    case "markdown": return window.marked ? window.marked.parse(block.content) : `<p>${safe(block.content)}</p>`;
    case "latex": return `<div class="math-block">\\[${safe(block.content)}\\]</div>`;
    case "caption": return `<p class="article-caption">${safe(block.content)}</p>`;
    case "video": return videoEmbed(block.content);
    case "code": return `<pre><code class="language-${safe(block.language)}">${safe(block.content)}</code></pre>`;
    case "table": return tableBlock(block.content);
    default: return "";
  }
}

async function renderCurrentModule() {
  const module = currentModule();
  if (!module) {
    q("#module-article").innerHTML = '<p class="empty">The current module has not been generated yet.</p>';
    return;
  }
  const metadata = module.metadata;
  q("#module-title").textContent = `Day ${String(metadata.day).padStart(2, "0")} · ${metadata.title}`;
  q("#module-domain").textContent = metadata.domain;
  q("#module-duration").textContent = `${metadata.duration_minutes} minute research session`;
  q("#module-article").innerHTML = module.article.map(articleBlock).join("");
  q("#experiment-path").textContent = module.experiment_path || "No experiment attached";
  q("#experiment-source").textContent = module.experiment_source || "No static experiment source is available.";
  const research = currentResearch();
  renderSourceLedger(research?.sources || []);
  if (window.MathJax?.typesetPromise) await window.MathJax.typesetPromise([q("#module-article")]);
}

function renderSourceLedger(sources) {
  q("#source-ledger").innerHTML = sources.map((source) => {
    const date = source.year || `accessed ${source.accessed_on || "date unknown"}`;
    return `<article class="source-entry"><span class="source-type">${safe(source.kind)}</span><h3>${safe(source.title)}</h3><p>${safe(source.authors)} · ${safe(date)}</p><a href="${safe(source.url)}" target="_blank" rel="noreferrer">OPEN ORIGINAL SOURCE ↗</a></article>`;
  }).join("");
}

function prepareTabs() {
  document.querySelectorAll(".module-tab").forEach((button) => button.addEventListener("click", () => {
    document.querySelectorAll(".module-tab").forEach((item) => item.classList.remove("active"));
    document.querySelectorAll(".module-panel").forEach((panel) => panel.classList.remove("active"));
    button.classList.add("active");
    q(`#${button.dataset.panel}`).classList.add("active");
  }));
  q("#copy-code").addEventListener("click", async () => {
    await navigator.clipboard.writeText(q("#experiment-source").textContent);
    q("#copy-code").textContent = "Copied";
    window.setTimeout(() => { q("#copy-code").textContent = "Copy code"; }, 1600);
  });
}

function lessonClass(lesson) {
  const currentDay = curriculumState.payload.state.current_day;
  if (lesson.day === currentDay) return "current";
  if (lesson.status === "generated") return "generated";
  return "planned";
}

function lessonCard(lesson) {
  return `<article class="lesson-card ${lessonClass(lesson)}"><span class="lesson-number">DAY ${String(lesson.day).padStart(2, "0")} · CYCLE ${String(lesson.cycle).padStart(2, "0")}</span><h3>${safe(lesson.topic)}</h3><div class="lesson-meta">${safe(lesson.stage)} · ${safe(lesson.status).toUpperCase()}</div><span class="lesson-domain">${safe(lesson.domain)}</span><div class="thread-list">${lesson.foundation_threads.map(safe).join(" · ")}</div></article>`;
}

function renderRoadmap() {
  const query = q("#lesson-search").value.toLowerCase().trim();
  const domain = q("#domain-filter").value;
  const stage = q("#stage-filter").value;
  const lessons = curriculumState.payload.plan.lessons.filter((lesson) => {
    const searchable = [lesson.topic, lesson.domain, lesson.stage, ...lesson.foundation_threads].join(" ").toLowerCase();
    return (!query || searchable.includes(query)) && (domain === "all" || lesson.domain === domain) && (stage === "all" || lesson.stage === stage);
  });
  q("#roadmap-grid").innerHTML = lessons.length ? lessons.map(lessonCard).join("") : '<p class="empty">No mapped lessons match this filter.</p>';
}

function prepareRoadmap() {
  const plan = curriculumState.payload.plan;
  const stages = [...new Set(plan.lessons.map((lesson) => lesson.stage))];
  q("#stage-filter").insertAdjacentHTML("beforeend", stages.map((stage) => `<option>${safe(stage)}</option>`).join(""));
  q("#horizon-rule").textContent = plan.horizon_policy.extension_rule;
  ["#lesson-search", "#domain-filter", "#stage-filter"].forEach((selector) => q(selector).addEventListener("input", renderRoadmap));
  renderRoadmap();
}

function renderFoundations() {
  q("#foundation-threads").innerHTML = curriculumState.payload.plan.supporting_cs_threads.map((thread, index) => `<article class="foundation-item"><span>${String(index + 1).padStart(2, "0")}</span><h3>${safe(thread)}</h3></article>`).join("");
}

function renderResearchLedger() {
  const entries = [...curriculumState.payload.research_log.entries].reverse();
  q("#research-ledger").innerHTML = entries.map((entry) => {
    const lesson = curriculumState.payload.plan.lessons.find((item) => item.day === entry.day);
    const corrections = (entry.corrections || []).map((correction) => `<div class="correction"><b>Correction · ${safe(correction.date || "undated")}</b><br>${safe(correction.note || correction)}</div>`).join("");
    const sources = entry.sources.map((source) => `<div class="research-source"><b>${safe(source.title)}</b><span>${safe(source.kind)} · ${safe(source.authors)}</span><br><a href="${safe(source.url)}" target="_blank" rel="noreferrer">SOURCE ↗</a></div>`).join("");
    return `<article class="research-record"><header><h3>Day ${String(entry.day).padStart(2, "0")} · ${safe(lesson?.topic || entry.module_slug)}</h3><time>${safe(entry.researched_on)}</time></header><p>${safe(entry.scope_note)}</p><div class="research-sources">${sources}</div>${corrections}</article>`;
  }).join("");
}

function showCurriculumError(error) {
  const banner = q("#curriculum-error");
  banner.hidden = false;
  banner.textContent = `Unable to load curriculum data: ${error.message}`;
  console.error(error);
}

async function initializeCurriculum() {
  const [curriculumResponse, manifestResponse] = await Promise.all([fetch("data/curriculum.json"), fetch("data/manifest.json")]);
  if (!curriculumResponse.ok || !manifestResponse.ok) throw new Error("Static curriculum data is unavailable");
  [curriculumState.payload, curriculumState.manifest] = await Promise.all([curriculumResponse.json(), manifestResponse.json()]);
  renderMetrics();
  prepareTabs();
  await renderCurrentModule();
  prepareRoadmap();
  renderFoundations();
  renderResearchLedger();
}

initializeCurriculum().catch(showCurriculumError);
