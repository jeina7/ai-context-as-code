const state = {
  notes: [],
  notesBySlug: new Map(),
  tree: null,
  stats: null,
  graph: { nodes: [], edges: [] },
  report: null,
  currentNote: null,
  graphMode: "local",
  theme: localStorage.getItem("acc-theme") || "light",
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
  stats: document.querySelector("#stats"),
  breadcrumbs: document.querySelector("#breadcrumbs"),
  noteMeta: document.querySelector("#note-meta"),
  outline: document.querySelector("#outline"),
  localGraph: document.querySelector("#local-graph"),
  globalGraph: document.querySelector("#global-graph"),
  graphSummary: document.querySelector("#graph-summary"),
  graphLocal: document.querySelector("#graph-local"),
  graphAll: document.querySelector("#graph-all"),
  typeFilters: document.querySelector("#type-filters"),
  commandPalette: document.querySelector("#command-palette"),
  commandInput: document.querySelector("#command-input"),
  commandResults: document.querySelector("#command-results"),
  hoverPreview: document.querySelector("#hover-preview"),
  sidebar: document.querySelector("#sidebar"),
  downloadLink: document.querySelector("#download-link"),
};

const typeLabels = {
  principle: "Principle",
  pattern: "Pattern",
  research: "Research",
  decision: "Decision",
  project: "Project",
  worklog: "Worklog",
  reference: "Reference",
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
    const active = state.currentNote?.slug === node.slug ? " active" : "";
    return `<a class="tree-note${active}" href="#/${node.slug}">${escapeHtml(node.title)}</a>`;
  }
  const children = node.children.map(renderTreeNode).join("");
  if (node.name === "notes") return children;
  return `<details open><summary>${escapeHtml(node.name)}</summary><div>${children}</div></details>`;
}

function renderTree() {
  els.tree.innerHTML = renderTreeNode(state.tree);
}

function renderTypeFilters() {
  const counts = new Map();
  for (const note of state.notes) counts.set(note.type, (counts.get(note.type) || 0) + 1);
  els.typeFilters.innerHTML = [...counts.entries()]
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([type, count]) => `<button class="filter-chip" data-filter="${type}" type="button">${typeLabels[type] || type}<span>${count}</span></button>`)
    .join("");
}

function renderBacklinks(note) {
  if (!note.backlinks.length) {
    els.backlinks.innerHTML = `<p class="muted">No backlinks yet.</p>`;
    return;
  }
  els.backlinks.innerHTML = note.backlinks
    .map((link) => `<a href="#/${link.slug}">${escapeHtml(link.title)}</a>`)
    .join("");
}

function renderStats() {
  const generated = state.stats.generated_at ? new Date(state.stats.generated_at).toLocaleString() : "unknown";
  const orphanCount = state.report?.orphan_notes?.length ?? 0;
  els.stats.innerHTML = `
    <div class="stat-row"><span>Notes</span><strong>${state.stats.note_count}</strong></div>
    <div class="stat-row"><span>Broken links</span><strong>${state.stats.broken_link_count}</strong></div>
    <div class="stat-row"><span>Orphans</span><strong>${orphanCount}</strong></div>
    <div class="stat-row"><span>Generated</span><strong>${generated}</strong></div>
  `;
}

function renderMeta(note) {
  const parts = note.path.split("/");
  els.breadcrumbs.innerHTML = parts
    .map((part, index) => `<span>${escapeHtml(part.replace(".md", ""))}</span>${index < parts.length - 1 ? "<b>/</b>" : ""}`)
    .join("");
  els.noteMeta.innerHTML = `
    <span class="type-chip type-${note.type}">${escapeHtml(typeLabels[note.type] || note.type)}</span>
    <span class="meta-chip">${escapeHtml(note.status)}</span>
    <span class="meta-chip">Updated ${escapeHtml(note.updated || "unknown")}</span>
    ${hasDraft(note) ? '<span class="meta-chip draft-chip">Draft saved</span>' : ""}
  `;
}

