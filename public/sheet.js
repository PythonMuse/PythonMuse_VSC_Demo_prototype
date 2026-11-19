/* Spreadsheet preview: window.renderSheet(sheets, esc) -> html.
   sheets = [{name, rows: [[null | {v, f?}, ...], ...]}]. Interaction is delegated on document,
   so it works no matter who inserts the markup. */
(function () {
  'use strict';

  const DEFAULT_NOTE = 'Click a cell to see its formula';

  function colName(i) {
    let s = '';
    for (let n = i + 1; n > 0; n = Math.floor((n - 1) / 26)) s = String.fromCharCode(65 + ((n - 1) % 26)) + s;
    return s;
  }

  function display(v) {
    if (v === null || v === undefined) return '';
    if (typeof v === 'boolean') return v ? 'TRUE' : 'FALSE';
    if (typeof v === 'number') return Number.isFinite(v) ? v.toLocaleString('en-US', { maximumFractionDigits: 2 }) : String(v);
    return String(v);
  }

  function norm(cell) {
    if (cell === null || cell === undefined) return null;
    if (typeof cell === 'object') return cell;
    return { v: cell };
  }

  function paneHtml(sheet, index, esc) {
    const rows = (sheet && sheet.rows) || [];
    const cols = rows.reduce((m, r) => Math.max(m, (r || []).length), 0);
    let h = `<div class="sheet-pane" data-sheet-index="${index}"${index ? ' hidden' : ''}>` +
      `<div class="sheet-fbar"><span class="sheet-ref">&nbsp;</span><span class="sheet-fx">fx</span>` +
      `<span class="sheet-formula dim" data-default="${esc(DEFAULT_NOTE)}">${esc(DEFAULT_NOTE)}</span></div>` +
      '<div class="sheet-scroll"><table class="sheet"><thead><tr><th class="corner"></th>';
    for (let c = 0; c < cols; c++) h += `<th>${colName(c)}</th>`;
    h += '</tr></thead><tbody>';
    rows.forEach((row, r) => {
      h += `<tr><th class="rn">${r + 1}</th>`;
      for (let c = 0; c < cols; c++) {
        const cell = norm((row || [])[c]);
        const ref = colName(c) + (r + 1);
        if (!cell || (cell.v === undefined && !cell.f) || cell.v === null && !cell.f) {
          h += `<td data-ref="${ref}"></td>`;
          continue;
        }
        const f = cell.f ? String(cell.f) : '';
        const v = cell.v === undefined || cell.v === null ? f : cell.v;
        const cls = [typeof v === 'number' ? 'num' : '', typeof v === 'boolean' ? 'bool' : '', f ? 'fx' : ''].filter(Boolean).join(' ');
        h += `<td data-ref="${ref}"${cls ? ` class="${cls}"` : ''}${f ? ` data-f="${esc(f)}"` : ''}>${esc(display(v))}</td>`;
      }
      h += '</tr>';
    });
    return h + '</tbody></table></div></div>';
  }

  window.renderSheet = function (sheets, esc) {
    if (!Array.isArray(sheets) || !sheets.length) return '<div class="gone-note">This workbook has no sheets.</div>';
    const tabs = sheets.map((s, i) =>
      `<button class="sheet-tab${i ? '' : ' active'}" type="button" role="tab" aria-selected="${i === 0}" data-sheet-tab="${i}">${esc((s && s.name) || 'Sheet' + (i + 1))}</button>`).join('');
    return '<div class="sheet-wrap">' +
      '<div class="sheet-panes">' + sheets.map((s, i) => paneHtml(s, i, esc)).join('') + '</div>' +
      `<div class="sheet-tabs" role="tablist" aria-label="Sheets">${tabs}</div></div>`;
  };

  document.addEventListener('click', function (e) {
    const target = e.target;
    if (!target || !target.closest) return;

    const tab = target.closest('[data-sheet-tab]');
    if (tab) {
      const wrap = tab.closest('.sheet-wrap');
      if (!wrap) return;
      const idx = tab.getAttribute('data-sheet-tab');
      wrap.querySelectorAll('[data-sheet-tab]').forEach(function (b) {
        const on = b === tab;
        b.classList.toggle('active', on);
        b.setAttribute('aria-selected', on ? 'true' : 'false');
      });
      wrap.querySelectorAll('.sheet-pane').forEach(function (p) {
        p.hidden = p.getAttribute('data-sheet-index') !== idx;
      });
      return;
    }

    const td = target.closest('.sheet-wrap td[data-ref]');
    if (td) {
      const pane = td.closest('.sheet-pane');
      if (!pane) return;
      const prev = pane.querySelector('td.sel');
      if (prev) prev.classList.remove('sel');
      td.classList.add('sel');
      const f = td.getAttribute('data-f');
      const text = f || td.textContent;
      pane.querySelector('.sheet-ref').textContent = td.getAttribute('data-ref');
      const out = pane.querySelector('.sheet-formula');
      out.textContent = text;
      out.classList.toggle('dim', !text);
    }
  });
})();
