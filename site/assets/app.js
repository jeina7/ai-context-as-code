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
  renderLoading("Loading ACAC context");

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
  syncActiveTree();

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
      ${renderTreeList(mainNodes, "main")}
    </section>
    <div class="tree-divider" aria-hidden="true"></div>
    <section class="tree-section">
      <h2 class="tree-section-title">Special contents</h2>
      ${renderTreeList(specialNodes, "special")}
    </section>
  `;
  syncActiveTree();
}

function renderTreeList(nodes, group) {
  if (!nodes.length) return '<p class="muted">No documents yet.</p>';
  return `<ul class="tree-list">${nodes.map((node) => renderTreeNode(node, group)).join("")}</ul>`;
}

function renderTreeNode(node, group) {
  const children = node.children?.length ? renderTreeList(node.children, group) : "";
  const tokenClass = group === "special" ? " special" : "";

  if (node.kind === "note") {
    return `
      <li class="tree-item">
        <a class="tree-link" href="${node.route}" data-route="${node.route}">
          <span class="tree-token${tokenClass}">${escapeHtml(shortType(node.type || "note"))}</span>
          <span>${escapeHtml(node.title)}</span>
        </a>
      </li>
    `;
  }

  const label = node.route
    ? `<a class="tree-link" href="${node.route}" data-route="${node.route}">
        <span class="tree-token${tokenClass}">dir</span><span>${escapeHtml(node.name)}</span>
      </a>`
    : `<div class="tree-folder"><span class="tree-token${tokenClass}">dir</span><span>${escapeHtml(node.name)}</span></div>`;

  return `<li class="tree-item">${label}${children}</li>`;
}

function syncActiveTree() {
  if (!treeRoot) return;
  const currentPath = window.location.pathname;
  for (const link of treeRoot.querySelectorAll(".tree-link")) {
    const active = link.getAttribute("href") === currentPath;
    link.classList.toggle("active", active);
    if (active) {
      link.setAttribute("aria-current", "page");
    } else {
      link.removeAttribute("aria-current");
    }
  }
}

function renderHome() {
  const startHere = state.home.startHere || [];
  const specialContents = state.home.specialContents || [];
  const recentDaily = compactNotes([state.home.today, state.home.recentDaily]);
  const projectDocs = compactNotes([
    state.home.currentProject,
    state.home.latestDesign,
    state.home.latestDecision,
    state.home.latestWorklog,
  ]);

  main.innerHTML = `
    <div class="reader-inner">
      <div class="breadcrumb"><span>trove</span><span>home</span></div>
      <header class="product-header">
        <p class="eyebrow">Public-safe context reader</p>
        <h1 class="home-title">${escapeHtml(state.home.title || "AI Context as Code")}</h1>
        <p class="home-copy">${escapeHtml(
          state.home.description ||
            "First cloud-based ACAC context instance built from trove markdown source.",
        )}</p>
        <div class="scope-row" aria-label="Reader scope">
          <span class="pill success">read-only</span>
          <span class="pill accent">${escapeHtml(String(state.build?.publicNotes || 0))} public notes</span>
          <span class="pill${state.build?.warnings ? " warning" : ""}">
            ${escapeHtml(String(state.build?.warnings || 0))} warnings
          </span>
        </div>
      </header>

      <div class="dashboard-grid">
        <div class="dashboard-stack">
          <section class="module">
            <div class="module-header">
              <div>
                <h2>Context map</h2>
                <p class="module-description">The public reader separates working context from agent-facing special contents.</p>
              </div>
            </div>
            ${renderStructureGrid()}
          </section>

          <section class="module">
            <div class="module-header">
              <div>
                <h2>Start here</h2>
                <p class="module-description">Open these notes first to understand this instance.</p>
              </div>
            </div>
            ${renderDocList(startHere, { showSummary: true })}
          </section>

          <section class="module">
            <div class="module-header">
              <div>
                <h2>Source boundary</h2>
                <p class="module-description">The repository README defines what this reader is allowed to show.</p>
              </div>
            </div>
            <article class="document">
              ${renderMarkdown(stripFirstHeading(state.home.readme || ""), null)}
            </article>
          </section>
        </div>

        <div class="dashboard-stack">
          <section class="module compact">
            <div class="module-header">
              <div>
                <h2>Current project</h2>
                <p class="module-description">The active ACAC implementation surface.</p>
              </div>
            </div>
            ${renderDocList(projectDocs, { showSummary: false })}
          </section>

          <section class="module compact">
            <div class="module-header">
              <div>
                <h2>Today</h2>
                <p class="module-description">Latest day-level context in the public trove.</p>
              </div>
            </div>
            ${renderDocList(recentDaily, { showSummary: true })}
          </section>

          <section class="module compact">
            <div class="module-header">
              <div>
                <h2>Special contents</h2>
                <p class="module-description">Agent-facing markdown, shown as managed content rather than hidden runtime config.</p>
              </div>
            </div>
            ${renderDocList(specialContents, { showSummary: false })}
          </section>

          <section class="module compact">
            <div class="module-header">
              <div>
                <h2>Build status</h2>
                <p class="module-description">Generated output boundary for this static reader.</p>
              </div>
            </div>
            ${renderBuildMetrics()}
          </section>
        </div>
      </div>
    </div>
  `;

  renderHomeContext();
  focusMain();
}

function renderStructureGrid() {
  const counts = countByTopFolder();
  const items = [
    {
      name: "Daily/",
      count: counts.Daily || 0,
      body: "Day-level state, handoff notes, and worklog pointers.",
    },
    {
      name: "Projects/",
      count: counts.Projects || 0,
      body: "Durable project context: designs, decisions, references, and worklogs.",
    },
    {
      name: "_config/",
      count: counts._config || 0,
      body: "Agent-facing memory, skills, commands, and entry sources.",
    },
    {
      name: "_archived/",
      count: counts._archived || 0,
      body: "Retired public-safe context, separated from the active surface.",
    },
  ];

  return `
    <div class="structure-grid">
      ${items
        .map(
          (item) => `
            <div class="structure-item">
              <strong>${escapeHtml(item.name)}</strong>
              <p>${escapeHtml(String(item.count))} public note${item.count === 1 ? "" : "s"}</p>
              <p>${escapeHtml(item.body)}</p>
            </div>
          `,
        )
        .join("")}
    </div>
  `;
}

function renderBuildMetrics() {
  const build = state.build || {};
  return `
    <ul class="metric-list">
      <li>
        <strong>${escapeHtml(String(build.publicNotes || 0))}</strong>
        <span>public notes in generated metadata</span>
      </li>
      <li>
        <strong>${escapeHtml(String(build.warnings || 0))}</strong>
        <span>validation warnings before deploy</span>
      </li>
      <li>
        <strong>${build.analytics?.enabled ? "On" : "Off"}</strong>
        <span>Cloudflare Web Analytics page views</span>
      </li>
    </ul>
  `;
}

function renderHomeContext() {
  const build = state.build || {};
  contextPanel.innerHTML = `
    <section class="context-section">
      <h2>Build</h2>
      <p class="context-value">${escapeHtml(formatBuildTime(build.builtAt))}</p>
      <div class="status-row">
        <span class="pill accent">${escapeHtml(String(build.publicNotes || 0))} notes</span>
        <span class="pill${build.warnings ? " warning" : " success"}">${escapeHtml(
          String(build.warnings || 0),
        )} warnings</span>
        <span class="pill">analytics ${build.analytics?.enabled ? "enabled" : "disabled"}</span>
      </div>
    </section>
    <section class="context-section">
      <h2>Boundary</h2>
      <ul class="context-list">
        <li>
          <strong>Public-safe only</strong>
          <div class="context-meta">Private and internal notes are excluded from this build.</div>
        </li>
        <li>
          <strong>Read-only static reader</strong>
          <div class="context-meta">No editing, runtime hooks, MCP, or live Claude Code connection.</div>
        </li>
        <li>
          <strong>Generated output</strong>
          <div class="context-meta">The site reads JSON and markdown payloads built from trove source.</div>
        </li>
      </ul>
    </section>
    <section class="context-section">
      <h2>Search scope</h2>
      <p class="context-meta">Daily, Projects, _config, and _archived are searchable. _assets stays hidden.</p>
    </section>
  `;
}

async function renderNote(id) {
  const note = state.notesById.get(id);
  if (!note) {
    renderMissing("Document not found", `/trove/${id}`);
    return;
  }

  renderLoading("Loading note");
  try {
    const response = await fetch(`/content/trove/${id}.md`);
    if (!response.ok) throw new Error("Markdown payload is missing");
    const markdown = await response.text();
    const prepared = prepareNoteMarkdown(markdown, note);
    const breadcrumbs = note.path.split("/");

    main.innerHTML = `
      <div class="reader-inner narrow">
        <div class="breadcrumb">${breadcrumbs.map((part) => `<span>${escapeHtml(part)}</span>`).join("")}</div>
        <header class="note-header">
          <div class="meta-strip">
            ${renderNotePills(note)}
          </div>
          <h1 class="note-title">${escapeHtml(note.title)}</h1>
          ${renderSummary(note.summary)}
        </header>
        <article class="document">
          ${renderMarkdown(prepared.body, note)}
        </article>
      </div>
    `;

    renderNoteContext(note, prepared.body);
    focusMain();
  } catch (error) {
    renderMissing(error.message, note.route);
  }
}

function renderNoteContext(note, markdown) {
  const links = state.backlinks[note.id] || { backlinks: [], outgoing: [] };
  const headings = extractHeadings(markdown);
  const related = findRelatedContext(note);

  contextPanel.innerHTML = `
    <section class="context-section">
      <h2>Document</h2>
      <p class="context-value">${escapeHtml(note.title)}</p>
      <p class="context-meta">${escapeHtml(note.path)}</p>
      <div class="status-row">
        ${renderNotePills(note)}
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
      <h2>Connections</h2>
      <div class="status-row">
        <span class="pill">${escapeHtml(String(links.backlinks.length))} backlinks</span>
        <span class="pill">${escapeHtml(String(links.outgoing.length))} outgoing</span>
        <span class="pill${links.outgoing.some((item) => item.broken) ? " warning" : ""}">
          ${escapeHtml(String(links.outgoing.filter((item) => item.broken).length))} broken
        </span>
      </div>
    </section>
    <section class="context-section">
      <h2>Backlinks</h2>
      ${renderBacklinkList(links.backlinks)}
    </section>
    <section class="context-section">
      <h2>Outgoing</h2>
      ${renderOutgoingList(links.outgoing)}
    </section>
    <section class="context-section">
      <h2>Related context</h2>
      ${renderDocList(related, { showSummary: false })}
    </section>
  `;
}

function renderNotePills(note) {
  return `
    <span class="pill">${escapeHtml(note.type || "note")}</span>
    <span class="pill${note.status === "active" ? " success" : ""}">${escapeHtml(note.status || "unknown")}</span>
    <span class="pill${specialClass(note)}">${escapeHtml(note.visibility || "unknown")}</span>
    ${note.updated ? `<span class="pill">updated ${escapeHtml(note.updated)}</span>` : ""}
    ${isSpecialPath(note.path) ? '<span class="pill special">special contents</span>' : ""}
  `;
}

function renderSummary(summary) {
  const lines = splitLines(summary);
  if (!lines.length) return "";
  return `
    <div class="note-summary">
      ${lines.map((line) => `<p>${renderInline(line, null)}</p>`).join("")}
    </div>
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
            return `
              <li>
                <span class="wikilink-broken">${escapeHtml(item.raw)}</span>
                <div class="context-meta">Broken wikilink. Validator warnings should catch this before deploy.</div>
              </li>
            `;
          }
          const note = state.notesById.get(item.targetId);
          return `
            <li>
              <a href="/trove/${item.targetId}" data-route="/trove/${item.targetId}">
                ${escapeHtml(item.targetTitle || note?.title || item.raw)}
              </a>
              ${note?.path ? `<div class="context-meta">${escapeHtml(note.path)}</div>` : ""}
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
  const resultLabel = query
    ? `${results.length} result${results.length === 1 ? "" : "s"} for "${query}"`
    : "Search the public trove";

  main.innerHTML = `
    <div class="reader-inner narrow">
      <div class="breadcrumb"><span>trove</span><span>search</span></div>
      <header class="search-header">
        <p class="eyebrow">Context retrieval</p>
        <h1 class="search-title">Search</h1>
        <p class="search-summary">${escapeHtml(resultLabel)}</p>
        <div class="scope-row">
          <span class="pill">title</span>
          <span class="pill">path</span>
          <span class="pill">summary</span>
          <span class="pill special">special contents included</span>
          <span class="pill">_assets hidden</span>
        </div>
      </header>
      ${
        query
          ? results.length
            ? `<ul class="result-list">${results.map((item) => renderSearchResult(item, query)).join("")}</ul>`
            : renderInlineState("No matching context", "Try a shorter title, folder name, or project keyword.")
          : renderInlineState(
              "Ready to search",
              "Search looks across title, path, description, summary, and body snippets in the generated public index.",
            )
      }
    </div>
  `;

  renderSearchContext(query, results);
  focusMain();
}

function renderSearchContext(query, results) {
  const specialCount = results.filter((item) => isSpecialPath(item.path)).length;
  contextPanel.innerHTML = `
    <section class="context-section">
      <h2>Search scope</h2>
      <p class="context-meta">Public notes from Daily, Projects, _config, and _archived. _assets is hidden.</p>
    </section>
    <section class="context-section">
      <h2>Current query</h2>
      <p class="context-value">${escapeHtml(query || "No query yet")}</p>
      <div class="status-row">
        <span class="pill">${escapeHtml(String(results.length))} results</span>
        <span class="pill special">${escapeHtml(String(specialCount))} special</span>
      </div>
    </section>
  `;
}

function search(query) {
  const q = query.trim().toLowerCase();
  if (!q) return [];

  return state.searchIndex
    .map((item) => {
      const title = (item.title || "").toLowerCase();
      const path = (item.path || "").toLowerCase();
      const description = (item.description || "").toLowerCase();
      const summary = (item.summary || "").toLowerCase();
      const body = (item.body || "").toLowerCase();
      let score = 0;
      if (title.includes(q)) score += 100;
      if (path.includes(q)) score += 60;
      if (description.includes(q)) score += 40;
      if (summary.includes(q)) score += 30;
      if (body.includes(q)) score += 10;
      if (isSpecialPath(item.path)) score -= 4;
      return { ...item, score };
    })
    .filter((item) => item.score > 0)
    .sort((a, b) => b.score - a.score || a.title.localeCompare(b.title));
}

function renderSearchResult(item, query) {
  return `
    <li>
      <div class="result-row">
        <div>
          <a class="result-title" href="${item.route}" data-route="${item.route}">
            ${highlight(item.title, query)}
          </a>
          <div class="result-path">${escapeHtml(item.path)}</div>
          <p class="result-summary">${highlight(firstUsefulText(item), query)}</p>
        </div>
        <div class="status-row">
          <span class="pill">${escapeHtml(item.type || "note")}</span>
          ${isSpecialPath(item.path) ? '<span class="pill special">special</span>' : ""}
          ${item.status ? `<span class="pill${item.status === "active" ? " success" : ""}">${escapeHtml(item.status)}</span>` : ""}
        </div>
      </div>
    </li>
  `;
}

function renderDocList(items, options = {}) {
  const docs = compactNotes(items);
  if (!docs.length) return '<p class="muted">No public documents yet.</p>';
  const showSummary = options.showSummary ?? false;
  return `
    <ul class="doc-list">
      ${docs
        .map(
          (item) => `
            <li>
              <div class="doc-row">
                <div>
                  <a class="doc-title" href="${item.route}" data-route="${item.route}">${escapeHtml(item.title)}</a>
                  <div class="doc-meta">${escapeHtml(item.path)} · ${escapeHtml(item.type || "note")}</div>
                  ${showSummary && item.summary ? `<p class="doc-summary">${escapeHtml(firstLine(item.summary))}</p>` : ""}
                </div>
                <div class="status-row">
                  ${item.status ? `<span class="pill${item.status === "active" ? " success" : ""}">${escapeHtml(item.status)}</span>` : ""}
                  ${isSpecialPath(item.path) ? '<span class="pill special">special</span>' : ""}
                </div>
              </div>
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

    if (trimmed === "---") {
      html.push("<hr />");
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
      html.push(
        `<h${depth} id="${id}"><a class="heading-anchor" href="#${id}">${renderInline(text, currentNote)}</a></h${depth}>`,
      );
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

    if (trimmed.startsWith(">")) {
      const quote = [];
      while (i < lines.length && lines[i].trim().startsWith(">")) {
        quote.push(lines[i].trim().replace(/^>\s?/, ""));
        i += 1;
      }
      html.push(`<blockquote><p>${renderInline(quote.join(" "), currentNote)}</p></blockquote>`);
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
      !lines[i].trim().startsWith(">") &&
      !lines[i].trim().startsWith("```") &&
      lines[i].trim() !== "---" &&
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
      text: stripInlineMarkers(match[2].trim()),
      id: uniqueSlug(match[2].trim(), usedSlugs),
    }));
}

