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

function currentLesson() {
  const day = curriculumState.payload.state.current_day;
  return curriculumState.payload.plan.lessons.find((lesson) => lesson.day === day);
}

function currentResearch() {
  const day = curriculumState.payload.state.current_day;
  return curriculumState.payload.research_log.entries.find((entry) => entry.day === day);
}

function renderPublicationMetadata() {
  const metrics = curriculumState.manifest.curriculum;
  const research = currentResearch();
  const lesson = currentLesson();
  const learning = curriculumState.payload.learning_log.entries.find((entry) => entry.day === metrics.current_day);
  q("#current-day").textContent = `Day ${String(metrics.current_day).padStart(2, "0")} of an open horizon`;
  q("#mapped-lessons").textContent = metrics.mapped_lessons;
  q("#generated-modules").textContent = metrics.generated_modules;
  q("#research-sources").textContent = metrics.research_sources;
  q("#curriculum-updated").textContent = `PLAN · ${curriculumState.payload.plan.updated_on}`;
  q("#module-researched").textContent = research?.researched_on || "Pending";
  q("#current-foundations").textContent = lesson?.foundation_threads.join(" · ") || "—";
  q("#reading-status").textContent = learning?.status === "ready" ? "Ready to study" : (learning?.status || "Not generated");
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

function articleDeck(module) {
  const objective = module.article.find((block) => block.type === "markdown" && block.content.includes("Research objective"));
  if (!objective) return "A generation-day technical chapter moving from engineering motivation through formulation, implementation, failure analysis, and research practice.";
  const container = document.createElement("div");
  container.innerHTML = window.marked ? window.marked.parse(objective.content) : objective.content;
  return container.textContent.replace("Research objective.", "").trim();
}

function slugify(value, index) {
  const slug = value.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  return slug || `section-${index + 1}`;
}

function buildArticleToc() {
  const headings = [...q("#module-article").querySelectorAll("h3")];
  q("#article-toc").innerHTML = headings.map((heading, index) => {
    heading.id = slugify(heading.textContent, index);
    return `<li><a href="#${heading.id}">${safe(heading.textContent.replace(/^\d+\s*·\s*/, ""))}</a></li>`;
  }).join("");
  if (!("IntersectionObserver" in window)) return;
  const items = [...q("#article-toc").querySelectorAll("li")];
  const observer = new IntersectionObserver((entries) => entries.forEach((entry) => {
    if (!entry.isIntersecting) return;
    items.forEach((item) => item.classList.toggle("active", item.querySelector("a").hash === `#${entry.target.id}`));
  }), { rootMargin: "-15% 0px -70%", threshold: 0 });
  headings.forEach((heading) => observer.observe(heading));
}

function updateReadingProgress() {
  const article = q("#module-article");
  const start = article.offsetTop;
  const finish = start + article.offsetHeight - window.innerHeight;
  const progress = Math.max(0, Math.min(1, (window.scrollY - start) / Math.max(1, finish - start)));
  q("#reading-progress-bar").style.width = `${progress * 100}%`;
}

async function renderCurrentModule() {
  const module = currentModule();
  if (!module) {
    q("#module-article").innerHTML = '<p class="empty">The current module has not been generated yet.</p>';
    return;
  }
  const metadata = module.metadata;
  q("#module-title").textContent = metadata.title;
  q("#module-domain").textContent = metadata.domain;
  q("#module-duration").textContent = `${metadata.duration_minutes} minutes`;
  q(".publication-deck").textContent = articleDeck(module);
  q("#module-article").innerHTML = module.article.map(articleBlock).join("");
  q("#experiment-path").textContent = module.experiment_path || "No experiment attached";
  q("#experiment-source").textContent = module.experiment_source || "No static experiment source is available.";
  q("#module-source-link").href = module.module_source_url;
  renderSourceLedger(currentResearch()?.sources || []);
  buildArticleToc();
  if (window.MathJax?.typesetPromise) await window.MathJax.typesetPromise([q("#module-article")]);
  updateReadingProgress();
}

function renderSourceLedger(sources) {
  q("#source-ledger").innerHTML = sources.map((source) => {
    const date = source.year || `accessed ${source.accessed_on || "date unknown"}`;
    return `<li class="source-entry"><div><span class="source-type">${safe(source.kind)}</span><h3>${safe(source.title)}</h3><p>${safe(source.authors)} · ${safe(date)}</p></div><a href="${safe(source.url)}" target="_blank" rel="noreferrer">Original source ↗</a></li>`;
  }).join("");
}

function prepareReadingInteractions() {
  q("#copy-code").addEventListener("click", async () => {
    await navigator.clipboard.writeText(q("#experiment-source").textContent);
    q("#copy-code").textContent = "Copied";
    window.setTimeout(() => { q("#copy-code").textContent = "Copy source"; }, 1600);
  });
  window.addEventListener("scroll", updateReadingProgress, { passive: true });
  window.addEventListener("resize", updateReadingProgress);
}

function lessonClass(lesson) {
  if (lesson.day === curriculumState.payload.state.current_day) return "current";
  return lesson.status === "generated" ? "generated" : "planned";
}

function lessonCard(lesson) {
  return `<article class="lesson-card ${lessonClass(lesson)}"><span class="lesson-number">${String(lesson.day).padStart(2, "0")}</span><h3>${safe(lesson.topic)}</h3><div class="lesson-meta">Cycle ${String(lesson.cycle).padStart(2, "0")} · ${safe(lesson.stage)}</div><span class="lesson-domain">${safe(lesson.domain)}</span><div class="thread-list">${lesson.foundation_threads.map(safe).join(" · ")}</div></article>`;
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
  q("#foundation-threads").innerHTML = curriculumState.payload.plan.supporting_cs_threads.map((thread) => `<li class="foundation-item"><span></span><h3>${safe(thread)}</h3></li>`).join("");
}

function renderResearchLedger() {
  const entries = [...curriculumState.payload.research_log.entries].reverse();
  q("#research-ledger").innerHTML = entries.map((entry) => {
    const lesson = curriculumState.payload.plan.lessons.find((item) => item.day === entry.day);
    const corrections = (entry.corrections || []).map((correction) => `<div class="correction"><b>Correction · ${safe(correction.date || "undated")}</b><br>${safe(correction.note || correction)}</div>`).join("");
    const sources = entry.sources.map((source) => `<div class="research-source"><b>${safe(source.title)}</b><span>${safe(source.kind)} · ${safe(source.authors)}</span><br><a href="${safe(source.url)}" target="_blank" rel="noreferrer">Source ↗</a></div>`).join("");
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
  renderPublicationMetadata();
  prepareReadingInteractions();
  await renderCurrentModule();
  prepareRoadmap();
  renderFoundations();
  renderResearchLedger();
}

initializeCurriculum().catch(showCurriculumError);