function renderOutline(note) {
  const headings = extractHeadings(note);
  if (!headings.length) {
    els.outline.innerHTML = `<p class="muted">No headings.</p>`;
    return;
  }
  els.outline.innerHTML = headings
    .map((heading) => `<a class="depth-${heading.depth}" href="#/${note.slug}#${heading.id}">${escapeHtml(heading.text)}</a>`)
    .join("");
}

function currentSlug() {
  return location.hash.replace(/^#\/?/, "").split("#")[0] || "index";
}

async function renderNote() {
  const note = state.notesBySlug.get(currentSlug()) || state.notesBySlug.get("index");
  state.currentNote = note;
  els.note.innerHTML = renderMarkdown(note.body);
  addHeadingAnchors(els.note);
  await renderMermaid(els.note);
  renderMeta(note);
  renderBacklinks(note);
  renderOutline(note);
  renderTree();
  renderGraph();
  renderEditorState();
  document.title = `${note.title} · AI Context as Code`;
  requestAnimationFrame(() => {
    const anchor = location.hash.split("#")[2];
    if (anchor) document.getElementById(anchor)?.scrollIntoView({ block: "start" });
  });
}

function runSearch(query) {
  const value = query.trim().toLowerCase();
  if (!value) {
    renderTree();
    return;
  }
  const matches = state.notes.filter((note) => `${note.title} ${note.type} ${note.body}`.toLowerCase().includes(value));
  els.tree.innerHTML = matches
    .map((note) => `<a class="tree-note" href="#/${note.slug}"><span>${escapeHtml(note.title)}</span><small>${escapeHtml(note.type)}</small></a>`)
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
          <text x="${node.x}" y="${node.y + r + 13}">${escapeHtml(node.title.slice(0, compact ? 18 : 28))}</text>
        </a>
      `;
    })
    .join("");
  return `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="Knowledge graph"><g class="graph-edges">${edgeSvg}</g><g>${nodeSvg}</g></svg>`;
}

function renderGraph() {
  const note = state.currentNote;
  const local = relatedGraph(note, "local");
  els.localGraph.innerHTML = graphSvg(local, note, true);
  const activeGraph = relatedGraph(note, state.graphMode);
  els.globalGraph.innerHTML = graphSvg(activeGraph, note, false);
  els.graphSummary.textContent = `${activeGraph.nodes.length} nodes · ${activeGraph.edges.length} links`;
  els.graphLocal.classList.toggle("active", state.graphMode === "local");
  els.graphAll.classList.toggle("active", state.graphMode === "all");
}

function renderEditorState() {
  const note = state.currentNote;
  els.editorTitle.textContent = `Edit ${note.title}`;
  const draft = localStorage.getItem(draftKey(note));
  els.editorText.value = draft ?? note.body;
  els.draftStatus.textContent = draft ? "Saved draft loaded from this browser." : "Drafts stay in this browser until exported.";
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

function exportPatch() {
  const note = state.currentNote;
  const original = note.body;
  const updated = els.editorText.value;
  const patch = [
    `# Patch export for ${note.path}`,
    "",
    "This patch is generated in the browser. Review it locally before committing.",
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

function openCommandPalette() {
  els.commandPalette.classList.remove("hidden");
  els.commandInput.value = "";
  renderCommandResults("");
  els.commandInput.focus();
}

function closeCommandPalette() {
  els.commandPalette.classList.add("hidden");
}

function renderCommandResults(query) {
  const value = query.trim().toLowerCase();
  const commands = [
    { title: "Toggle editor", action: () => toggleEditor() },
    { title: "Toggle theme", action: () => toggleTheme() },
    { title: "Show full graph", action: () => { state.graphMode = "all"; renderGraph(); } },
  ];
  const noteResults = state.notes
    .filter((note) => !value || `${note.title} ${note.type} ${note.body}`.toLowerCase().includes(value))
    .slice(0, 8)
    .map((note) => ({ title: note.title, subtitle: note.path, action: () => { location.hash = `#/${note.slug}`; } }));
  const commandResults = commands
    .filter((command) => !value || command.title.toLowerCase().includes(value))
    .map((command) => ({ ...command, subtitle: "Command" }));
  const results = [...commandResults, ...noteResults].slice(0, 10);
  els.commandResults.innerHTML = results
    .map((item, index) => `<button type="button" data-command-index="${index}"><span>${escapeHtml(item.title)}</span><small>${escapeHtml(item.subtitle)}</small></button>`)
    .join("");
  els.commandResults.querySelectorAll("button").forEach((button, index) => {
    button.addEventListener("click", () => {
      results[index].action();
      closeCommandPalette();
    });
  });
}

function toggleTheme() {
  state.theme = state.theme === "dark" ? "light" : "dark";
  localStorage.setItem("acc-theme", state.theme);
  document.documentElement.dataset.theme = state.theme;
  renderNote();
}

function showHoverPreview(event) {
  const link = event.target.closest("[data-preview]");
  if (!link) return;
  const note = state.notesBySlug.get(link.dataset.preview);
  if (!note) return;
  const rect = link.getBoundingClientRect();
  els.hoverPreview.innerHTML = `
    <strong>${escapeHtml(note.title)}</strong>
    <span>${escapeHtml(note.type)} · ${escapeHtml(note.updated || "unknown")}</span>
    <p>${escapeHtml(note.body.replace(/^# .*\n?/, "").trim().slice(0, 220))}</p>
  `;
  els.hoverPreview.style.left = `${Math.min(rect.left, window.innerWidth - 340)}px`;
  els.hoverPreview.style.top = `${rect.bottom + 10}px`;
  els.hoverPreview.classList.remove("hidden");
}

function hideHoverPreview() {
  els.hoverPreview.classList.add("hidden");
}

async function init() {
  document.documentElement.dataset.theme = state.theme;
  const [notes, tree, stats, graph, report] = await Promise.all([
    loadJson("./_build/notes.json"),
    loadJson("./_build/tree.json"),
    loadJson("./_build/stats.json"),
    loadJson("./_build/graph.json"),
    loadJson("./_build/report.json"),
  ]);

  state.notes = notes;
  state.tree = tree;
  state.stats = stats;
  state.graph = graph;
  state.report = report;
  for (const note of notes) {
    state.notesBySlug.set(note.slug, note);
    state.notesBySlug.set(note.slug.split("/").pop(), note);
  }

  renderTypeFilters();
  renderStats();
  await renderNote();
}

els.search.addEventListener("input", (event) => runSearch(event.target.value));
els.graphLocal.addEventListener("click", () => { state.graphMode = "local"; renderGraph(); });
els.graphAll.addEventListener("click", () => { state.graphMode = "all"; renderGraph(); });
document.querySelector("#edit-toggle").addEventListener("click", () => toggleEditor());
document.querySelector("#theme-toggle").addEventListener("click", toggleTheme);
document.querySelector("#command-open").addEventListener("click", openCommandPalette);
document.querySelector("#nav-toggle").addEventListener("click", () => els.sidebar.classList.toggle("open"));
document.querySelector("#save-draft").addEventListener("click", saveDraft);
document.querySelector("#discard-draft").addEventListener("click", discardDraft);
document.querySelector("#export-patch").addEventListener("click", exportPatch);
els.editorText.addEventListener("input", () => {
  els.draftStatus.textContent = "Unsaved browser draft.";
  updateEditorPreview();
});
els.commandInput.addEventListener("input", (event) => renderCommandResults(event.target.value));
els.commandPalette.addEventListener("click", (event) => {
  if (event.target === els.commandPalette) closeCommandPalette();
});
els.typeFilters.addEventListener("click", (event) => {
  const button = event.target.closest("[data-filter]");
  if (!button) return;
  runSearch(button.dataset.filter);
  els.search.value = button.dataset.filter;
});
document.body.addEventListener("mouseover", showHoverPreview);
document.body.addEventListener("mouseout", hideHoverPreview);
window.addEventListener("hashchange", () => {
  els.sidebar.classList.remove("open");
  renderNote();
});
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
