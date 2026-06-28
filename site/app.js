const state = {
  notes: [],
  notesBySlug: new Map(),
  tree: null,
  stats: null,
  graph: { nodes: [], edges: [] },
  report: null,
  dashboard: null,
  searchIndex: [],
  searchBySlug: new Map(),
  currentNote: null,
  lang: normalizeLang(new URLSearchParams(location.search).get("lang") || localStorage.getItem("acc-note-lang") || "en"),
  graphMode: "local",
  theme: localStorage.getItem("acc-theme") || "dark",
};

const els = {
  note: document.querySelector("#note"),
  reader: document.querySelector("#reader"),
  editor: document.querySelector("#editor"),
  editorText: document.querySelector("#editor-text"),
  editorPreview: document.querySelector("#editor-preview"),
  editorTitle: document.querySelector("#editor-title"),
  draftStatus: document.querySelector("#draft-status"),
  tree: document.querySelector("#tree"),
  search: document.querySelector("#search"),
  backlinks: document.querySelector("#backlinks"),
  outgoing: document.querySelector("#outgoing"),
  contextHealth: document.querySelector("#context-health"),
  stats: document.querySelector("#stats"),
  breadcrumbs: document.querySelector("#breadcrumbs"),
  noteMeta: document.querySelector("#note-meta"),
  outline: document.querySelector("#outline"),
  globalGraph: document.querySelector("#global-graph"),
  graphInsights: document.querySelector("#graph-insights"),
  graphSummary: document.querySelector("#graph-summary"),
  graphLocal: document.querySelector("#graph-local"),
  graphAll: document.querySelector("#graph-all"),
  langKo: document.querySelector("#lang-ko"),
  langEn: document.querySelector("#lang-en"),
  typeFilters: document.querySelector("#type-filters"),
  commandPalette: document.querySelector("#command-palette"),
  commandInput: document.querySelector("#command-input"),
  commandResults: document.querySelector("#command-results"),
  hoverPreview: document.querySelector("#hover-preview"),
  sidebar: document.querySelector("#sidebar"),
  workspace: document.querySelector(".workspace"),
  downloadLink: document.querySelector("#download-link"),
};

const finePointerQuery = window.matchMedia("(hover: hover) and (pointer: fine)");
let commandItems = [];
let commandSelectionIndex = 0;

const typeLabels = {
  principle: "Principle",
  pattern: "Pattern",
  research: "Research",
  decision: "Decision",
  project: "Project",
  worklog: "Worklog",
  reference: "Reference",
};

function normalizeLang(value) {
  return value === "ko" ? "ko" : "en";
}

function activeContentLang() {
  return currentSlug() === "dashboard" ? "en" : state.lang;
}

function typeLabel(type) {
  return typeLabels[type] || type;
}

function reasonLabel(reason) {
  return reason;
}

const uiText = {
  en: {
    dashboard: "Workspace Status",
    dashboardSubtitle: "Notes to review, recent changes, and graph health in one place.",
    reviewQueue: "Needs Review",
    reviewQueueDescription: "Notes that changed recently or need stronger links.",
    recentlyChanged: "Recently Changed",
    recentlyChangedDescription: "Fresh notes worth checking before the next change.",
    hubNotes: "Hub Notes",
    hubNotesDescription: "Notes other work depends on most often.",
    editorOriginal: "Editing canonical English source. Translations stay read-only in this browser.",
    notes: "Notes",
    brokenLinks: "Broken links",
    orphans: "Orphans",
    generated: "Generated",
    backlinks: "Backlinks",
    outgoing: "Outgoing",
    status: "Status",
    current: "Current",
    incoming: "Incoming",
    mapSignal: "Map signal",
    related: "Related",
    noOutgoing: "No outgoing links.",
    noHeadings: "No headings.",
    draftSaved: "Draft saved",
    updated: "Updated",
    noDirectNeighbors: "No direct neighbors yet",
    notesUnit: "notes",
    linksUnit: "links",
    searchNotes: "Search notes",
    searchPrompt: "Search notes or run a command",
    command: "Command",
    commands: "Commands",
    notesGroup: "Notes",
    noSearchResults: "No matching notes or commands.",
  },
};

const folderLabels = {
  "start": "Start",
  "principles": "Principles",
  "concepts": "Concepts",
  "workflows": "Workflows",
  "projects": "Projects",
  "decisions": "Decisions",
  "research": "Research",
  "worklog": "Worklog",
};

async function loadJson(path) {
  const response = await fetch(path);
  if (!response.ok) throw new Error(`Failed to load ${path}`);
  return response.json();
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function slugKey(value) {
  return value.replace(/\.md$/, "");
}

function t(key) {
  return uiText.en[key] || key;
}

function folderLabel(folder) {
  return folderLabels[folder] || folder;
}

function localizedNote(note) {
  const translation = note?.translations?.[activeContentLang()];
  return {
    ...note,
    displayTitle: translation?.title || note.title,
    displayBody: translation?.body || note.body,
    hasTranslation: Boolean(translation),
  };
}

function localizedTitle(note) {
  return localizedNote(note).displayTitle;
}

function localizedBody(note) {
  return localizedNote(note).displayBody;
}

function sourceTitle(note) {
  return note?.title || note?.resolved_title || note?.slug || "";
}

function syncLanguageControls() {
  document.documentElement.lang = activeContentLang();
  els.langKo.classList.toggle("active", activeContentLang() === "ko");
  els.langEn.classList.toggle("active", activeContentLang() === "en");
}

function summaryFromMarkdown(markdown, limit = 180) {
  return markdown
    .replace(/^# .*\n?/, "")
    .replace(/^#{2,6}\s+.*$/gm, "")
    .replace(/```[\s\S]*?```/g, "")
    .replace(/\[\[([^\]|]+)\|?([^\]]*)\]\]/g, (_match, target, label) => label || target)
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, limit);
}