function uniqueSlug(text, usedSlugs) {
  const base =
    stripInlineMarkers(text)
      .toLowerCase()
      .replace(/[^a-z0-9가-힣]+/g, "-")
      .replace(/^-+|-+$/g, "") || "section";
  const count = usedSlugs.get(base) || 0;
  usedSlugs.set(base, count + 1);
  return count ? `${base}-${count + 1}` : base;
}

function prepareNoteMarkdown(markdown, note) {
  const lines = markdown.replace(/\r\n/g, "\n").split("\n");
  let index = 0;

  while (index < lines.length && !lines[index].trim()) index += 1;
  if (/^#\s+/.test(lines[index]?.trim() || "")) {
    index += 1;
    while (index < lines.length && !lines[index].trim()) index += 1;
  }

  const summaryLines = splitLines(note.summary);
  if (summaryLines.length) {
    let probe = index;
    while (probe < lines.length && !lines[probe].trim()) probe += 1;
    let matched = 0;
    while (
      matched < summaryLines.length &&
      probe < lines.length &&
      lines[probe].trim() === summaryLines[matched].trim()
    ) {
      probe += 1;
      matched += 1;
    }
    if (matched === summaryLines.length) {
      index = probe;
      while (index < lines.length && !lines[index].trim()) index += 1;
    }
  }

  return { body: lines.slice(index).join("\n").trim() };
}

