const state = {
  notes: [],
  notesById: new Map(),
  linkLookup: new Map(),
  tree: null,
  home: null,
  backlinks: {},
  build: null,
  searchIndex: [],
};

const main = document.querySelector("#main");
const contextPanel = document.querySelector("#context");
const treeRoot = document.querySelector("#tree");
const searchForm = document.querySelector(".search-form");
const searchInput = document.querySelector("#global-search");

async function fetchJson(path) {
  const response = await fetch(path);
  if (!response.ok) {
    throw new Error(`Could not load ${path}`);
  }
  return response.json();
}

async function init() {
  try {
    const [notes, tree, home, backlinks, build, searchIndex] = await Promise.all([
      fetchJson("/data/notes.json"),
      fetchJson("/data/tree.json"),
      fetchJson("/data/home.json"),
      fetchJson("/data/backlinks.json"),
      fetchJson("/data/build.json"),
      fetchJson("/data/search-index.json"),
    ]);

    state.notes = notes;
    state.tree = tree;
    state.home = home;
    state.backlinks = backlinks;
    state.build = build;
    state.searchIndex = searchIndex;
    state.notesById = new Map(notes.map((note) => [note.id, note]));
    state.linkLookup = buildLinkLookup(notes);

    renderTree();
    await renderRoute();
  } catch (error) {
    renderFatalError(error);
  }
}

function buildLinkLookup(notes) {
  const lookup = new Map();
  for (const note of notes) {
    const pathNoExt = note.path.replace(/\.md$/, "");
    const filename = note.path.split("/").pop().replace(/\.md$/, "");
    lookup.set(note.title, note.id);
    lookup.set(note.path, note.id);
    lookup.set(pathNoExt, note.id);
    lookup.set(filename, note.id);
  }
  return lookup;
}

function navigate(path) {
  if (path === window.location.pathname + window.location.search) return;
  window.history.pushState({}, "", path);
  document.body.classList.remove("nav-open");
  renderRoute();
}

async function renderRoute() {
  const { pathname, search } = window.location;
  setSearchValue(new URLSearchParams(search).get("q") || "");

  if (pathname === "/") {
    renderHome();
    return;
  }

  if (pathname === "/search") {
    renderSearch();
    return;
  }

  if (pathname.startsWith("/trove/")) {
    const id = decodeURIComponent(pathname.replace("/trove/", ""));
    await renderNote(id);
    return;
  }

  renderMissing("Route not found", pathname);
}

function setSearchValue(value) {
  if (searchInput && searchInput.value !== value) {
    searchInput.value = value;
  }
}

function renderTree() {
  if (!state.tree) return;
  const mainNodes = state.tree.nodes?.main || [];
  const specialNodes = state.tree.nodes?.special || [];
  treeRoot.innerHTML = `
    <section class="tree-section">
      <h2 class="tree-section-title">Main context</h2>
      ${renderTreeList(mainNodes)}
    </section>
    <div class="tree-divider" aria-hidden="true"></div>
    <section class="tree-section">
      <h2 class="tree-section-title">Special contents</h2>
      ${renderTreeList(specialNodes)}
    </section>
  `;
}

function renderTreeList(nodes) {
  if (!nodes.length) return '<p class="muted">No documents yet.</p>';
  return `<ul class="tree-list">${nodes.map(renderTreeNode).join("")}</ul>`;
}

function renderTreeNode(node) {
  const currentPath = window.location.pathname;
  const active = node.route && currentPath === node.route ? " active" : "";
  const children = node.children?.length ? renderTreeList(node.children) : "";

  if (node.kind === "note") {
    return `
      <li class="tree-item">
        <a class="tree-link${active}" href="${node.route}" data-route="${node.route}">
          <span class="tree-token">${escapeHtml(node.type || "note")}</span>
          <span>${escapeHtml(node.title)}</span>
        </a>
      </li>
    `;
  }

  const label = node.route
    ? `<a class="tree-link${active}" href="${node.route}" data-route="${node.route}">
        <span class="tree-token">dir</span><span>${escapeHtml(node.name)}</span>
      </a>`
    : `<div class="tree-folder"><span class="tree-token">dir</span><span>${escapeHtml(node.name)}</span></div>`;

  return `<li class="tree-item">${label}${children}</li>`;
}