function resolveNote(target) {
  const key = slugKey(target.trim());
  return state.notesBySlug.get(key) || state.notesBySlug.get(key.split("/").pop());
}

function draftKey(note) {
  return `acc-draft:${note.slug}`;
}

function hasDraft(note) {
  return localStorage.getItem(draftKey(note)) !== null;
}

function preprocessMarkdown(markdown) {
  return markdown.replace(/\[\[([^\]]+)\]\]/g, (_match, rawTarget) => {
    const [target, label] = rawTarget.split("|").map((part) => part.trim());
    const resolved = resolveNote(target);
    const text = escapeHtml(label || target);
    if (!resolved) return `<span class="broken-link">${text}</span>`;
    return `<a class="wiki-link" href="#/${resolved.slug}" data-preview="${resolved.slug}">${text}</a>`;
  });
}

function renderMarkdown(markdown) {
  const prepared = preprocessMarkdown(markdown);
  if (window.marked) {
    marked.setOptions({ gfm: true, breaks: false, headerIds: false, mangle: false });
    return marked.parse(prepared);
  }
  return prepared
    .split(/\n{2,}/)
    .map((block) => `<p>${block}</p>`)
    .join("");
}

async function renderMermaid(container) {
  if (!window.mermaid) return;
  mermaid.initialize({
    startOnLoad: false,
    securityLevel: "strict",
    theme: state.theme === "dark" ? "dark" : "neutral",
  });
  const blocks = [...container.querySelectorAll("code.language-mermaid")];
  for (const [index, block] of blocks.entries()) {
    const source = block.textContent;
    const wrapper = document.createElement("div");
    wrapper.className = "mermaid-block";
    try {
      const { svg } = await mermaid.render(`mermaid-${Date.now()}-${index}`, source);
      wrapper.innerHTML = svg;
    } catch (error) {
      wrapper.innerHTML = `<pre class="mermaid-error">${escapeHtml(error.message)}</pre>`;
    }
    block.closest("pre").replaceWith(wrapper);
  }
}

