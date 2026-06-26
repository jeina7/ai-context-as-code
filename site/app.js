const state = {
  notes: [],
  notesBySlug: new Map(),
  tree: null,
  stats: null,
};

const noteEl = document.querySelector("#note");
const treeEl = document.querySelector("#tree");
const searchEl = document.querySelector("#search");
const backlinksEl = document.querySelector("#backlinks");
const statsEl = document.querySelector("#stats");

async function loadJson(path) {
  const response = await fetch(path);
  if (!response.ok) throw new Error(`Failed to load ${path}`);
  return response.json();
}

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function renderMarkdown(markdown) {
  const lines = escapeHtml(markdown).split("\n");
  const html = [];
  let inList = false;

  for (const rawLine of lines) {
    const line = rawLine.trimEnd();
    if (!line.trim()) {
      if (inList) {
        html.push("</ul>");
        inList = false;
      }
      continue;
    }

    const withLinks = line.replace(/\[\[([^\]]+)\]\]/g, (_match, rawTarget) => {
      const [target, label] = rawTarget.split("|");
      const slug = target.replace(/\.md$/, "");
      const resolved = state.notesBySlug.get(slug) || state.notesBySlug.get(slug.split("/").pop());
      const text = label || target;
      if (!resolved) return `<span class="broken-link">${text}</span>`;
      return `<a href="#/${resolved.slug}">${text}</a>`;
    });

    if (withLinks.startsWith("# ")) {
      if (inList) {
        html.push("</ul>");
        inList = false;
      }
      html.push(`<h1>${withLinks.slice(2)}</h1>`);
    } else if (withLinks.startsWith("## ")) {
      if (inList) {
        html.push("</ul>");
        inList = false;
      }
      html.push(`<h2>${withLinks.slice(3)}</h2>`);
    } else if (withLinks.startsWith("- ")) {
      if (!inList) {
        html.push("<ul>");
        inList = true;
      }
      html.push(`<li>${withLinks.slice(2)}</li>`);
    } else {
      if (inList) {
        html.push("</ul>");
        inList = false;
      }
      html.push(`<p>${withLinks}</p>`);
    }
  }

  if (inList) html.push("</ul>");
  return html.join("\n");
}

function renderTreeNode(node) {
  if (node.type === "note") {
    return `<a class="tree-note" href="#/${node.slug}">${node.title}</a>`;
  }
  const children = node.children.map(renderTreeNode).join("");
  if (node.name === "notes") return children;
  return `<details open><summary>${node.name}</summary><div>${children}</div></details>`;
}

function renderTree() {
  treeEl.innerHTML = renderTreeNode(state.tree);
}

function renderBacklinks(note) {
  if (!note.backlinks.length) {
    backlinksEl.innerHTML = `<p class="muted">No backlinks yet.</p>`;
    return;
  }
  backlinksEl.innerHTML = note.backlinks
    .map((link) => `<a href="#/${link.slug}">${link.title}</a>`)
    .join("");
}

function renderStats() {
  statsEl.innerHTML = `
    <p>${state.stats.note_count} notes</p>
    <p>${state.stats.broken_link_count} broken links</p>
  `;
}

function currentSlug() {
  return location.hash.replace(/^#\/?/, "") || "index";
}

function renderNote() {
  const note = state.notesBySlug.get(currentSlug()) || state.notesBySlug.get("index");
  noteEl.innerHTML = renderMarkdown(note.body);
  renderBacklinks(note);
  document.title = `${note.title} · AI Context as Code`;
}

function runSearch(query) {
  const value = query.trim().toLowerCase();
  if (!value) {
    renderTree();
    return;
  }
  const matches = state.notes.filter((note) => {
    return `${note.title} ${note.body}`.toLowerCase().includes(value);
  });
  treeEl.innerHTML = matches
    .map((note) => `<a class="tree-note" href="#/${note.slug}">${note.title}</a>`)
    .join("") || `<p class="muted">No matches.</p>`;
}

async function init() {
  const [notes, tree, stats] = await Promise.all([
    loadJson("./_build/notes.json"),
    loadJson("./_build/tree.json"),
    loadJson("./_build/stats.json"),
  ]);

  state.notes = notes;
  state.tree = tree;
  state.stats = stats;
  for (const note of notes) {
    state.notesBySlug.set(note.slug, note);
    state.notesBySlug.set(note.slug.split("/").pop(), note);
  }

  renderTree();
  renderStats();
  renderNote();
}

searchEl.addEventListener("input", (event) => runSearch(event.target.value));
window.addEventListener("hashchange", renderNote);

init().catch((error) => {
  noteEl.innerHTML = `<p class="error">${error.message}</p>`;
});