function renderHome() {
  const startHere = state.home.startHere || [];
  const specialContents = state.home.specialContents || [];
  const build = state.build || {};

  main.innerHTML = `
    <div class="reader-inner">
      <div class="breadcrumb"><span>trove</span><span>home</span></div>
      <h1 class="home-title">${escapeHtml(state.home.title)}</h1>
      <p class="home-copy">${escapeHtml(state.home.description)}</p>
      <div class="home-grid">
        <section class="panel">
          <h2>Start here</h2>
          ${renderDocList(startHere)}
        </section>
        <section class="panel">
          <h2>Current project</h2>
          ${state.home.currentProject ? renderDocList([state.home.currentProject]) : '<p class="muted">No project index yet.</p>'}
        </section>
        <section class="panel">
          <h2>Today</h2>
          ${state.home.today ? renderDocList([state.home.today]) : '<p class="muted">No daily note yet.</p>'}
        </section>
        <section class="panel">
          <h2>Special contents</h2>
          ${renderDocList(specialContents)}
        </section>
      </div>
      <article class="document">
        ${renderMarkdown(state.home.readme || "", null)}
      </article>
    </div>
  `;

  contextPanel.innerHTML = `
    <section class="context-section">
      <h2>Build</h2>
      <div class="status-row">
        <span class="pill">${escapeHtml(String(build.publicNotes || 0))} public notes</span>
        <span class="pill${build.warnings ? " warning" : ""}">${escapeHtml(String(build.warnings || 0))} warnings</span>
        <span class="pill">analytics ${build.analytics?.enabled ? "enabled" : "disabled"}</span>
      </div>
      <p class="context-meta">${escapeHtml(build.builtAt || "Not built yet")}</p>
    </section>
    <section class="context-section">
      <h2>Structure</h2>
      <ul class="context-list">
        <li><strong>Daily/</strong><div class="context-meta">Day-level context and worklog pointers.</div></li>
        <li><strong>Projects/</strong><div class="context-meta">Project decisions, designs, references, research, and worklogs.</div></li>
        <li><strong>_config/</strong><div class="context-meta">Agent-facing memory, skills, commands, and entry sources.</div></li>
      </ul>
    </section>
  `;
  focusMain();
}

async function renderNote(id) {
  const note = state.notesById.get(id);
  if (!note) {
    renderMissing("Document not found", `/trove/${id}`);
    return;
  }

  main.innerHTML = '<section class="loading-state"><p>Loading note...</p></section>';
  try {
    const response = await fetch(`/content/trove/${id}.md`);
    if (!response.ok) throw new Error("Markdown payload is missing");
    const markdown = await response.text();
    const breadcrumbs = note.path.split("/");
    main.innerHTML = `
      <div class="reader-inner">
        <div class="breadcrumb">${breadcrumbs.map((part) => `<span>${escapeHtml(part)}</span>`).join("")}</div>
        <div class="meta-strip">
          <span class="pill">${escapeHtml(note.type)}</span>
          <span class="pill">${escapeHtml(note.status)}</span>
          <span class="pill">${escapeHtml(note.visibility)}</span>
          <span class="pill">updated ${escapeHtml(note.updated)}</span>
        </div>
        <article class="document">
          ${renderMarkdown(markdown, note)}
        </article>
      </div>
    `;
    renderNoteContext(note, markdown);
    focusMain();
  } catch (error) {
    renderMissing(error.message, note.route);
  }
}

function renderNoteContext(note, markdown) {
  const links = state.backlinks[note.id] || { backlinks: [], outgoing: [] };
  const headings = extractHeadings(markdown);
  contextPanel.innerHTML = `
    <section class="context-section">
      <h2>Document</h2>
      <p class="context-value">${escapeHtml(note.title)}</p>
      <p class="context-meta">${escapeHtml(note.path)}</p>
      <div class="status-row">
        <span class="pill">${escapeHtml(note.type)}</span>
        <span class="pill">${escapeHtml(note.status)}</span>
      </div>
    </section>
    <section class="context-section">
      <h2>Contents</h2>
      ${
        headings.length
          ? headings
              .map(
                (heading) =>
                  `<a class="toc-link depth-${heading.depth}" href="#${heading.id}">${escapeHtml(heading.text)}</a>`,
              )
              .join("")
          : '<p class="muted">No sections yet.</p>'
      }
    </section>
    <section class="context-section">
      <h2>Backlinks</h2>
      ${renderBacklinkList(links.backlinks)}
    </section>
    <section class="context-section">
      <h2>Outgoing</h2>
      ${renderOutgoingList(links.outgoing)}
    </section>
  `;
}