function extractHeadings(note) {
  return note.body
    .split("\n")
    .filter((line) => /^#{2,3}\s+/.test(line))
    .map((line) => {
      const depth = line.startsWith("###") ? 3 : 2;
      const text = line.replace(/^#{2,3}\s+/, "").trim();
      return { depth, text, id: text.toLowerCase().replace(/[^a-z0-9가-힣]+/g, "-").replace(/^-|-$/g, "") };
    });
}

function addHeadingAnchors(container) {
  const headings = [...container.querySelectorAll("h2, h3")];
  headings.forEach((heading) => {
    const id = heading.textContent.toLowerCase().replace(/[^a-z0-9가-힣]+/g, "-").replace(/^-|-$/g, "");
    heading.id = id;
    const anchor = document.createElement("a");
    anchor.href = `#/${state.currentNote.slug}#${id}`;
    anchor.className = "heading-anchor";
    anchor.textContent = "#";
    heading.append(anchor);
  });
}

function renderTreeNode(node) {
  if (node.type === "note") {
    const note = state.notesBySlug.get(node.slug);
    const title = note ? sourceTitle(note) : node.title;
    const active = currentSlug() !== "dashboard" && state.currentNote?.slug === node.slug ? " active" : "";
    return `<a class="tree-note${active}" href="#/${node.slug}">${escapeHtml(title)}</a>`;
  }
  const children = node.children.map(renderTreeNode).join("");
  if (node.name === "notes") return children;
  return `<details open><summary>${escapeHtml(folderLabel(node.name))}</summary><div>${children}</div></details>`;
}

function renderTree() {
  const active = currentSlug() === "dashboard" ? " active" : "";
  els.tree.innerHTML = `<a class="tree-note dashboard-link${active}" href="#/dashboard">${escapeHtml(t("dashboard"))}</a>` + renderTreeNode(state.tree);
}

function renderTypeFilters() {
  const counts = new Map();
  for (const note of state.notes) counts.set(note.type, (counts.get(note.type) || 0) + 1);
  els.typeFilters.innerHTML = [...counts.entries()]
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([type, count]) => `<button class="filter-chip" data-filter="${type}" type="button">${typeLabel(type)}<span>${count}</span></button>`)
    .join("");
}

function renderBacklinks(note) {
  if (!note) {
    els.backlinks.innerHTML = `<p class="muted">Dashboard has no backlinks.</p>`;
    return;
  }
  if (!note.backlinks.length) {
    els.backlinks.innerHTML = `<p class="muted">No backlinks yet.</p>`;
    return;
  }
  els.backlinks.innerHTML = note.backlinks
    .map((link) => `<a href="#/${link.slug}">${escapeHtml(sourceTitle(state.notesBySlug.get(link.slug) || link))}</a>`)
    .join("");
}

function renderOutgoing(note) {
  if (!note) {
    els.outgoing.innerHTML = state.dashboard.hub_notes
      .map((item) => `<a href="#/${item.slug}">${escapeHtml(sourceTitle(state.notesBySlug.get(item.slug) || item))}<small>${item.connection_count} ${escapeHtml(t("linksUnit"))}</small></a>`)
      .join("");
    return;
  }
  const links = note.links.filter((link) => link.resolved_slug);
  if (!links.length) {
    els.outgoing.innerHTML = `<p class="muted">${escapeHtml(t("noOutgoing"))}</p>`;
    return;
  }
  els.outgoing.innerHTML = links
    .map((link) => `<a href="#/${link.resolved_slug}">${escapeHtml(sourceTitle(state.notesBySlug.get(link.resolved_slug) || { title: link.resolved_title }))}</a>`)
    .join("");
}

function renderStats() {
  const generated = state.stats.generated_at ? new Date(state.stats.generated_at).toLocaleString() : "unknown";
  const orphanCount = state.report?.orphan_notes?.length ?? 0;
  els.stats.innerHTML = `
    <div class="stat-row"><span>${escapeHtml(t("notes"))}</span><strong>${state.stats.note_count}</strong></div>
    <div class="stat-row"><span>${escapeHtml(t("brokenLinks"))}</span><strong>${state.stats.broken_link_count}</strong></div>
    <div class="stat-row"><span>${escapeHtml(t("orphans"))}</span><strong>${orphanCount}</strong></div>
    <div class="stat-row"><span>${escapeHtml(t("generated"))}</span><strong>${generated}</strong></div>
  `;
}

function renderContextHealth(note = null) {
  const health = state.dashboard?.context_health;
  if (!health) return;
  const noteSignals = note ? [
    [t("backlinks"), note.backlinks.length],
    [t("outgoing"), note.links.filter((link) => link.resolved_slug).length],
    [t("status"), note.status],
  ] : [
    [t("reviewQueue"), health.review_items],
    [t("hubNotes"), state.dashboard.hub_notes.length],
    [t("brokenLinks"), health.broken_links],
  ];
  els.contextHealth.innerHTML = noteSignals
    .map(([label, value]) => `<div class="health-row"><span>${escapeHtml(label)}</span><strong>${escapeHtml(value)}</strong></div>`)
    .join("");
}

function renderMeta(note) {
  const parts = note.path.split("/");
  els.breadcrumbs.innerHTML = parts
    .map((part, index) => `<span>${escapeHtml(part.replace(".md", ""))}</span>${index < parts.length - 1 ? "<b>/</b>" : ""}`)
    .join("");
  els.noteMeta.innerHTML = `
    <span class="type-chip type-${note.type}">${escapeHtml(typeLabel(note.type))}</span>
    <span class="meta-chip">${escapeHtml(note.status)}</span>
    <span class="meta-chip">${escapeHtml(t("updated"))} ${escapeHtml(note.updated || "unknown")}</span>
    <span class="meta-chip">${localizedNote(note).hasTranslation ? state.lang.toUpperCase() : "EN"}</span>
    ${hasDraft(note) ? `<span class="meta-chip draft-chip">${escapeHtml(t("draftSaved"))}</span>` : ""}
  `;
}

function renderOutline(note) {
  const headings = extractHeadings({ ...note, body: localizedBody(note) });
  if (!headings.length) {
    els.outline.innerHTML = `<p class="muted">${escapeHtml(t("noHeadings"))}</p>`;
    return;
  }
  els.outline.innerHTML = headings
    .map((heading) => `<a class="depth-${heading.depth}" href="#/${note.slug}#${heading.id}">${escapeHtml(heading.text)}</a>`)
    .join("");
}

function currentSlug() {
  return location.hash.replace(/^#\/?/, "").split("#")[0] || "dashboard";
}

function dashboardCard(item, extra = "") {
  const note = state.notesBySlug.get(item.slug);
  const title = note ? sourceTitle(note) : item.title;
  const summary = note ? summaryFromMarkdown(note.body) : item.summary;
  return `
    <a class="dashboard-card type-${item.type}" href="#/${item.slug}">
      <span>${escapeHtml(typeLabel(item.type))}</span>
      <strong>${escapeHtml(title)}</strong>
      ${summary ? `<p>${escapeHtml(summary)}</p>` : ""}
      ${extra}
    </a>
  `;
}

function renderDashboard() {
  const overview = state.notesBySlug.get("start/overview") || state.notes[0];
  state.currentNote = overview;
  document.querySelector(".app-shell").classList.add("dashboard-mode");
  syncLanguageControls();
  const health = state.dashboard.context_health;
  const queue = state.dashboard.review_queue.length
    ? state.dashboard.review_queue
    : [{ title: "No review items", type: "project", slug: "start/overview", reasons: ["context is healthy"] }];
  els.editor.classList.add("hidden");
  els.reader.classList.remove("hidden");
  document.querySelector("#edit-toggle").textContent = "Edit";
  els.breadcrumbs.innerHTML = "";
  els.noteMeta.innerHTML = "";
  els.note.innerHTML = `
    <section class="dashboard-shell">
      <div class="dashboard-hero">
        <div>
          <p class="eyebrow">AI Context as Code</p>
          <h1>${escapeHtml(t("dashboard"))}</h1>
          <p>${escapeHtml(t("dashboardSubtitle"))}</p>
        </div>
        <div class="dashboard-status">
          <span>Publish status</span>
          <strong>${health.broken_links === 0 ? "Clean" : `${health.broken_links} ${t("brokenLinks")}`}</strong>
        </div>
      </div>
      <div class="health-grid">
        <div><span>${escapeHtml(t("notes"))}</span><strong>${health.notes}</strong></div>
        <div><span>Review</span><strong>${health.review_items}</strong></div>
        <div><span>${escapeHtml(t("orphans"))}</span><strong>${health.orphans}</strong></div>
        <div><span>${escapeHtml(t("brokenLinks"))}</span><strong>${health.broken_links}</strong></div>
      </div>
    </section>
    <section class="dashboard-layout">
      <div class="dashboard-main">
        <div class="dashboard-heading">
          <div>
            <h2>${escapeHtml(t("reviewQueue"))}</h2>
            <p>${escapeHtml(t("reviewQueueDescription"))}</p>
          </div>
        </div>
        <div class="review-list">
          ${queue.map((item) => `
            <a class="review-item type-${item.type}" href="#/${item.slug}">
              <span>${escapeHtml(typeLabel(item.type))}</span>
              <strong>${escapeHtml(sourceTitle(state.notesBySlug.get(item.slug) || item))}</strong>
              <em>${item.reasons.map(reasonLabel).map(escapeHtml).join(" · ")}</em>
            </a>
          `).join("")}
        </div>
      </div>
      <div class="dashboard-side">
        <section>
          <div class="dashboard-heading compact-heading">
            <div>
              <h2>${escapeHtml(t("recentlyChanged"))}</h2>
              <p>${escapeHtml(t("recentlyChangedDescription"))}</p>
            </div>
          </div>
          <div class="dashboard-cards compact">
            ${state.dashboard.recent_notes.slice(0, 5).map((item) => dashboardCard(item, `<em>${escapeHtml(item.updated || "unknown")}</em>`)).join("")}
          </div>
        </section>
        <section>
          <div class="dashboard-heading compact-heading">
            <div>
              <h2>${escapeHtml(t("hubNotes"))}</h2>
              <p>${escapeHtml(t("hubNotesDescription"))}</p>
            </div>
          </div>
          <div class="dashboard-cards compact">
            ${state.dashboard.hub_notes.slice(0, 5).map((item) => dashboardCard(item, `<em>${item.connection_count} ${escapeHtml(t("linksUnit"))}</em>`)).join("")}
          </div>
        </section>
      </div>
    </section>
    <section class="dashboard-section runtime-strip">
      <div>
        <span>Agent config</span>
        <strong>Use familiar surfaces such as AGENTS.md, CLAUDE.md, skills, memory, and commands.</strong>
      </div>
      <a class="tool-button primary" href="#/projects/agent-runtime-references">Open config plan</a>
    </section>
  `;
  els.outline.innerHTML = "";
  renderBacklinks(null);
  renderOutgoing(null);
  renderContextHealth(null);
  renderTree();
  document.title = `${t("dashboard")} · AI Context as Code`;
}

async function renderNote() {
  if (currentSlug() === "dashboard") {
    renderDashboard();
    return;
  }
  document.querySelector(".app-shell").classList.remove("dashboard-mode");
  syncLanguageControls();
  const note = state.notesBySlug.get(currentSlug()) || state.notesBySlug.get("start/overview");
  state.currentNote = note;
  els.note.innerHTML = renderMarkdown(localizedBody(note));
  addHeadingAnchors(els.note);
  await renderMermaid(els.note);
  renderMeta(note);
  renderBacklinks(note);
  renderOutgoing(note);
  renderContextHealth(note);
  renderOutline(note);
  renderTree();
  renderGraph();
  renderEditorState();
  document.title = `${localizedTitle(note)} · AI Context as Code`;
  requestAnimationFrame(() => {
    const anchor = location.hash.split("#")[2];
    if (anchor) {
      document.getElementById(anchor)?.scrollIntoView({ block: "start" });
      return;
    }
    els.workspace.scrollTo({ top: 0, left: 0, behavior: "auto" });
    window.scrollTo({ top: 0, left: 0, behavior: "auto" });
  });
}
function runSearch(query) {
  const value = query.trim().toLowerCase();
  if (!value) {
    renderTree();
    return;
  }
  const matches = state.notes.filter((note) => {
    const record = state.searchBySlug.get(note.slug);
    const translationText = Object.values(record?.translations || {})
      .map((translation) => `${translation.title || ""} ${translation.text || ""}`)
      .join(" ");
    return `${note.title} ${note.type} ${note.body} ${translationText}`.toLowerCase().includes(value);
  });
  els.tree.innerHTML = matches
    .map((note) => `<a class="tree-note" href="#/${note.slug}"><span>${escapeHtml(sourceTitle(note))}</span><small>${escapeHtml(note.type)}</small></a>`)
    .join("") || `<p class="muted empty">No matches.</p>`;
}

function relatedGraph(note, mode) {
  if (mode === "all") return state.graph;
  const keep = new Set([note.slug]);
  for (const edge of state.graph.edges) {
    if (edge.source === note.slug) keep.add(edge.target);
    if (edge.target === note.slug) keep.add(edge.source);
  }
  return {
    nodes: state.graph.nodes.filter((node) => keep.has(node.id)),
    edges: state.graph.edges.filter((edge) => keep.has(edge.source) && keep.has(edge.target)),
  };
}

function layoutNodes(nodes, width, height) {
  const centerX = width / 2;
  const centerY = height / 2;
  const radius = Math.max(70, Math.min(width, height) * 0.34);
  if (nodes.length === 1) return [{ ...nodes[0], x: centerX, y: centerY }];
  return nodes.map((node, index) => {
    const angle = (Math.PI * 2 * index) / nodes.length - Math.PI / 2;
    const weight = Math.min(28, (node.link_count + node.backlink_count) * 3);
    return {
      ...node,
      x: centerX + Math.cos(angle) * (radius - weight),
      y: centerY + Math.sin(angle) * (radius - weight),
    };
  });
}

function graphSvg(graph, note, compact = false) {
  const width = compact ? 260 : 760;
  const height = compact ? 210 : 340;
  const nodes = layoutNodes(graph.nodes, width, height);
  const byId = new Map(nodes.map((node) => [node.id, node]));
  const edges = graph.edges
    .map((edge) => ({ ...edge, sourceNode: byId.get(edge.source), targetNode: byId.get(edge.target) }))
    .filter((edge) => edge.sourceNode && edge.targetNode);
  const edgeSvg = edges
    .map((edge) => `<line x1="${edge.sourceNode.x}" y1="${edge.sourceNode.y}" x2="${edge.targetNode.x}" y2="${edge.targetNode.y}" />`)
    .join("");
  const nodeSvg = nodes
    .map((node) => {
      const active = node.id === note.slug ? " graph-node-active" : "";
      const r = Math.max(6, Math.min(15, 7 + node.backlink_count));
      return `
        <a href="#/${node.id}" class="graph-node-link">
          <circle class="graph-node type-${node.type}${active}" cx="${node.x}" cy="${node.y}" r="${r}"></circle>
          <text x="${node.x}" y="${node.y + r + 13}">${escapeHtml(sourceTitle(state.notesBySlug.get(node.id) || node).slice(0, compact ? 18 : 28))}</text>
        </a>
      `;
    })
    .join("");
  return `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="Knowledge graph"><g class="graph-edges">${edgeSvg}</g><g>${nodeSvg}</g></svg>`;
}

function graphInsight(label, value, detail = "") {
  return `
    <div class="graph-insight-card">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value)}</strong>
      ${detail ? `<small>${escapeHtml(detail)}</small>` : ""}
    </div>
  `;
}

function noteOutgoingSlugs(note) {
  return new Set((note.links || []).filter((link) => link.resolved_slug).map((link) => link.resolved_slug));
}

function noteBacklinkSlugs(note) {
  return new Set((note.backlinks || []).map((link) => link.slug));
}

function relationReason(source, target) {
  const outgoing = noteOutgoingSlugs(source);
  const targetOutgoing = noteOutgoingSlugs(target);
  const incoming = noteBacklinkSlugs(source);
  const targetTitle = sourceTitle(target);
  if (outgoing.has(target.slug) && targetOutgoing.has(source.slug)) {
    return `Mutual links with ${targetTitle}.`;
  }
  if (outgoing.has(target.slug)) {
    return `This note directly references ${targetTitle}.`;
  }
  if (incoming.has(target.slug)) {
    return `${targetTitle} points back to this note.`;
  }
  const sharedTargets = [...outgoing].filter((slug) => targetOutgoing.has(slug));
  if (sharedTargets.length) {
    const sharedTitle = sourceTitle(state.notesBySlug.get(sharedTargets[0]) || { title: sharedTargets[0] });
    return `Both notes reference ${sharedTitle}.`;
  }
  const degree = (target.link_count || target.links?.filter((link) => link.resolved_slug).length || 0) + (target.backlink_count || target.backlinks?.length || 0);
  return `${targetTitle} is a hub with ${degree} connections.`;
}

function strongestRelatedNote(note, local) {
  const outgoing = noteOutgoingSlugs(note);
  const incoming = noteBacklinkSlugs(note);
  return local.nodes
    .filter((node) => node.id !== note.slug)
    .map((node) => {
      const target = state.notesBySlug.get(node.id) || node;
      let score = (node.link_count || 0) + (node.backlink_count || 0);
      if (outgoing.has(node.id)) score += 20;
      if (incoming.has(node.id)) score += 16;
      return { target, score };
    })
    .sort((a, b) => b.score - a.score)[0]?.target;
}

function renderGraphInsights(note, activeGraph) {
  const local = relatedGraph(note, "local");
  const incoming = note.backlinks || [];
  const outgoing = (note.links || []).filter((link) => link.resolved_slug);
  const strongest = strongestRelatedNote(note, local);
  const hubs = state.dashboard.hub_notes
    .slice(0, 3)
    .map((item) => sourceTitle(state.notesBySlug.get(item.slug) || item))
    .join(", ");
  const review = state.dashboard.review_queue
    .slice(0, 3)
    .map((item) => sourceTitle(state.notesBySlug.get(item.slug) || item))
    .join(", ");
  const activeTitle = sourceTitle(note);
  const connected = local.nodes.length > 1
    ? local.nodes.filter((node) => node.id !== note.slug).map((node) => sourceTitle(state.notesBySlug.get(node.id) || node)).slice(0, 3).join(", ")
    : t("noDirectNeighbors");
  const relatedDetail = strongest ? relationReason(note, strongest) : connected;

  els.graphInsights.innerHTML = [
    graphInsight(t("current"), activeTitle, typeLabel(note.type)),
    graphInsight(t("incoming"), `${incoming.length}`, incoming.slice(0, 2).map((item) => sourceTitle(state.notesBySlug.get(item.slug) || item)).join(", ")),
    graphInsight(t("outgoing"), `${outgoing.length}`, outgoing.slice(0, 2).map((item) => sourceTitle(state.notesBySlug.get(item.resolved_slug) || item)).join(", ")),
    state.graphMode === "all"
      ? graphInsight(t("mapSignal"), `${activeGraph.nodes.length} ${t("notesUnit")}`, hubs || review || "No graph signal yet")
      : graphInsight(t("related"), `${Math.max(0, local.nodes.length - 1)} ${t("notesUnit")}`, relatedDetail),
  ].join("");
}

function renderGraph() {
  const note = state.currentNote;
  const activeGraph = relatedGraph(note, state.graphMode);
  els.globalGraph.innerHTML = graphSvg(activeGraph, note, false);
  els.graphSummary.textContent = `${activeGraph.nodes.length} ${t("notesUnit")} · ${activeGraph.edges.length} ${t("linksUnit")}`;
  renderGraphInsights(note, activeGraph);
  els.graphLocal.classList.toggle("active", state.graphMode === "local");
  els.graphAll.classList.toggle("active", state.graphMode === "all");
}

function renderEditorState() {
  const note = state.currentNote;
  if (!note) return;
  els.editorTitle.textContent = `Edit ${note.title}`;
  const draft = localStorage.getItem(draftKey(note));
  els.editorText.value = draft ?? note.body;
  els.draftStatus.textContent = draft ? "Saved draft loaded from this browser." : t("editorOriginal");
  if (!els.editor.classList.contains("hidden")) updateEditorPreview();
}

async function updateEditorPreview() {
  els.editorPreview.innerHTML = renderMarkdown(els.editorText.value);
  addHeadingAnchors(els.editorPreview);
  await renderMermaid(els.editorPreview);
}

function toggleEditor(force) {
  const shouldShow = force ?? els.editor.classList.contains("hidden");
  els.editor.classList.toggle("hidden", !shouldShow);
  els.reader.classList.toggle("hidden", shouldShow);
  document.querySelector("#edit-toggle").textContent = shouldShow ? "Read" : "Edit";
  if (shouldShow) {
    renderEditorState();
    els.editorText.focus();
  }
}

function saveDraft() {
  localStorage.setItem(draftKey(state.currentNote), els.editorText.value);
  renderMeta(state.currentNote);
  renderEditorState();
}

function discardDraft() {
  localStorage.removeItem(draftKey(state.currentNote));
  renderMeta(state.currentNote);
  renderEditorState();
}

function markdownSections(markdown) {
  const lines = markdown.split("\n");
  const sections = [];
  let current = { heading: "Document start", startLine: 1, lines: [] };
  lines.forEach((line, index) => {
    if (/^#{1,6}\s+/.test(line) && current.lines.length) {
      current.endLine = index;
      sections.push(current);
      current = { heading: line.replace(/^#{1,6}\s+/, "").trim(), startLine: index + 1, lines: [line] };
      return;
    }
    if (/^#{1,6}\s+/.test(line) && !current.lines.length) {
      current.heading = line.replace(/^#{1,6}\s+/, "").trim();
    }
    current.lines.push(line);
  });
  current.endLine = lines.length;
  sections.push(current);
  return sections.map((section, index) => ({
    ...section,
    key: `${section.heading.toLowerCase()}::${index}`,
    text: section.lines.join("\n"),
  }));
}

function changedMarkdownSections(original, updated) {
  const originalSections = markdownSections(original);
  const updatedSections = markdownSections(updated);
  const originalByKey = new Map(originalSections.map((section) => [section.key, section]));
  const updatedByKey = new Map(updatedSections.map((section) => [section.key, section]));
  const keys = [...new Set([...originalByKey.keys(), ...updatedByKey.keys()])];
  return keys
    .map((key) => {
      const before = originalByKey.get(key);
      const after = updatedByKey.get(key);
      if (before?.text === after?.text) return null;
      return {
        heading: after?.heading || before?.heading || "Document start",
        status: before && after ? "changed" : before ? "removed" : "added",
        before,
        after,
      };
    })
    .filter(Boolean);
}

function exportPatch() {
  const note = state.currentNote;
  const original = note.body;
  const updated = els.editorText.value;
  const sectionChanges = changedMarkdownSections(original, updated);
  const patch = [
    `# Patch export for ${note.path}`,
    "",
    "This patch is generated in the browser. Review it locally before committing.",
    "",
    "## Changed Sections",
    "",
    sectionChanges.length
      ? sectionChanges.map((change) => `- ${change.status}: ${change.heading}`).join("\n")
      : "- No section changes detected.",
    "",
    "## Section Review",
    "",
    ...sectionChanges.flatMap((change) => [
      `### ${change.status}: ${change.heading}`,
      "",
      change.before ? `Original lines ${change.before.startLine}-${change.before.endLine}` : "Original: not present",
      change.after ? `Updated lines ${change.after.startLine}-${change.after.endLine}` : "Updated: removed",
      "",
      "```markdown",
      change.after?.text || "",
      "```",
      "",
    ]),
    "## Full File Diff",
    "",
    "```diff",
    `--- a/notes/${note.path}`,
    `+++ b/notes/${note.path}`,
    "@@",
    ...original.split("\n").map((line) => `-${line}`),
    ...updated.split("\n").map((line) => `+${line}`),
    "```",
    "",
  ].join("\n");
  const blob = new Blob([patch], { type: "text/markdown;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  els.downloadLink.href = url;
  els.downloadLink.download = `${note.slug.split("/").pop()}-patch.md`;
  els.downloadLink.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function openCommandPalette(initialQuery = "") {
  els.commandPalette.classList.remove("hidden");
  els.commandInput.value = initialQuery;
  commandSelectionIndex = 0;
  renderCommandResults(initialQuery);
  els.commandInput.focus();
}

function closeCommandPalette() {
  els.commandPalette.classList.add("hidden");
  els.search.value = "";
}

function commandText(command) {
  return command.title;
}

function snippetFor(note, query) {
  const record = state.searchBySlug.get(note.slug);
  const indexedSummary = record?.translations?.[state.lang]?.summary || record?.summary;
  const translatedBodies = Object.values(record?.translations || {}).map((translation) => translation.text || "");
  const candidates = [localizedBody(note), note.body, ...translatedBodies, indexedSummary].filter(Boolean);
  const matchCandidate = query
    ? candidates.find((candidate) => candidate.toLowerCase().includes(query.toLowerCase()))
    : candidates[0];
  const body = (matchCandidate || "").replace(/^# .*\n?/, "").replace(/\s+/g, " ").trim();
  if (!query) return summaryFromMarkdown(localizedBody(note), 110);
  const index = body.toLowerCase().indexOf(query.toLowerCase());
  if (index < 0) return summaryFromMarkdown(localizedBody(note), 110);
  const start = Math.max(0, index - 42);
  const end = Math.min(body.length, index + query.length + 82);
  return `${start > 0 ? "..." : ""}${body.slice(start, end)}${end < body.length ? "..." : ""}`;
}

function daysSince(dateValue) {
  const time = Date.parse(dateValue || "");
  if (Number.isNaN(time)) return 999;
  return Math.max(0, Math.floor((Date.now() - time) / 86400000));
}

function noteSearchScore(note, query) {
  const record = state.searchBySlug.get(note.slug);
  const indexedTranslations = Object.values(record?.translations || {});
  const translatedTitles = indexedTranslations.map((translation) => translation.title || "").join(" ");
  const translatedText = indexedTranslations.map((translation) => translation.text || "").join(" ");
  const title = `${record?.title || ""} ${translatedTitles} ${note.title}`.toLowerCase();
  const slug = `${note.slug} ${record?.path || ""}`.toLowerCase();
  const type = `${note.type} ${record?.type || ""}`.toLowerCase();
  const headings = (record?.headings || []).join(" ").toLowerCase();
  const body = `${record?.text || ""} ${translatedText} ${note.body}`.toLowerCase();
  const q = query.toLowerCase();
  const terms = q.split(/\s+/).filter(Boolean);
  let score = 0;
  if (!q) score += 12;
  if (title === q) score += 320;
  if (title.startsWith(q)) score += 240;
  if (title.includes(q)) score += 160;
  if (slug.includes(q)) score += 80;
  if (type.includes(q)) score += 48;
  if (headings.includes(q)) score += 42;
  if (body.includes(q)) score += 28;
  for (const term of terms) {
    if (title.includes(term)) score += 36;
    if (slug.includes(term)) score += 18;
    if (headings.includes(term)) score += 14;
    if (body.includes(term)) score += 8;
  }
  score += Math.min(32, (record?.backlink_count ?? note.backlinks?.length ?? 0) * 4);
  score += Math.min(12, (record?.link_count ?? 0) * 2);
  score += Math.max(0, 24 - daysSince(note.updated));
  if (state.dashboard.review_queue.some((item) => item.slug === note.slug)) score += 20;
  return score;
}

function defaultSearchNotes() {
  const ordered = [
    ...state.dashboard.review_queue.map((item) => item.slug),
    ...state.dashboard.recent_notes.map((item) => item.slug),
    ...state.dashboard.hub_notes.map((item) => item.slug),
  ];
  const seen = new Set();
  return ordered
    .map((slug) => state.notesBySlug.get(slug))
    .filter((note) => note && !seen.has(note.slug) && seen.add(note.slug))
    .slice(0, 8);
}

function renderCommandResults(query) {
  const value = query.trim().toLowerCase();
  const commands = [
    { title: "Open dashboard", action: () => { location.hash = "#/dashboard"; } },
    { title: "Toggle editor", action: () => toggleEditor() },
    { title: "Toggle theme", action: () => toggleTheme() },
    { title: "Show full context map", action: () => { state.graphMode = "all"; renderGraph(); } },
  ];
  const notePool = value
    ? state.notes
        .map((note) => ({ note, score: noteSearchScore(note, value) }))
        .filter((item) => item.score > 0)
        .sort((a, b) => b.score - a.score)
        .map((item) => item.note)
    : defaultSearchNotes();
  const noteResults = notePool
    .slice(0, 8)
    .map((note) => ({
      kind: "note",
      title: sourceTitle(note),
      subtitle: `${typeLabel(note.type)} · ${note.path}`,
      detail: snippetFor(note, value),
      action: () => { location.hash = `#/${note.slug}`; },
    }));
  const commandResults = commands
    .filter((command) => !value || `${command.title} ${commandText(command)}`.toLowerCase().includes(value))
    .map((command) => ({ ...command, kind: "command", title: commandText(command), subtitle: t("command") }));
  commandItems = [...commandResults, ...noteResults].slice(0, 10);
  commandSelectionIndex = Math.min(commandSelectionIndex, Math.max(0, commandItems.length - 1));
  if (!commandItems.length) {
    els.commandResults.innerHTML = `<div class="command-empty">${escapeHtml(t("noSearchResults"))}</div>`;
    return;
  }
  const grouped = [
    [t("commands"), commandItems.filter((item) => item.kind === "command")],
    [t("notesGroup"), commandItems.filter((item) => item.kind === "note")],
  ].filter(([, items]) => items.length);
  let visibleIndex = 0;
  els.commandResults.innerHTML = grouped
    .map(([label, items]) => `
      <div class="command-group">${escapeHtml(label)}</div>
      ${items.map((item) => {
        const index = visibleIndex++;
        return `
          <button class="${index === commandSelectionIndex ? "active" : ""}" type="button" data-command-index="${index}">
            <span>
              <strong>${escapeHtml(item.title)}</strong>
              <small>${escapeHtml(item.subtitle)}</small>
            </span>
            ${item.kind === "command" ? '<kbd class="command-kbd">Run</kbd>' : ""}
            ${item.detail ? `<p>${escapeHtml(item.detail)}</p>` : ""}
          </button>
        `;
      }).join("")}
    `)
    .join("");
  els.commandResults.querySelectorAll("button").forEach((button, index) => {
    button.addEventListener("click", () => {
      commandItems[index].action();
      closeCommandPalette();
    });
  });
  els.commandResults.querySelector("button.active")?.scrollIntoView({ block: "nearest" });
}

function moveCommandSelection(delta) {
  if (!commandItems.length) return;
  commandSelectionIndex = (commandSelectionIndex + delta + commandItems.length) % commandItems.length;
  renderCommandResults(els.commandInput.value);
}

function runSelectedCommand() {
  const item = commandItems[commandSelectionIndex];
  if (!item) return;
  item.action();
  closeCommandPalette();
}

function toggleTheme() {
  state.theme = state.theme === "dark" ? "light" : "dark";
  localStorage.setItem("acc-theme", state.theme);
  document.documentElement.dataset.theme = state.theme;
  renderNote();
}

function setLanguage(lang) {
  state.lang = normalizeLang(lang);
  localStorage.setItem("acc-note-lang", state.lang);
  els.search.placeholder = t("searchNotes");
  els.commandInput.placeholder = t("searchPrompt");
  syncLanguageControls();
  renderNote();
}

function showHoverPreview(event) {
  if (!finePointerQuery.matches) return;
  const link = event.target.closest("[data-preview]");
  if (!link) return;
  const note = state.notesBySlug.get(link.dataset.preview);
  if (!note) return;
  const rect = link.getBoundingClientRect();
  els.hoverPreview.innerHTML = `
    <strong>${escapeHtml(localizedTitle(note))}</strong>
    <span>${escapeHtml(typeLabel(note.type))} · ${escapeHtml(note.updated || "unknown")}</span>
    <p>${escapeHtml(localizedBody(note).replace(/^# .*\n?/, "").trim().slice(0, 220))}</p>
  `;
  els.hoverPreview.style.left = `${Math.min(rect.left, window.innerWidth - 340)}px`;
  els.hoverPreview.style.top = `${rect.bottom + 10}px`;
  els.hoverPreview.classList.remove("hidden");
}

function hideHoverPreview() {
  els.hoverPreview.classList.add("hidden");
}

async function navigateHash() {
  hideHoverPreview();
  els.sidebar.classList.remove("open");
  await renderNote();
}

async function init() {
  document.documentElement.dataset.theme = state.theme;
  document.documentElement.lang = activeContentLang();
  const [notes, tree, stats, graph, report, dashboard, searchIndex] = await Promise.all([
    loadJson("./_build/notes.json"),
    loadJson("./_build/tree.json"),
    loadJson("./_build/stats.json"),
    loadJson("./_build/graph.json"),
    loadJson("./_build/report.json"),
    loadJson("./_build/dashboard.json"),
    loadJson("./_build/search-index.json"),
  ]);

  state.notes = notes;
  state.tree = tree;
  state.stats = stats;
  state.graph = graph;
  state.report = report;
  state.dashboard = dashboard;
  state.searchIndex = searchIndex;
  state.searchBySlug = new Map(searchIndex.map((item) => [item.slug, item]));
  for (const note of notes) {
    state.notesBySlug.set(note.slug, note);
    state.notesBySlug.set(note.slug.split("/").pop(), note);
  }

  renderTypeFilters();
  renderStats();
  els.search.placeholder = t("searchNotes");
  els.commandInput.placeholder = t("searchPrompt");
  syncLanguageControls();
  await renderNote();
}

els.search.addEventListener("focus", () => openCommandPalette(els.search.value));
els.search.addEventListener("click", () => openCommandPalette(els.search.value));
els.search.addEventListener("input", (event) => openCommandPalette(event.target.value));
els.graphLocal.addEventListener("click", () => { state.graphMode = "local"; renderGraph(); });
els.graphAll.addEventListener("click", () => { state.graphMode = "all"; renderGraph(); });
document.querySelector("#edit-toggle").addEventListener("click", () => toggleEditor());
document.querySelector("#theme-toggle").addEventListener("click", toggleTheme);
els.langKo.addEventListener("click", () => setLanguage("ko"));
els.langEn.addEventListener("click", () => setLanguage("en"));
document.querySelector("#command-open").addEventListener("click", () => openCommandPalette());
document.querySelector("#nav-toggle").addEventListener("click", () => els.sidebar.classList.toggle("open"));
document.querySelector("#save-draft").addEventListener("click", saveDraft);
document.querySelector("#discard-draft").addEventListener("click", discardDraft);
document.querySelector("#export-patch").addEventListener("click", exportPatch);
els.editorText.addEventListener("input", () => {
  els.draftStatus.textContent = "Unsaved browser draft.";
  updateEditorPreview();
});
els.commandInput.addEventListener("input", (event) => {
  commandSelectionIndex = 0;
  renderCommandResults(event.target.value);
});
els.commandInput.addEventListener("keydown", (event) => {
  if (event.key === "ArrowDown") {
    event.preventDefault();
    moveCommandSelection(1);
  }
  if (event.key === "ArrowUp") {
    event.preventDefault();
    moveCommandSelection(-1);
  }
  if (event.key === "Enter") {
    event.preventDefault();
    runSelectedCommand();
  }
});
els.commandPalette.addEventListener("click", (event) => {
  if (event.target === els.commandPalette) closeCommandPalette();
});
els.typeFilters.addEventListener("click", (event) => {
  const button = event.target.closest("[data-filter]");
  if (!button) return;
  runSearch(button.dataset.filter);
  els.search.value = button.dataset.filter;
});
document.body.addEventListener("pointerover", showHoverPreview);
document.body.addEventListener("pointerout", (event) => {
  if (!event.relatedTarget || !event.relatedTarget.closest("[data-preview]")) hideHoverPreview();
});
document.body.addEventListener("pointerdown", hideHoverPreview);
window.addEventListener("scroll", hideHoverPreview, { passive: true });
window.addEventListener("hashchange", navigateHash);
window.addEventListener("keydown", (event) => {
  if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
    event.preventDefault();
    openCommandPalette();
  }
  if (event.key === "Escape") closeCommandPalette();
});

init().catch((error) => {
  els.note.innerHTML = `<p class="error">${escapeHtml(error.message)}</p>`;
});
