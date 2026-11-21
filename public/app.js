/* Editor look-alike with a scripted chat pane. All content comes from
   window.REPOS (written by tools/build.py): one entry per practice repo,
   each shown as a tab at the top of the page. No framework, no build step. */
(function () {
  'use strict';

  const REPOS = (window.REPOS || (window.REPO_DATA ? [window.REPO_DATA] : [])).map((r, n) => ({ id: r.id || 'repo' + n, chat: [], terminal: [], ...r }));
  const $ = (id) => document.getElementById(id);
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const baseName = (p) => p.split('/').pop();
  const dirName = (p) => p.split('/').slice(0, -1).join('/');
  const STATUS_NAME = { M: 'Modified', U: 'Untracked', D: 'Deleted' };
  const narrow = () => window.innerWidth <= 760;

  /* ------------------------------------------------------------ state
     Every repo keeps its own state object (open tabs, working tree, chat),
     so switching tabs at the top and back again picks up where you left off.
     REPO / files / changes / state always point at the active repo. */
  let REPO, files, changes, state;
  const stateByRepo = new Map();
  const ui = { sideOpen: !narrow(), panelOpen: false, chatOpen: !narrow(), suggestOpen: true };

  function freshState(repo) {
    const map = new Map();
    for (const f of repo.files) {
      const copy = { ...f };
      if (!copy.status) copy.head = copy.working;   // unchanged: HEAD is the same as the working tree
      map.set(copy.path, copy);
    }
    return {
      view: 'explorer',            // 'explorer' | 'scm'
      collapsed: new Set(),        // folder paths the reader has closed
      tabs: [],                    // { id, kind: 'file' | 'diff', path, preview, rich }
      activeId: null,
      diffMode: 'auto',            // 'auto' picks side by side only when both sides fit
      line: null,
      files: map,
      terminal: repo.terminal.slice(),
      chat: [],                    // { role: 'user', text } | { role: 'ai', step, pending, fresh } | { role: 'ai', text, hint }
      done: new Set(),             // chat step ids that have run
      draft: '',
      busy: false,
    };
  }

  function recompute() {
    changes = [...files.values()].filter((f) => f.status).sort((x, y) => x.path.localeCompare(y.path));
  }

  function loadRepo(id) {
    if (REPO) state.draft = $('chat-text').value;
    REPO = REPOS.find((r) => r.id === id) || REPOS[0];
    if (!stateByRepo.has(REPO.id)) stateByRepo.set(REPO.id, freshState(REPO));
    state = stateByRepo.get(REPO.id);
    files = state.files;
    recompute();
    $('chat-text').value = state.draft;
  }

  /* ------------------------------------------------------------ icons */
  const svg = (body, size, cls) =>
    `<svg class="${cls || 'ico'}" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" aria-hidden="true">${body}</svg>`;
  const ICON = {
    explorer: svg('<path d="M8 7H5.5A1.5 1.5 0 0 0 4 8.5v11A1.5 1.5 0 0 0 5.5 21h7a1.5 1.5 0 0 0 1.5-1.5V18"/><path d="M9.500 3h6L20 7.500v9a1.500 1.500 0 0 1-1.500 1.500h-9A1.500 1.500 0 0 1 8 16.500v-12A1.500 1.500 0 0 1 9.500 3z"/><path d="M15 3v5h5"/>', 24),
    scm: svg('<circle cx="7" cy="5" r="2.200"/><circle cx="7" cy="19" r="2.200"/><circle cx="17" cy="9" r="2.200"/><path d="M7 7.200v9.600M17 11.200c0 4-10 2-10 5.600"/>', 24),
    branch: svg('<circle cx="4.500" cy="3.500" r="1.500"/><circle cx="4.500" cy="12.500" r="1.500"/><circle cx="11.500" cy="6" r="1.500"/><path d="M4.500 5v6M11.500 7.500c0 2.500-7 1.500-7 3.500"/>', 16),
    right: svg('<path d="M6 4l4 4-4 4"/>', 16),
    down: svg('<path d="M4 6l4 4 4-4"/>', 16),
    close: svg('<path d="M4.500 4.500l7 7M11.500 4.500l-7 7"/>', 16),
    side: svg('<rect x="2" y="3" width="12" height="10" rx="1.500"/><path d="M6 3v10"/>', 16),
    panel: svg('<rect x="2" y="3" width="12" height="10" rx="1.500"/><path d="M2 9.500h12"/>', 16),
    theme: svg('<circle cx="8" cy="8" r="5.500"/><path d="M8 2.500a5.500 5.500 0 0 1 0 11z" fill="currentColor"/>', 16),
    check: svg('<path d="M3 8.500l3.200 3.200L13 5"/>', 16),
    terminal: svg('<path d="M3 4.500l4 3.500-4 3.500M8.500 12H13"/>', 16),
    spark: svg('<path d="M8 1.800l1.300 3.600 3.600 1.300-3.600 1.300L8 11.600 6.700 8 3.100 6.700l3.600-1.300z"/><path d="M12.500 10.500l.6 1.600 1.600.6-1.600.6-.6 1.600-.6-1.600-1.600-.6 1.600-.6z"/>', 16),
    send: svg('<path d="M2.500 8h9M8 3.500 12.500 8 8 12.500"/>', 16),
    reset: svg('<path d="M3 8a5 5 0 1 0 1.500-3.600"/><path d="M3 2.500v3h3"/>', 16),
    user: svg('<circle cx="8" cy="5.500" r="2.700"/><path d="M2.800 14c.7-2.800 2.800-4.200 5.200-4.200s4.500 1.400 5.200 4.200"/>', 16),
    lock: svg('<rect x="3" y="7" width="10" height="7" rx="1.200"/><path d="M5.500 7V5a2.500 2.500 0 0 1 5 0v2"/>', 16),
    mark: svg('<path d="M6 5 3.500 8 6 11M10 5l2.500 3L10 11" stroke="#fff" stroke-width="1.600"/>', 16),
  };
  const FILE_ICON = {
    python: '<rect x="2.500" y="2" width="7.500" height="7.500" rx="2.200" fill="#4b8bbe"/><rect x="6" y="6.500" width="7.500" height="7.500" rx="2.200" fill="#f2c53d"/>',
    markdown: '<g stroke="var(--ic-md)"><rect x="1.500" y="3.500" width="13" height="9" rx="1.500"/><path d="M4 10V6.200l2 2.200 2-2.200V10M11.500 6v3.800M9.900 8.300l1.600 1.600 1.600-1.600"/></g>',
    csv: '<g stroke="var(--ic-csv)"><rect x="2" y="3" width="12" height="10" rx="1.200"/><path d="M2 6.400h12M2 9.700h12M6.200 3v10M10 3v10"/></g>',
    sheet: '<g stroke="var(--ic-csv)"><rect x="2" y="2" width="12" height="12" rx="1.500"/><path d="M5 5.500l3 5M8 5.500l-3 5M10 6h2M10 8h2M10 10h2"/></g>',
    image: '<g stroke="var(--ic-img)"><rect x="2" y="3" width="12" height="10" rx="1.500"/><circle cx="5.600" cy="6.400" r="1.100"/><path d="M2.500 12l3.500-3.500 2.500 2.500 2-2 3 3"/></g>',
    ignore: '<g stroke="var(--ic-git)"><path d="M8 2.200l5.800 5.800L8 13.800 2.200 8z"/><circle cx="8" cy="8" r="1.200"/></g>',
    plaintext: '<g stroke="var(--ic-txt)"><path d="M3 4.500h10M3 7.500h10M3 10.500h10M3 13.500h6"/></g>',
  };
  const fileIcon = (path) => svg(FILE_ICON[langOf(path)] || FILE_ICON.plaintext, 16);

  /* --------------------------------------------------------- languages */
  const LANG_LABEL = { python: 'Python', markdown: 'Markdown', csv: 'CSV', sheet: 'Excel Workbook', image: 'Image', ignore: 'Ignore', plaintext: 'Plain Text' };
  function langOf(path) {
    const name = baseName(path);
    const ext = name.includes('.') ? name.split('.').pop().toLowerCase() : '';
    if (name === '.gitignore') return 'ignore';
    if (ext === 'py') return 'python';
    if (ext === 'md') return 'markdown';
    if (ext === 'csv') return 'csv';
    if (ext === 'xlsx' || ext === 'xls') return 'sheet';
    if (['png', 'jpg', 'jpeg', 'gif', 'svg', 'webp'].includes(ext)) return 'image';
    return 'plaintext';
  }

  /* -------------------------------------------------------- tokenizers
     Each returns an array of lines; a line is an array of [class, text]. */
  const words = (s) => new Set(s.split(' '));
  const PY_FLOW = words('if elif else for while in return import from as with try except finally raise pass break continue yield assert');
  const PY_WORD = words('def class lambda and or not is None True False global nonlocal del async await');
  const PY_TYPE = words('str int float bool list dict set tuple Path');

  function toLines(tokens) {
    const lines = [[]];
    for (const [cls, text] of tokens) {
      text.split('\n').forEach((part, i) => {
        if (i) lines.push([]);
        if (part) lines[lines.length - 1].push([cls, part]);
      });
    }
    return lines;
  }

  function tokPython(text) {
    const re = /(#[^\n]*)|([rbfuRBFU]{0,2}(?:"""[\s\S]*?"""|'''[\s\S]*?'''))|([rbfuRBFU]{0,2}(?:"(?:\\.|[^"\\\n])*"|'(?:\\.|[^'\\\n])*'))|(@[A-Za-z_][\w.]*)|(\d[\d_]*\.?\d*)|([A-Za-z_]\w*)|(\s+)|([\s\S])/g;
    const out = [];
    let prev = '';
    let m;
    while ((m = re.exec(text))) {
      const t = m[0];
      if (m[1]) out.push(['cm', t]);
      else if (m[2]) out.push(['st', t]);
      else if (m[3]) {
        if (/^[rbuRBU]?[fF]/.test(t)) {
          t.split(/(\{[^{}]*\})/).forEach((part, i) => part && out.push([i % 2 ? 'va' : 'st', part]));
        } else out.push(['st', t]);
      } else if (m[4]) out.push(['fn', t]);
      else if (m[5]) out.push(['nu', t]);
      else if (m[6]) {
        let cls = 'va';
        if (PY_FLOW.has(t)) cls = 'kc';
        else if (PY_WORD.has(t)) cls = 'kw';
        else if (prev === 'def') cls = 'fn';
        else if (prev === 'class' || prev === 'import' || prev === 'from' || prev === 'as' || PY_TYPE.has(t)) cls = 'ty';
        else if (text[re.lastIndex] === '(') cls = 'fn';
        else if (/^[A-Z][A-Z0-9_]+$/.test(t)) cls = 'cn';
        out.push([cls, t]);
      } else out.push(['', t]);
      if (!m[7]) prev = t;
    }
    return toLines(out);
  }

  function tokMarkdownInline(line) {
    const toks = [];
    let rest = line;
    const list = /^(\s*)([-*+]|\d+\.)(\s+)/.exec(line);
    if (list) {
      toks.push(['', list[1]], ['li', list[2]], ['', list[3]]);
      rest = line.slice(list[0].length);
    }
    const re = /(`[^`]*`)|(\*\*[^*]+\*\*)|(\*[^*\s][^*]*\*)|(\[[^\]]*\])(\([^)]*\))|(\|)/g;
    let last = 0;
    let m;
    while ((m = re.exec(rest))) {
      if (m.index > last) toks.push(['', rest.slice(last, m.index)]);
      if (m[1]) toks.push(['cd', m[1]]);
      else if (m[2]) toks.push(['bd', m[2]]);
      else if (m[3]) toks.push(['it', m[3]]);
      else if (m[4]) toks.push(['lk', m[4]], ['ur', m[5]]);
      else toks.push(['mt', m[6]]);
      last = re.lastIndex;
    }
    if (last < rest.length) toks.push(['', rest.slice(last)]);
    return toks;
  }

  function tokMarkdown(text) {
    const lines = text.split('\n');
    let front = lines[0] === '---';
    let fence = false;
    return lines.map((line, i) => {
      if (front) {
        if (line === '---') { if (i) front = false; return [['mt', line]]; }
        const kv = /^(\s*)([\w-]+)(:)(.*)$/.exec(line);
        return kv ? [['', kv[1]], ['tg', kv[2]], ['', kv[3]], ['st', kv[4]]] : [['st', line]];
      }
      if (/^\s*```/.test(line)) { fence = !fence; return [['mt', line]]; }
      if (fence) return [['cd', line]];
      if (/^#{1,6}\s/.test(line)) return [['hd', line]];
      return tokMarkdownInline(line);
    });
  }

  function splitCsv(line) {
    const cells = [''];
    let quoted = false;
    for (const ch of line) {
      if (ch === '"') quoted = !quoted;
      if (ch === ',' && !quoted) cells.push('');
      else cells[cells.length - 1] += ch;
    }
    return cells;
  }
  const tokCsv = (text) => text.split('\n').map((line) => {
    const toks = [];
    splitCsv(line).forEach((cell, i) => {
      if (i) toks.push(['mt', ',']);
      if (cell) toks.push(['c' + (i % 9), cell]);
    });
    return line ? toks : [];
  });

  const tokPlain = (text) => text.split('\n').map((line) => (line ? [[/^\s*#/.test(line) ? 'cm' : '', line]] : []));

  function tokenize(path, text) {
    const body = text.replace(/\n$/, '');
    const lang = langOf(path);
    if (lang === 'python') return tokPython(body);
    if (lang === 'markdown') return tokMarkdown(body);
    if (lang === 'csv') return tokCsv(body);
    return tokPlain(body);
  }

  /** Tokens -> HTML. `range` ([from, to) in characters) marks an in-line change. */
  function lineHtml(tokens, range) {
    let html = '';
    let pos = 0;
    for (const [cls, text] of tokens) {
      const start = pos;
      const end = (pos += text.length);
      const wrap = (s) => (cls ? `<span class="t-${cls}">${esc(s)}</span>` : esc(s));
      if (!range || range[1] <= start || range[0] >= end) { html += wrap(text); continue; }
      const a = Math.max(range[0], start) - start;
      const b = Math.min(range[1], end) - start;
      html += (a ? wrap(text.slice(0, a)) : '') + `<span class="chg">${wrap(text.slice(a, b))}</span>` + (b < text.length ? wrap(text.slice(b)) : '');
    }
    return html;
  }

  /* -------------------------------------------------------------- diff */
  function diffRows(a, b) {
    const n = a.length, m = b.length;
    const lcs = Array.from({ length: n + 1 }, () => new Uint16Array(m + 1));
    for (let i = n - 1; i >= 0; i--) {
      for (let j = m - 1; j >= 0; j--) {
        lcs[i][j] = a[i] === b[j] ? lcs[i + 1][j + 1] + 1 : Math.max(lcs[i + 1][j], lcs[i][j + 1]);
      }
    }
    const rows = [];
    let dels = [], adds = [];
    const flush = () => {
      for (let k = 0; k < Math.max(dels.length, adds.length); k++) {
        rows.push({ l: k < dels.length ? dels[k] : null, r: k < adds.length ? adds[k] : null, same: false });
      }
      dels = []; adds = [];
    };
    let i = 0, j = 0;
    while (i < n || j < m) {
      if (i < n && j < m && a[i] === b[j]) { flush(); rows.push({ l: i++, r: j++, same: true }); }
      else if (j >= m || (i < n && lcs[i + 1][j] >= lcs[i][j + 1])) dels.push(i++);
      else adds.push(j++);
    }
    flush();
    return rows;
  }

  /** Changed character ranges for a pair of lines, or null if they share too little. */
  function changedRange(x, y) {
    const max = Math.min(x.length, y.length);
    let p = 0;
    while (p < max && x[p] === y[p]) p++;
    let s = 0;
    while (s < max - p && x[x.length - 1 - s] === y[y.length - 1 - s]) s++;
    if (p + s < max * 0.3) return null;
    return [[p, x.length - s], [p, y.length - s]];
  }

  /** Side by side only works when the longest line fits in half the editor. */
  function fitsSideBySide(file) {
    const probe = document.createElement('span');
    probe.className = 'code';
    probe.style.cssText = 'position:absolute;visibility:hidden;white-space:pre';
    probe.textContent = '0'.repeat(100);
    document.body.appendChild(probe);
    const ch = probe.getBoundingClientRect().width / 100;
    probe.remove();
    const longest = Math.max(...((file.head || '') + '\n' + (file.working || '')).split('\n').map((l) => l.length));
    return (longest + 9) * ch + 16 <= $('editor').clientWidth / 2;
  }
  const diffIsInline = (file) => state.diffMode === 'inline' || (state.diffMode === 'auto' && !fitsSideBySide(file));

  function renderDiff(file, inline) {
    const oldText = (file.head || '').replace(/\n$/, '');
    const newText = (file.working || '').replace(/\n$/, '');
    const a = oldText.split('\n'), b = newText.split('\n');
    const ta = tokenize(file.path, oldText), tb = tokenize(file.path, newText);
    const rows = diffRows(a, b);
    let added = 0, removed = 0, html = '';
    const num = (n, cls) => `<div class="ln ${cls}">${n == null ? '' : n + 1}</div>`;
    for (const row of rows) {
      const pair = !row.same && row.l != null && row.r != null ? changedRange(a[row.l], b[row.r]) : null;
      const left = row.l == null ? '' : lineHtml(ta[row.l], pair && pair[0]);
      const right = row.r == null ? '' : lineHtml(tb[row.r], pair && pair[1]);
      if (!row.same) { if (row.l != null) removed++; if (row.r != null) added++; }
      if (inline) {
        if (row.same) html += num(row.l, '') + num(row.r, '') + `<div class="lc">${right}</div>`;
        else {
          if (row.l != null) html += num(row.l, 'del') + num(null, 'del') + `<div class="lc del">${left}</div>`;
          if (row.r != null) html += num(null, 'add') + num(row.r, 'add') + `<div class="lc add">${right}</div>`;
        }
      } else {
        const lc = row.same ? '' : row.l == null ? 'fill' : 'del';
        const rc = row.same ? '' : row.r == null ? 'fill' : 'add';
        html += num(row.l, lc) + `<div class="lc left ${lc}">${left}</div>` + num(row.r, rc) + `<div class="lc ${rc}">${right}</div>`;
      }
    }
    const head = inline ? '' : '<div class="diff-head"><span>HEAD (last commit)</span><span>Working tree</span></div>';
    return { html: `${head}<div class="diff ${inline ? 'inline' : 'split'}">${html}</div>`, added, removed };
  }

  /* ---------------------------------------------------- markdown preview */
  function resolvePath(from, href) {
    const parts = dirName(from).split('/').filter(Boolean);
    for (const seg of href.split('#')[0].split('/')) {
      if (seg === '..') parts.pop();
      else if (seg && seg !== '.') parts.push(seg);
    }
    return parts.join('/');
  }

  function mdInline(src, path) {
    const codes = [];
    let s = src.replace(/`([^`]*)`/g, (_, c) => `\u0001${codes.push(c) - 1}\u0001`);
    s = esc(s);
    s = s.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (_, label, href) => {
      if (/^https?:/.test(href)) return `<a href="${href}" target="_blank" rel="noopener">${label}</a>`;
      const target = resolvePath(path, href);
      return files.has(target) ? `<a href="${fileHash('file', target)}" data-open="${esc(target)}">${label}</a>` : label;
    });
    s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>').replace(/\*([^*\s][^*]*)\*/g, '<em>$1</em>');
    // `path/to/file` in prose opens that file when it exists in the repo.
    return s.replace(/\u0001(\d+)\u0001/g, (_, n) => {
      const code = codes[n];
      const f = files.get(code);
      return f && f.working !== undefined
        ? `<a class="code-link" href="${fileHash('file', code)}" data-open="${esc(code)}"><code>${esc(code)}</code></a>`
        : `<code>${esc(code)}</code>`;
    });
  }

  function renderMarkdown(text, path) {
    const lines = text.replace(/\n$/, '').split('\n');
    const inline = (s) => mdInline(s, path);
    const isItem = (l) => /^\s*([-*+]|\d+\.)\s+/.test(l);
    let html = '';
    let i = 0;
    if (lines[0] === '---') {
      const end = lines.indexOf('---', 1);
      const pairs = [];
      lines.slice(1, end).forEach((l) => {
        const kv = /^([\w-]+):\s*(.*)$/.exec(l);
        if (kv) pairs.push([kv[1], /^[>|][-+]?$/.test(kv[2]) ? '' : kv[2]]);
        else if (pairs.length) pairs[pairs.length - 1][1] += (pairs[pairs.length - 1][1] ? ' ' : '') + l.trim();
      });
      html += '<div class="fm"><div class="fm-title">Front matter</div><dl>' +
        pairs.map(([k, v]) => `<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join('') + '</dl></div>';
      i = end + 1;
    }
    while (i < lines.length) {
      const line = lines[i];
      let m;
      if (!line.trim()) { i++; continue; }
      if (line.trim().startsWith('```')) {
        const code = [];
        for (i++; i < lines.length && !lines[i].trim().startsWith('```'); i++) code.push(lines[i]);
        i++;
        html += `<pre><code>${esc(code.join('\n'))}</code></pre>`;
      } else if ((m = /^(#{1,6})\s+(.*)$/.exec(line))) {
        html += `<h${m[1].length}>${inline(m[2])}</h${m[1].length}>`;
        i++;
      } else if (line.trim().startsWith('|')) {
        const rows = [];
        for (; i < lines.length && lines[i].trim().startsWith('|'); i++) {
          rows.push(lines[i].trim().replace(/^\||\|$/g, '').split('|').map((c) => c.trim()));
        }
        const body = rows.slice(2).map((r) => '<tr>' + r.map((c) => `<td>${inline(c)}</td>`).join('') + '</tr>').join('');
        html += '<table><thead><tr>' + rows[0].map((c) => `<th>${inline(c)}</th>`).join('') + `</tr></thead><tbody>${body}</tbody></table>`;
      } else if (isItem(line)) {
        const tag = /^\s*\d+\./.test(line) ? 'ol' : 'ul';
        const items = [];
        for (; i < lines.length && lines[i].trim() && (isItem(lines[i]) || /^\s+\S/.test(lines[i])); i++) {
          if (isItem(lines[i])) items.push(lines[i].replace(/^\s*([-*+]|\d+\.)\s+/, ''));
          else items[items.length - 1] += ' ' + lines[i].trim();
        }
        html += `<${tag}>` + items.map((it) => `<li>${inline(it)}</li>`).join('') + `</${tag}>`;
      } else {
        const para = [];
        for (; i < lines.length && lines[i].trim() && !/^(#{1,6}\s|\s*```|\s*\|)/.test(lines[i]) && !isItem(lines[i]); i++) para.push(lines[i].trim());
        html += `<p>${inline(para.join(' '))}</p>`;
      }
    }
    return `<article class="md">${html}</article>`;
  }

  /* ------------------------------------------------------------ csv table */
  function renderCsvTable(text) {
    const rows = text.replace(/\n$/, '').split('\n').map((l) => splitCsv(l).map((c) => c.replace(/^"|"$/g, '')));
    const head = rows[0];
    const numeric = head.map((_, c) => rows.slice(1).every((r) => /^-?\d+(\.\d+)?$/.test(r[c] || '0')));
    const cls = (c, v) => (v === '' ? 'empty' : numeric[c] ? 'num' : '');
    return '<div class="csv-wrap"><table class="csv"><thead><tr><th class="rn"></th>' +
      head.map((h, c) => `<th class="${numeric[c] ? 'num' : ''}">${esc(h)}</th>`).join('') + '</tr></thead><tbody>' +
      rows.slice(1).map((r, n) => `<tr><td class="rn">${n + 1}</td>` +
        head.map((_, c) => `<td class="${cls(c, r[c] || '')}">${esc(r[c] || '')}</td>`).join('') + '</tr>').join('') +
      '</tbody></table></div>';
  }

  /* ----------------------------------------------------------------- tabs */
  const activeTab = () => state.tabs.find((t) => t.id === state.activeId) || null;

  function openTab(kind, path, pin) {
    const file = files.get(path);
    if (!file) return;
    if (kind === 'diff' && file.status !== 'M' && file.status !== 'D') kind = 'file';
    if (kind === 'file' && file.status === 'D') kind = 'diff';
    const id = kind + ':' + path;
    let tab = state.tabs.find((t) => t.id === id);
    if (!tab) {
      tab = { id, kind, path, preview: !pin, rich: false };
      const slot = state.tabs.findIndex((t) => t.preview);
      if (!pin && slot >= 0) state.tabs[slot] = tab; else state.tabs.push(tab);
    } else if (pin) tab.preview = false;
    state.activeId = id;
    state.line = null;
    if (window.innerWidth <= 760) ui.sideOpen = false;
    render();
  }

  function closeTab(id) {
    const at = state.tabs.findIndex((t) => t.id === id);
    if (at < 0) return;
    state.tabs.splice(at, 1);
    if (state.activeId === id) {
      const next = state.tabs[Math.min(at, state.tabs.length - 1)];
      state.activeId = next ? next.id : null;
      state.line = null;
    }
    render();
  }

  /* --------------------------------------------------------------- render */
  function renderRepoTabs() {
    const idx = Math.max(0, REPOS.findIndex((r) => r.id === REPO.id));
    document.documentElement.dataset.tab = String(idx % 3);
    $('repotabs').innerHTML = '<span class="brand"><img src="logo.png" alt="" width="28" height="28">PythonMuse · VS Code practice</span><div class="rtabs" role="tablist" aria-label="Practice repositories">' +
      REPOS.map((r, i) => {
        const st = stateByRepo.get(r.id);
        const n = st ? st.done.size : 0;
        return `<button class="rtab c${i % 3} ${r.id === REPO.id ? 'active' : ''}" role="tab" aria-selected="${r.id === REPO.id}" data-repo="${esc(r.id)}" title="${esc(r.name)}">` +
          `${esc(r.tabLabel || r.name)}${r.chat.length ? `<span class="rcount">${n}/${r.chat.length}</span>` : ''}</button>`;
      }).join('') + '</div>';
  }

  /** Banner under the repo tabs: this is a mock-up, and here is the real repo. */
  function renderNotice() {
    const git = REPO.source || '';
    const web = git.replace(/\.git$/, '');
    const cmd = git ? 'git clone ' + git : '';
    $('notice').innerHTML = `<span class="n-tag">Training mock-up</span>` +
      '<span class="n-text">Simulated VS Code for practice. AI replies are prepared in advance and nothing you do here is saved.</span>' +
      (web ? `<span class="n-real">Real repo on GitHub: <a href="${esc(web)}" target="_blank" rel="noopener" title="${esc(web)}">${esc(web.replace(/^https:\/\/github\.com\//, ''))}</a></span>` +
        `<button class="n-copy" data-copy="${esc(cmd)}" title="${esc(cmd)}"><code>git clone</code><span class="n-copied">Copy</span></button>` : '');
  }

  function renderTitlebar() {
    $('titlebar').innerHTML =
      `<div class="title-left"><span class="mark">${ICON.mark}</span><span class="pill">Practice copy</span></div>` +
      `<div class="command-center">${esc(REPO.name)}</div>` +
      '<div class="title-right">' +
      `<button class="icon-btn ${ui.chatOpen ? 'on' : ''}" data-act="chat" title="Toggle chat (Ctrl+Alt+I)" aria-label="Toggle chat">${ICON.spark}</button>` +
      `<button class="icon-btn ${ui.sideOpen ? 'on' : ''}" data-act="side" title="Toggle sidebar (Ctrl+B)" aria-label="Toggle sidebar">${ICON.side}</button>` +
      `<button class="icon-btn ${ui.panelOpen ? 'on' : ''}" data-act="panel" title="Toggle terminal (Ctrl+\`)" aria-label="Toggle terminal">${ICON.panel}</button>` +
      `<button class="icon-btn" data-act="theme" title="Switch light / dark theme" aria-label="Switch theme">${ICON.theme}</button>` +
      '</div>';
  }

  function renderActivity() {
    const btn = (view, label, icon, badge) =>
      `<button class="act-btn ${state.view === view && ui.sideOpen ? 'active' : ''}" data-view="${view}" title="${label}" aria-label="${label}">${icon}${badge || ''}</button>`;
    $('activitybar').innerHTML =
      btn('explorer', 'Explorer (Ctrl+Shift+E)', ICON.explorer) +
      btn('scm', `Source Control (Ctrl+Shift+G): ${changes.length} pending changes`, ICON.scm, changes.length ? `<span class="badge">${changes.length}</span>` : '');
  }

  function treeHtml() {
    const root = { dirs: new Map(), files: [] };
    for (const f of files.values()) {
      const parts = f.path.split('/');
      let node = root;
      parts.slice(0, -1).forEach((part) => {
        if (!node.dirs.has(part)) node.dirs.set(part, { dirs: new Map(), files: [], changed: false });
        node = node.dirs.get(part);
        if (f.status) node.changed = true;
      });
      node.files.push(f);
    }
    const tab = activeTab();
    const byName = (x, y) => x.localeCompare(y, 'en', { sensitivity: 'base' });
    const walk = (node, prefix, depth) => {
      let html = '';
      for (const name of [...node.dirs.keys()].sort(byName)) {
        const path = prefix + name;
        const dir = node.dirs.get(name);
        const open = !state.collapsed.has(path);
        html += `<button class="row folder" data-dir="${esc(path)}" style="--d:${depth}" aria-expanded="${open}">` +
          `<span class="twist">${open ? ICON.down : ICON.right}</span><span class="name ${dir.changed ? 's-M' : ''}">${esc(name)}</span>` +
          (dir.changed ? '<span class="stat s-M" title="Contains changes"><span class="dot"></span></span>' : '') + '</button>';
        if (open) html += walk(dir, path + '/', depth + 1);
      }
      for (const f of node.files.slice().sort((x, y) => byName(baseName(x.path), baseName(y.path)))) {
        html += `<button class="row file ${tab && tab.path === f.path ? 'active' : ''}" data-file="${esc(f.path)}" style="--d:${depth}">` +
          `${fileIcon(f.path)}<span class="name s-${f.status}">${esc(baseName(f.path))}</span>` +
          (f.status ? `<span class="stat s-${f.status}" title="${STATUS_NAME[f.status]}">${f.status}</span>` : '') + '</button>';
      }
      return html;
    };
    return `<div class="section-title">${ICON.down}${esc(REPO.name)}</div>` + walk(root, '', 0);
  }

  function scmHtml() {
    const tab = activeTab();
    const rows = changes.map((f) =>
      `<button class="row file ${tab && tab.path === f.path ? 'active' : ''}" data-change="${esc(f.path)}" style="--d:0" title="${esc(f.path)} • ${STATUS_NAME[f.status]}">` +
      `${fileIcon(f.path)}<span class="name s-${f.status}">${esc(baseName(f.path))}</span><span class="dir">${esc(dirName(f.path))}</span>` +
      `<span class="stat s-${f.status}">${f.status}</span></button>`).join('');
    return '<div class="scm-box">' +
      `<textarea rows="2" readonly aria-label="Commit message">${esc(REPO.commitMessage)}</textarea>` +
      `<button class="commit-btn" disabled>${ICON.check}Commit</button>` +
      '<div class="hint">Nothing here can be committed. Select a file below to compare the working tree with the last commit.</div></div>' +
      `<div class="section-title">${ICON.down}Changes<span class="count">${changes.length}</span></div>${rows}`;
  }

  function renderSidebar() {
    $('side-head').textContent = state.view === 'scm' ? 'Source Control' : 'Explorer';
    $('side-body').innerHTML = state.view === 'scm' ? scmHtml() : treeHtml();
  }

  /** True when another file in this repo has the same name (README.md, etc.), so tabs show the folder. */
  function isDupName(path) {
    const n = baseName(path);
    let c = 0;
    for (const k of files.keys()) if (baseName(k) === n && ++c > 1) return true;
    return false;
  }

  function renderTabs() {
    $('tabs').innerHTML = state.tabs.map((t) => {
      const f = files.get(t.path);
      const label = baseName(t.path) + (t.kind === 'diff' ? ' (Working Tree)' : '');
      const where = isDupName(t.path) ? `<span class="where">${esc(dirName(t.path) || 'repo root')}</span>` : '';
      return `<div class="tab ${t.id === state.activeId ? 'active' : ''} ${t.preview ? 'preview' : ''}" data-tab="${esc(t.id)}" role="tab" tabindex="0" aria-selected="${t.id === state.activeId}" title="${esc(t.path)}">` +
        `${fileIcon(t.path)}<span class="label s-${f.status}">${esc(label)}</span>${where}` +
        (f.status ? `<span class="stat s-${f.status}">${f.status}</span>` : '') +
        `<button class="x" data-close="${esc(t.id)}" aria-label="Close ${esc(label)}">${ICON.close}</button></div>`;
    }).join('');

    const tab = activeTab();
    const actions = [];
    if (tab) {
      const f = files.get(tab.path);
      const lang = langOf(tab.path);
      if (tab.kind === 'file' && lang === 'markdown') actions.push(['rich', tab.rich ? 'Show Source' : 'Open Preview']);
      if (tab.kind === 'file' && lang === 'csv') actions.push(['rich', tab.rich ? 'Show Text' : 'Show Table']);
      if (tab.kind === 'diff' && f.kind === 'text') actions.push(['inline', diffIsInline(f) ? 'Side by Side' : 'Inline']);
      if (tab.kind === 'file' && f.status === 'M') actions.push(['changes', 'Open Changes']);
      if (tab.kind === 'diff') actions.push(['file', 'Open File']);
    }
    $('actions').innerHTML = actions.map(([act, label]) => `<button class="text-btn" data-edit="${act}">${label}</button>`).join('');
  }

  function renderEditor() {
    const tab = activeTab();
    const editor = $('editor');
    const crumbs = $('breadcrumbs');
    if (!tab) {
      crumbs.innerHTML = '';
      const start = [['README.md', 'Read the README'], [[...files.keys()].find((p) => p.endsWith('SKILL.md')), 'Open a skill'], [changes[0] && changes[0].path, 'See what changed']]
        .filter(([p]) => p && files.has(p));
      editor.innerHTML = `<div class="welcome"><div><h1>${esc(REPO.name)}</h1><p>A practice copy of this repository. Browse it the way you would in VS Code, and use the chat on the right to run the prepared prompts.</p>` +
        start.map(([p, label], n) => `<button data-${n === 2 ? 'change' : 'file'}="${esc(p)}">${fileIcon(p)}${label}: ${esc(baseName(p))}</button>`).join('') +
        '<div class="keys"><span>Explorer</span><span><kbd>Ctrl</kbd> <kbd>Shift</kbd> <kbd>E</kbd></span><span>Source Control</span><span><kbd>Ctrl</kbd> <kbd>Shift</kbd> <kbd>G</kbd></span>' +
        '<span>Toggle sidebar</span><span><kbd>Ctrl</kbd> <kbd>B</kbd></span><span>Toggle terminal</span><span><kbd>Ctrl</kbd> <kbd>`</kbd></span>' +
        '<span>Toggle chat</span><span><kbd>Ctrl</kbd> <kbd>Alt</kbd> <kbd>I</kbd></span></div></div></div>';
      return;
    }
    const f = files.get(tab.path);
    let meta = '';
    let html;
    const fig = (cls, src, label, alt) => src === undefined
      ? `<figure class="${cls} gone"><figcaption>${label}</figcaption><div class="gone-note">File deleted</div></figure>`
      : `<figure class="${cls}"><figcaption>${label}</figcaption><img src="${esc(src)}" alt="${esc(baseName(f.path))} ${alt}"></figure>`;
    const sheet = (data) => (window.renderSheet ? window.renderSheet(data, esc) : '<div class="gone-note">Spreadsheet preview unavailable.</div>');
    if (tab.kind === 'diff' && f.kind === 'image') {
      html = '<div class="image-diff">' + fig('old', f.head, '<b>HEAD</b> last commit', 'at the last commit') +
        fig('new', f.working, '<b>Working tree</b> after the AI’s changes', 'in the working tree') + '</div>';
    } else if (f.kind === 'sheet') {
      const gone = f.working === undefined;
      const note = tab.kind === 'diff'
        ? `<div class="sheet-note">${gone ? 'Deleted in the working tree. Showing the last committed version.' : 'Workbook changed. Showing the working-tree version.'}</div>` : '';
      html = note + sheet(gone ? f.head : f.working);
    } else if (tab.kind === 'diff') {
      const d = renderDiff(f, diffIsInline(f));
      html = d.html;
      meta = `<span class="meta"><span class="plus">+${d.added}</span><span class="minus">-${d.removed}</span></span>`;
    } else if (f.kind === 'image') {
      html = `<div class="image-view"><img src="${esc(f.working)}" alt="${esc(baseName(f.path))}"></div>`;
    } else if (tab.rich && langOf(f.path) === 'markdown') {
      html = renderMarkdown(f.working, f.path);
    } else if (tab.rich && langOf(f.path) === 'csv') {
      html = renderCsvTable(f.working);
    } else {
      html = '<div class="code">' + tokenize(f.path, f.working).map((toks, n) =>
        `<div class="line ${state.line === n + 1 ? 'cur' : ''}" data-ln="${n + 1}"><span class="ln">${n + 1}</span><span class="lc">${lineHtml(toks)}</span></div>`).join('') + '</div>';
    }
    const parts = tab.path.split('/');
    crumbs.innerHTML = parts.map((p, n) => `<span class="${n === parts.length - 1 ? 'last' : ''}">${esc(p)}</span>`).join(`<span class="sep">${ICON.right}</span>`) +
      (tab.kind === 'diff' ? `<span class="sep">${ICON.right}</span><span>HEAD ↔ Working Tree</span>` : '') + meta;
    editor.innerHTML = html;
    editor.scrollTop = 0;
    editor.scrollLeft = 0;
  }

  function renderPanel() {
    const lines = state.terminal.map((t) =>
      `<span class="prompt">${esc(REPO.name)} $</span> <span class="cmd">${esc(t.command)}</span>\n${t.output ? esc(t.output) + '\n' : ''}`).join('\n');
    $('panel').innerHTML = `<div class="panel-head"><span class="ptab">Terminal</span><button class="icon-btn" data-act="panel" aria-label="Close terminal" title="Close terminal">${ICON.close}</button></div>` +
      `<pre class="terminal">${lines}\n<span class="prompt">${esc(REPO.name)} $</span> </pre>`;
  }

  function renderStatus() {
    const tab = activeTab();
    let right = '';
    if (tab) {
      const f = files.get(tab.path);
      if (f.kind === 'text' && f.working !== undefined) {
        const count = f.working.replace(/\n$/, '').split('\n').length;
        right += `<span class="item">${state.line && tab.kind === 'file' && !tab.rich ? 'Ln ' + state.line + ' of ' + count : count + ' lines'}</span><span class="item wide">UTF-8</span>`;
      }
      right += `<span class="item">${LANG_LABEL[langOf(tab.path)]}</span>`;
    }
    $('statusbar').innerHTML =
      `<button class="item remote" data-view="scm" title="Source Control">${ICON.branch}${esc(REPO.branch)}${changes.length ? '*' : ''}</button>` +
      `<button class="item" data-view="scm" title="Pending changes">${changes.length} changes</button>` +
      `<button class="item" data-act="panel" title="Toggle terminal (Ctrl+\`)">${ICON.terminal}Terminal</button>` +
      `<span class="right">${right}</span>`;
  }

  function fileHash(kind, path) {
    return '#repo=' + encodeURIComponent(REPO.id) + (path ? '&' + kind + '=' + encodeURI(path) : '');
  }

  function render() {
    const app = $('app');
    app.classList.toggle('side-closed', !ui.sideOpen);
    app.classList.toggle('panel-open', ui.panelOpen);
    app.classList.toggle('chat-closed', !ui.chatOpen);
    renderRepoTabs();
    renderNotice();
    renderTitlebar();
    renderActivity();
    renderSidebar();
    renderTabs();
    renderEditor();
    renderStatus();
    const tab = activeTab();
    const hash = tab ? fileHash(tab.kind, tab.path) : fileHash();
    if (location.hash !== hash) history.replaceState(null, '', hash);
    document.title = (tab ? baseName(tab.path) + ' - ' : '') + REPO.name;
  }

  /* ----------------------------------------------------------------- chat
     Each step in REPO.chat is a prepared prompt + response. Running one adds
     the reply to the conversation and applies its file changes to this repo's
     working tree, so they show up in Explorer and Source Control. */
  const stepById = (id) => REPO.chat.find((s) => s.id === id) || null;
  const stepPaths = (step) => [...step.files.map((f) => f.path), ...(step.deletes || [])];
  const FALLBACK = 'This practice copy only answers the **prepared prompts** for this repository, so everyone sees the same result. ' +
    'Pick one under **Suggested prompts** below, or type something closer to one of them.';

  function statusOf(f) {
    if (f.head === undefined) return 'U';
    if (f.working === undefined) return 'D';
    const same = f.kind === 'sheet' ? JSON.stringify(f.head) === JSON.stringify(f.working) : f.head === f.working;
    return same ? '' : 'M';
  }

  function applyStep(step, st) {
    for (const nf of step.files) {
      let f = st.files.get(nf.path);
      if (!f) { f = { path: nf.path, kind: nf.kind }; st.files.set(nf.path, f); }
      f.kind = nf.kind;
      f.working = nf.kind === 'image' ? nf.url : nf.kind === 'sheet' ? nf.sheets : nf.content;
      f.status = statusOf(f);
    }
    for (const path of step.deletes || []) {
      const f = st.files.get(path);
      if (!f) continue;
      if (f.head === undefined) st.files.delete(path);
      else { f.working = undefined; f.status = 'D'; }
    }
    st.tabs = st.tabs.filter((t) => st.files.has(t.path));
    if (!st.tabs.some((t) => t.id === st.activeId)) st.activeId = st.tabs.length ? st.tabs[st.tabs.length - 1].id : null;
    st.terminal.push(...(step.terminal || []));
    st.done.add(step.id);
  }

  const STOP = new Set('the and for with this that these those are was were you your can could would should please what how why which into from about then them their there have has had will just its our out all any not but use using'.split(' '));
  const wordsOf = (s) => new Set((s.toLowerCase().match(/[a-z0-9_./-]+/g) || []).filter((w) => w.length > 2 && !STOP.has(w)));

  /** The prepared step closest to free-typed text, or null below `min`. */
  function matchStep(text, min) {
    const q = wordsOf(text);
    if (!q.size) return null;
    let best = null, score = 0;
    for (const step of REPO.chat) {
      const p = wordsOf(step.title + ' ' + step.prompt);
      let hit = 0;
      q.forEach((w) => { if (p.has(w)) hit++; });
      const sc = (hit / q.size) * Math.min(1, hit / 2);
      if (sc > score) { score = sc; best = step; }
    }
    return score >= min ? best : null;
  }

  function msgHtml(m, idx) {
    const who = (icon, name) => `<div class="who">${icon}<span>${name}</span></div>`;
    if (m.role === 'user') {
      const long = m.text.length > 420;
      return `<div class="msg user">${who(ICON.user, 'You')}<div class="bubble ${long && !m.expanded ? 'clamped' : ''}">${esc(m.text)}</div>` +
        (long ? `<button class="more" data-expand="${idx}">${m.expanded ? 'Show less' : 'Show full prompt'}</button>` : '') + '</div>';
    }
    if (m.pending) {
      return `<div class="msg ai">${who(ICON.spark, 'Copilot')}<div class="thinking"><span class="dots"><i></i><i></i><i></i></span>${esc(m.status || 'Working…')}</div></div>`;
    }
    const step = m.step ? stepById(m.step) : null;
    let html = `<div class="msg ai">${who(ICON.spark, 'Copilot')}<div class="ai-body ${m.fresh ? 'fresh' : ''}">${renderMarkdown(step ? step.response : m.text, '')}`;
    if (step && step.block) {
      html += `<div class="block-card">${ICON.lock}<div><b>Blocked by a PreToolUse hook</b><pre>${esc(step.block)}</pre></div></div>`;
    }
    if (step && step.terminal && step.terminal.length) {
      html += `<button class="term-chip" data-act="panel-open">${ICON.terminal}Ran ${step.terminal.length} command${step.terminal.length > 1 ? 's' : ''} in the terminal</button>`;
    }
    if (step && stepPaths(step).length) {
      const rows = stepPaths(step).map((p) => {
        const f = files.get(p);
        const st = f ? f.status : '';
        return `<button class="fc-row" data-change="${esc(p)}" title="${esc(p)}">${fileIcon(p)}<span class="name s-${st}">${esc(baseName(p))}</span>` +
          `<span class="dir">${esc(dirName(p))}</span>${st ? `<span class="stat s-${st}">${st}</span>` : ''}</button>`;
      }).join('');
      const n = stepPaths(step).length;
      html += `<div class="files-card"><div class="fc-head"><span>${n} file${n > 1 ? 's' : ''} changed</span><button class="text-btn" data-act="scm">Review in Source Control</button></div>${rows}</div>`;
    }
    if (m.hint && stepById(m.hint)) html += `<button class="sg-inline" data-fill="${esc(m.hint)}">Try: ${esc(stepById(m.hint).title)}</button>`;
    return html + '</div></div>';
  }

  function renderChat() {
    $('chat-head').innerHTML = `<span class="chat-title">${ICON.spark}Chat</span><span class="chat-mode">Agent</span><span class="chat-spacer"></span>` +
      `<button class="icon-btn" data-act="reset" title="Reset this repository and its chat" aria-label="Reset this repository">${ICON.reset}</button>` +
      `<button class="icon-btn" data-act="chat" title="Close chat (Ctrl+Alt+I)" aria-label="Close chat">${ICON.close}</button>`;

    const body = $('chat-body');
    const keepTop = body.scrollTop;   // a re-render (opening a file, expanding a block) must not jump the reader
    body.innerHTML = state.chat.length ? state.chat.map(msgHtml).join('') :
      `<div class="chat-empty">${ICON.spark}<h2>Practice prompts</h2>` +
      '<p>Pick a prompt below, read it, then press <b>Send</b>. The replies are prepared in advance, so everyone gets the same result.</p>' +
      '<p class="dim">When the AI changes files, they appear in Explorer and Source Control so you can review exactly what it did.</p></div>';
    body.querySelectorAll('.ai-body.fresh > .md > *, .ai-body.fresh > :not(.md)').forEach((el, i) => { el.style.animationDelay = i * 70 + 'ms'; });
    body.scrollTop = keepTop;
    state.chat.forEach((m) => { m.fresh = false; });

    const next = REPO.chat.find((s) => !state.done.has(s.id));
    $('chat-suggest').innerHTML = !REPO.chat.length ? '' :
      `<button class="sg-head" data-act="suggest" aria-expanded="${ui.suggestOpen}">${ui.suggestOpen ? ICON.down : ICON.right}Suggested prompts` +
      `<span class="count">${state.done.size}/${REPO.chat.length}</span></button>` +
      (ui.suggestOpen ? '<div class="sg-list">' + REPO.chat.map((s, n) =>
        `<button class="sg ${state.done.has(s.id) ? 'done' : ''} ${next === s ? 'next' : ''} ${state.fillId === s.id ? 'picked' : ''}" data-fill="${esc(s.id)}" title="${esc(s.prompt.slice(0, 280))}">` +
        `<span class="sg-n">${state.done.has(s.id) ? ICON.check : n + 1}</span><span class="sg-t">${esc(s.title)}</span></button>`).join('') + '</div>' : '');
    $('chat-send').disabled = state.busy;
  }

  function scrollChat() {
    const body = $('chat-body');
    const last = body.querySelector('.msg.ai:last-child');
    // a long reply opens at its first line; offsetTop is relative to #chat (not the scroller), so measure against the scroller's own box
    if (last && last.offsetHeight > body.clientHeight) body.scrollTop += last.getBoundingClientRect().top - body.getBoundingClientRect().top - 8;
    else body.scrollTop = body.scrollHeight;
  }

  function autosize() {
    const t = $('chat-text');
    t.style.height = 'auto';
    t.style.height = Math.min(t.scrollHeight, 220) + 'px';
  }

  function fill(id) {
    const step = stepById(id);
    if (!step || state.busy) return;
    ui.chatOpen = true;
    state.fillId = id;
    $('chat-text').value = step.prompt;
    autosize();
    render();
    renderChat();
    $('chat-text').focus();
    $('chat-text').scrollTop = 0;
  }

  function send() {
    const text = $('chat-text').value.trim();
    if (!text || state.busy) return;
    const picked = stepById(state.fillId);
    const step = picked && picked.prompt.trim() === text ? picked : matchStep(text, 0.5);
    const st = state;   // the reply lands in this repo even if the reader switches tabs meanwhile
    st.fillId = null;
    st.draft = '';
    $('chat-text').value = '';
    autosize();
    st.chat.push({ role: 'user', text });
    const msg = { role: 'ai', pending: true, status: 'Reading the workspace…' };
    st.chat.push(msg);
    st.busy = true;
    renderChat();
    scrollChat();
    const later = step && (step.files.length || (step.deletes || []).length) ? 'Editing files…'
      : step && step.terminal && step.terminal.length ? 'Running commands…' : 'Thinking…';
    setTimeout(() => { msg.status = later; if (st === state) renderChat(); }, 700);
    setTimeout(() => {
      msg.pending = false;
      msg.fresh = true;
      st.busy = false;
      if (step) {
        msg.step = step.id;
        applyStep(step, st);
      } else {
        msg.text = FALLBACK;
        const near = matchStep(text, 0.12);
        if (near) msg.hint = near.id;
      }
      if (st !== state) return;
      recompute();
      if (step && step.terminal && step.terminal.length) ui.panelOpen = true;
      render();
      renderPanel();
      renderChat();
      scrollChat();
    }, step ? 1500 + Math.min(1200, step.response.length / 4) : 900);
  }

  function resetRepo() {
    if (!window.confirm(`Reset “${REPO.tabLabel || REPO.name}”? This clears the chat and undoes every file change the AI made.`)) return;
    const fresh = freshState(REPO);
    stateByRepo.set(REPO.id, fresh);
    state = fresh;
    files = fresh.files;
    recompute();
    $('chat-text').value = '';
    autosize();
    renderPanel();
    renderChat();
    if (files.has('README.md')) openTab('file', 'README.md', true); else render();
  }

  function switchRepo(id) {
    if (id === REPO.id) return;
    loadRepo(id);
    autosize();
    renderPanel();
    renderChat();
    scrollChat();
    if (!state.tabs.length && files.has('README.md')) openTab('file', 'README.md', true); else render();
  }

  /* --------------------------------------------------------------- events */
  function setView(view) {
    if (state.view === view && ui.sideOpen) ui.sideOpen = false;
    else { state.view = view; ui.sideOpen = true; }
    render();
  }

  function act(name) {
    if (name === 'side') { ui.sideOpen = !ui.sideOpen; if (ui.sideOpen && narrow()) ui.chatOpen = false; }
    if (name === 'panel') ui.panelOpen = !ui.panelOpen;
    if (name === 'panel-open') ui.panelOpen = true;
    if (name === 'chat') { ui.chatOpen = !ui.chatOpen; if (ui.chatOpen && narrow()) ui.sideOpen = false; }
    if (name === 'scm') { state.view = 'scm'; ui.sideOpen = true; if (narrow()) ui.chatOpen = false; }
    if (name === 'suggest') { ui.suggestOpen = !ui.suggestOpen; return renderChat(); }
    if (name === 'send') return send();
    if (name === 'reset') return resetRepo();
    if (name === 'theme') {
      const next = document.documentElement.dataset.theme === 'light' ? 'dark' : 'light';
      document.documentElement.dataset.theme = next;
      try { localStorage.setItem('code-demo-theme', next); } catch (e) { /* private mode: keep for this visit only */ }
    }
    render();
  }

  function onClick(e, pin) {
    const hit = (attr) => { const el = e.target.closest(`[data-${attr}]`); return el ? el.dataset[attr] : null; };
    let v;
    if ((v = hit('repo'))) return switchRepo(v);
    if ((v = hit('copy'))) {
      const label = e.target.closest('[data-copy]').querySelector('.n-copied');
      const done = () => { label.textContent = 'Copied'; setTimeout(() => { label.textContent = 'Copy'; }, 1500); };
      try { navigator.clipboard.writeText(v).then(done, () => { label.textContent = 'Select & copy'; }); } catch (err) { label.textContent = 'Select & copy'; }
      return;
    }
    if ((v = hit('fill'))) return fill(v);
    if ((v = hit('expand'))) { const m = state.chat[Number(v)]; m.expanded = !m.expanded; return renderChat(); }
    if ((v = hit('close'))) return closeTab(v);
    if ((v = hit('open'))) { e.preventDefault(); if (narrow()) ui.chatOpen = false; return openTab('file', v, true); }
    if ((v = hit('file'))) return openTab('file', v, pin);
    if ((v = hit('change'))) { if (narrow()) ui.chatOpen = false; return openTab('diff', v, pin); }
    if ((v = hit('dir'))) {
      state.collapsed.has(v) ? state.collapsed.delete(v) : state.collapsed.add(v);
      return renderSidebar();
    }
    if ((v = hit('tab'))) {
      const tab = state.tabs.find((t) => t.id === v);
      if (pin) tab.preview = false;
      if (state.activeId !== v) { state.activeId = v; state.line = null; }
      return render();
    }
    if ((v = hit('view'))) return setView(v);
    if ((v = hit('act'))) return act(v);
    if ((v = hit('edit'))) {
      const tab = activeTab();
      if (v === 'rich') tab.rich = !tab.rich;
      if (v === 'inline') state.diffMode = diffIsInline(files.get(tab.path)) ? 'split' : 'inline';
      if (v === 'changes') return openTab('diff', tab.path, !tab.preview);
      if (v === 'file') return openTab('file', tab.path, !tab.preview);
      return render();
    }
    if ((v = hit('ln'))) {
      if (String(window.getSelection())) return;
      state.line = Number(v);
      document.querySelectorAll('.code .line.cur').forEach((el) => el.classList.remove('cur'));
      e.target.closest('.line').classList.add('cur');
      renderStatus();
    }
  }

  // A double click keeps the tab open (single clicks reuse one italic "preview" tab).
  // e.detail is the click count; a dblclick listener would miss it because the first
  // click already redrew the row.
  document.addEventListener('click', (e) => onClick(e, e.detail >= 2));
  document.addEventListener('auxclick', (e) => {
    const tab = e.button === 1 && e.target.closest('[data-tab]');
    if (tab) { e.preventDefault(); closeTab(tab.dataset.tab); }
  });
  document.addEventListener('keydown', (e) => {
    const mod = e.ctrlKey || e.metaKey;
    const key = e.key.toLowerCase();
    if (e.target.id === 'chat-text' && e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); }
    else if (e.key === 'Enter' && e.target.matches && e.target.matches('[data-tab]')) e.target.click();
    else if (mod && e.altKey && key === 'i') { e.preventDefault(); act('chat'); if (ui.chatOpen) $('chat-text').focus(); }
    else if (mod && e.shiftKey && key === 'e') { e.preventDefault(); state.view = 'explorer'; ui.sideOpen = true; render(); }
    else if (mod && e.shiftKey && key === 'g') { e.preventDefault(); state.view = 'scm'; ui.sideOpen = true; render(); }
    else if (mod && !e.shiftKey && !e.altKey && key === 'b') { e.preventDefault(); act('side'); }
    else if (mod && e.key === '`') { e.preventDefault(); act('panel'); }
  });
  $('chat-text').addEventListener('input', () => {
    autosize();
    // Editing a picked prompt turns it into free text, matched by wording instead.
    const picked = stepById(state.fillId);
    if (picked && $('chat-text').value.trim() !== picked.prompt.trim()) { state.fillId = null; renderChat(); }
  });

  /** #repo=<id>&file=<path> or #repo=<id>&diff=<path>; the old #file=... form opens the first repo. */
  function openFromHash() {
    const m = /^#(?:repo=([^&]*))?&?(?:(file|diff)=(.+))?$/.exec(location.hash);
    if (!m || (!m[1] && !m[2])) return false;
    if (m[1] && decodeURIComponent(m[1]) !== REPO.id && REPOS.some((r) => r.id === decodeURIComponent(m[1]))) {
      loadRepo(decodeURIComponent(m[1]));
      renderPanel();
      renderChat();
    }
    const path = m[3] && decodeURI(m[3]);
    if (!path || !files.has(path)) return false;
    if (m[2] === 'diff') state.view = 'scm';
    openTab(m[2], path, true);
    return true;
  }
  window.addEventListener('hashchange', openFromHash);

  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      const tab = activeTab();
      if (tab && tab.kind === 'diff' && state.diffMode === 'auto') { renderTabs(); renderEditor(); }
    }, 120);
  });

  if (!REPOS.length) {
    document.body.textContent = 'No repositories found. Run python tools/build.py to generate public/repo-data.js.';
    return;
  }
  loadRepo(REPOS[0].id);
  renderPanel();
  renderChat();
  if (!openFromHash()) {
    if (files.has('README.md')) openTab('file', 'README.md', true); else render();
  }
})();