function renderBacklinkList(items) {
  if (!items.length) return '<p class="muted">No backlinks yet.</p>';
  return `
    <ul class="context-list">
      ${items
        .map(
          (item) => `
            <li>
              <a href="${item.sourceRoute}" data-route="${item.sourceRoute}">${escapeHtml(item.sourceTitle)}</a>
              <div class="context-meta">${escapeHtml(item.sourcePath)}</div>
            </li>
          `,
        )
        .join("")}
    </ul>
  `;
}

function renderOutgoingList(items) {
  if (!items.length) return '<p class="muted">No outgoing links yet.</p>';
  return `
    <ul class="context-list">
      ${items
        .map((item) => {
          if (!item.targetId) {
            return `<li><span class="wikilink-broken">${escapeHtml(item.raw)}</span></li>`;
          }
          const note = state.notesById.get(item.targetId);
          return `
            <li>
              <a href="/trove/${item.targetId}" data-route="/trove/${item.targetId}">
                ${escapeHtml(item.targetTitle || note?.title || item.raw)}
              </a>
            </li>
          `;
        })
        .join("")}
    </ul>
  `;
}

function renderSearch() {
  const params = new URLSearchParams(window.location.search);
  const query = params.get("q") || "";
  const results = search(query);
  const resultLabel = query ? `${results.length} result${results.length === 1 ? "" : "s"}` : "Type a query";

  main.innerHTML = `
    <div class="reader-inner">
      <div class="breadcrumb"><span>trove</span><span>search</span></div>
      <h1 class="search-title">Search</h1>
      <p class="search-summary">${escapeHtml(resultLabel)}${query ? ` for "${escapeHtml(query)}"` : ""}</p>
      ${
        query
          ? `<ul class="result-list">${results.map((item) => renderSearchResult(item, query)).join("")}</ul>`
          : '<section class="empty-state"><p class="empty-copy">Search looks across title, path, description, summary, and body snippets.</p></section>'
      }
    </div>
  `;

  contextPanel.innerHTML = `
    <section class="context-section">
      <h2>Search scope</h2>
      <p class="context-meta">Public notes from Daily, Projects, _config, and _archived. _assets is hidden.</p>
    </section>
  `;
  focusMain();
}

function search(query) {
  const q = query.trim().toLowerCase();
  if (!q) return [];

  return state.searchIndex
    .map((item) => {
      const title = item.title.toLowerCase();
      const path = item.path.toLowerCase();
      const description = item.description.toLowerCase();
      const summary = item.summary.toLowerCase();
      const body = item.body.toLowerCase();
      let score = 0;
      if (title.includes(q)) score += 100;
      if (path.includes(q)) score += 60;
      if (description.includes(q)) score += 40;
      if (summary.includes(q)) score += 30;
      if (body.includes(q)) score += 10;
      return { ...item, score };
    })
    .filter((item) => item.score > 0)
    .sort((a, b) => b.score - a.score || a.title.localeCompare(b.title));
}

function renderSearchResult(item, query) {
  return `
    <li>
      <a class="result-title" href="${item.route}" data-route="${item.route}">
        ${highlight(item.title, query)}
      </a>
      <div class="result-path">${escapeHtml(item.path)}</div>
      <p>${highlight(item.summary || item.description || item.snippet, query)}</p>
    </li>
  `;
}

function renderDocList(items) {
  if (!items.length) return '<p class="muted">No documents yet.</p>';
  return `
    <ul class="doc-list">
      ${items
        .map(
          (item) => `
            <li>
              <a class="doc-title" href="${item.route}" data-route="${item.route}">${escapeHtml(item.title)}</a>
              <div class="doc-meta">${escapeHtml(item.path)} · ${escapeHtml(item.type)}</div>
            </li>
          `,
        )
        .join("")}
    </ul>
  `;
}