function stripFirstHeading(markdown) {
  return markdown.replace(/^\s*#\s+.+\n+/, "").trim();
}

function splitLines(value) {
  return String(value || "")
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);
}

function stripInlineMarkers(value) {
  return String(value || "")
    .replace(/`([^`]+)`/g, "$1")
    .replace(/\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]/g, (_, target, alias) => alias || target)
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
    .replace(/\*\*([^*]+)\*\*/g, "$1")
    .replace(/\*([^*]+)\*/g, "$1");
}

function renderMissing(title, detail) {
  main.innerHTML = `
    <section class="state-card">
      <p class="eyebrow">Reader state</p>
      <h1 class="state-title">${escapeHtml(title)}</h1>
      <p class="state-copy">${escapeHtml(detail)}</p>
      <div class="action-row">
        <a class="text-button" href="/" data-route="/">Return home</a>
        <a class="text-button" href="/search" data-route="/search">Open search</a>
      </div>
    </section>
  `;
  contextPanel.innerHTML = `
    <section class="context-section">
      <h2>Missing route</h2>
      <p class="context-meta">The public reader only serves generated routes from the build output.</p>
    </section>
  `;
  focusMain();
}

function renderFatalError(error) {
  main.innerHTML = `
    <section class="state-card">
      <p class="eyebrow">Build output</p>
      <h1 class="state-title">Build output is missing</h1>
      <p class="state-copy">${escapeHtml(error.message)}</p>
    </section>
  `;
  contextPanel.innerHTML = "";
}

function renderLoading(label) {
  main.innerHTML = `
    <section class="loading-state" aria-live="polite">
      <p class="eyebrow">${escapeHtml(label)}</p>
      <div class="loading-line medium"></div>
      <div class="loading-line"></div>
      <div class="loading-line short"></div>
    </section>
  `;
}

function renderInlineState(title, body) {
  return `
    <section class="state-card">
      <h2 class="state-title">${escapeHtml(title)}</h2>
      <p class="state-copy">${escapeHtml(body)}</p>
    </section>
  `;
}

function findRelatedContext(note) {
  if (!note.path.startsWith("Projects/ai-context-as-code/")) return [];
  return compactNotes([
    state.home?.currentProject,
    state.home?.latestDesign,
    state.home?.latestDecision,
    state.home?.latestWorklog,
  ]).filter((item) => item.id !== note.id);
}

function countByTopFolder() {
  const counts = {};
  for (const note of state.notes) {
    const top = note.path.split("/")[0];
    counts[top] = (counts[top] || 0) + 1;
  }
  return counts;
}

function compactNotes(items) {
  const seen = new Set();
  return (items || []).filter((item) => {
    if (!item || !item.id || seen.has(item.id)) return false;
    seen.add(item.id);
    return true;
  });
}

function shortType(type) {
  const map = {
    "agent-entry": "agt",
    "context-design": "ctx",
    command: "cmd",
    convention: "cnv",
    daily: "day",
    decision: "dec",
    design: "des",
    index: "idx",
    memory: "mem",
    principle: "prn",
    project: "prj",
    reference: "ref",
    research: "rsr",
    skill: "skl",
    worklog: "log",
  };
  return map[type] || String(type || "note").slice(0, 4);
}

function firstUsefulText(item) {
  return firstLine(item.summary) || item.description || item.snippet || "";
}

function firstLine(value) {
  return splitLines(value)[0] || "";
}

function isSpecialPath(path) {
  return String(path || "").startsWith("_config/") || String(path || "").startsWith("_archived/");
}

function specialClass(note) {
  if (note.visibility === "public") return " success";
  if (note.visibility === "internal") return " warning";
  if (note.visibility === "private") return " danger";
  return "";
}

function formatBuildTime(value) {
  if (!value) return "Not built yet";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleString(undefined, {
    year: "numeric",
    month: "short",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
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
    document.body.classList.add("nav-open");
    window.setTimeout(() => searchInput?.focus(), 80);
    return;
  }

  const route = event.target.closest("[data-route]")?.dataset.route;
  if (route) {
    event.preventDefault();
    navigate(route);
  }
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    document.body.classList.remove("nav-open");
  }
});

searchForm?.addEventListener("submit", (event) => {
  event.preventDefault();
  const query = new FormData(searchForm).get("q")?.toString().trim() || "";
  navigate(`/search${query ? `?q=${encodeURIComponent(query)}` : ""}`);
});

window.addEventListener("popstate", renderRoute);

init();