function renderMarkdown(markdown, currentNote) {
  const lines = markdown.replace(/\r\n/g, "\n").split("\n");
  const usedSlugs = new Map();
  const html = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];
    const trimmed = line.trim();

    if (!trimmed) {
      i += 1;
      continue;
    }

    if (trimmed.startsWith("```")) {
      const code = [];
      i += 1;
      while (i < lines.length && !lines[i].trim().startsWith("```")) {
        code.push(lines[i]);
        i += 1;
      }
      i += 1;
      html.push(`<pre><code>${escapeHtml(code.join("\n"))}</code></pre>`);
      continue;
    }

    const heading = /^(#{1,4})\s+(.+)$/.exec(trimmed);
    if (heading) {
      const depth = heading[1].length;
      const text = heading[2].trim();
      const id = uniqueSlug(text, usedSlugs);
      html.push(`<h${depth} id="${id}">${renderInline(text, currentNote)}</h${depth}>`);
      i += 1;
      continue;
    }

    if (isTableStart(lines, i)) {
      const tableLines = [];
      while (i < lines.length && lines[i].trim().startsWith("|")) {
        tableLines.push(lines[i]);
        i += 1;
      }
      html.push(renderTable(tableLines, currentNote));
      continue;
    }

    if (/^[-*]\s+/.test(trimmed)) {
      const items = [];
      while (i < lines.length && /^[-*]\s+/.test(lines[i].trim())) {
        items.push(lines[i].trim().replace(/^[-*]\s+/, ""));
        i += 1;
      }
      html.push(`<ul>${items.map((item) => `<li>${renderInline(item, currentNote)}</li>`).join("")}</ul>`);
      continue;
    }

    if (/^\d+\.\s+/.test(trimmed)) {
      const items = [];
      while (i < lines.length && /^\d+\.\s+/.test(lines[i].trim())) {
        items.push(lines[i].trim().replace(/^\d+\.\s+/, ""));
        i += 1;
      }
      html.push(`<ol>${items.map((item) => `<li>${renderInline(item, currentNote)}</li>`).join("")}</ol>`);
      continue;
    }

    const paragraph = [];
    while (
      i < lines.length &&
      lines[i].trim() &&
      !/^(#{1,4})\s+/.test(lines[i].trim()) &&
      !/^[-*]\s+/.test(lines[i].trim()) &&
      !/^\d+\.\s+/.test(lines[i].trim()) &&
      !lines[i].trim().startsWith("```") &&
      !isTableStart(lines, i)
    ) {
      paragraph.push(lines[i].trim());
      i += 1;
    }
    html.push(`<p>${renderInline(paragraph.join(" "), currentNote)}</p>`);
  }

  return html.join("\n");
}

function renderInline(text, currentNote) {
  const tokenRe = /`([^`]+)`|\[\[([^\]]+)\]\]|\[([^\]]+)\]\(([^)]+)\)/g;
  let output = "";
  let lastIndex = 0;
  let match;

  while ((match = tokenRe.exec(text))) {
    output += escapeHtml(text.slice(lastIndex, match.index));
    if (match[1]) {
      output += `<code>${escapeHtml(match[1])}</code>`;
    } else if (match[2]) {
      output += renderWikiLink(match[2], currentNote);
    } else if (match[3] && match[4]) {
      output += renderMarkdownLink(match[3], match[4]);
    }
    lastIndex = tokenRe.lastIndex;
  }

  output += escapeHtml(text.slice(lastIndex));
  return output
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/\*([^*]+)\*/g, "<em>$1</em>");
}

function renderWikiLink(raw, currentNote) {
  const [targetPart, alias] = raw.split("|");
  const cleanTarget = targetPart.split("#")[0].trim();
  const label = alias || cleanTarget.split("/").pop() || cleanTarget;
  const targetId = resolveWikiTarget(cleanTarget, currentNote);
  if (!targetId) {
    return `<span class="wikilink-broken">${escapeHtml(label)}</span>`;
  }
  return `<a class="wikilink" href="/trove/${targetId}" data-route="/trove/${targetId}">${escapeHtml(label)}</a>`;
}

function renderMarkdownLink(label, href) {
  if (href.startsWith("/trove/") || href === "/" || href.startsWith("/search")) {
    return `<a href="${escapeAttribute(href)}" data-route="${escapeAttribute(href)}">${escapeHtml(label)}</a>`;
  }
  return `<a href="${escapeAttribute(href)}" target="_blank" rel="noreferrer">${escapeHtml(label)}</a>`;
}

function resolveWikiTarget(target, currentNote) {
  const normalized = target.replace(/\.md$/, "");
  if (state.linkLookup.has(normalized)) return state.linkLookup.get(normalized);

  if (target.includes("/") && currentNote) {
    const base = currentNote.path.split("/").slice(0, -1);
    const resolved = normalizePath([...base, ...target.split("/")]);
    const noExt = resolved.replace(/\.md$/, "");
    return state.linkLookup.get(resolved) || state.linkLookup.get(noExt);
  }

  return null;
}

function normalizePath(parts) {
  const stack = [];
  for (const part of parts) {
    if (!part || part === ".") continue;
    if (part === "..") {
      stack.pop();
    } else {
      stack.push(part);
    }
  }
  return stack.join("/");
}

function isTableStart(lines, index) {
  return (
    lines[index]?.trim().startsWith("|") &&
    lines[index + 1]?.trim().startsWith("|") &&
    /^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?$/.test(lines[index + 1].trim())
  );
}

function renderTable(lines, currentNote) {
  const rows = lines.filter((_, index) => index !== 1).map(splitTableRow);
  const [head = [], ...body] = rows;
  return `
    <table>
      <thead><tr>${head.map((cell) => `<th>${renderInline(cell, currentNote)}</th>`).join("")}</tr></thead>
      <tbody>
        ${body.map((row) => `<tr>${row.map((cell) => `<td>${renderInline(cell, currentNote)}</td>`).join("")}</tr>`).join("")}
      </tbody>
    </table>
  `;
}

function splitTableRow(row) {
  return row
    .trim()
    .replace(/^\|/, "")
    .replace(/\|$/, "")
    .split("|")
    .map((cell) => cell.trim());
}

function extractHeadings(markdown) {
  const usedSlugs = new Map();
  return markdown
    .split("\n")
    .map((line) => /^(#{2,3})\s+(.+)$/.exec(line.trim()))
    .filter(Boolean)
    .map((match) => ({
      depth: match[1].length,
      text: match[2].trim(),
      id: uniqueSlug(match[2].trim(), usedSlugs),
    }));
}

function uniqueSlug(text, usedSlugs) {
  const base =
    text
      .toLowerCase()
      .replace(/`/g, "")
      .replace(/[^a-z0-9가-힣]+/g, "-")
      .replace(/^-+|-+$/g, "") || "section";
  const count = usedSlugs.get(base) || 0;
  usedSlugs.set(base, count + 1);
  return count ? `${base}-${count + 1}` : base;
}

function renderMissing(title, detail) {
  main.innerHTML = `
    <section class="empty-state">
      <h1 class="home-title">${escapeHtml(title)}</h1>
      <p class="empty-copy">${escapeHtml(detail)}</p>
      <a href="/" data-route="/">Return home</a>
    </section>
  `;
  contextPanel.innerHTML = "";
  focusMain();
}

function renderFatalError(error) {
  main.innerHTML = `
    <section class="empty-state">
      <h1 class="home-title">Build output is missing</h1>
      <p class="empty-copy">${escapeHtml(error.message)}</p>
    </section>
  `;
  contextPanel.innerHTML = "";
}

function highlight(text, query) {
  const escaped = escapeHtml(text || "");
  if (!query) return escaped;
  const safeQuery = escapeRegExp(escapeHtml(query));
  return escaped.replace(new RegExp(`(${safeQuery})`, "ig"), "<mark>$1</mark>");
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function escapeAttribute(value) {
  return escapeHtml(value).replaceAll("`", "&#96;");
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function focusMain() {
  main.focus({ preventScroll: true });
}

document.addEventListener("click", (event) => {
  const action = event.target.closest("[data-action]")?.dataset.action;
  if (action === "toggle-nav") {
    document.body.classList.toggle("nav-open");
    return;
  }
  if (action === "focus-search") {
    searchInput?.focus();
    return;
  }

  const route = event.target.closest("[data-route]")?.dataset.route;
  if (route) {
    event.preventDefault();
    navigate(route);
  }
});

searchForm?.addEventListener("submit", (event) => {
  event.preventDefault();
  const query = new FormData(searchForm).get("q")?.toString().trim() || "";
  navigate(`/search${query ? `?q=${encodeURIComponent(query)}` : ""}`);
});

window.addEventListener("popstate", renderRoute);

init();
