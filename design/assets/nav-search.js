// Masthead search — available on every page (not just the homepage/archive).
// Reuses window.JCS_ENTRIES from archive-data.js. Progressive enhancement:
// with no JS, the form still submits to archive.html?q=… for a full search.
(function () {
  function init() {
    var input = document.getElementById('nav-search');
    var box = document.getElementById('nav-suggest');
    var entries = window.JCS_ENTRIES || [];
    if (!input || !box || !entries.length) return;
    var form = input.closest('.nav-search');
    var icon = form && form.querySelector('svg');
    var active = -1;
    // pop-out: the collapsed magnifier opens the field; keep it open while it has focus/text
    function open() { if (form) form.classList.add('open'); input.focus(); }
    function close() { if (form && !input.value) form.classList.remove('open'); }
    if (icon) icon.addEventListener('click', function (ev) { ev.preventDefault(); open(); });
    input.addEventListener('blur', function () { setTimeout(close, 120); });
    // press "/" anywhere to summon search (unless already typing in a field)
    document.addEventListener('keydown', function (ev) {
      if (ev.key === '/' && !/^(INPUT|TEXTAREA|SELECT)$/.test((ev.target.tagName || '')) && !ev.target.isContentEditable) {
        ev.preventDefault(); open();
      }
    });
    function opts() { return box.querySelectorAll('a'); }
    function esc(s) { return String(s || '').replace(/[&<>]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]; }); }
    function highlight(i) {
      var o = opts();
      o.forEach(function (a, n) { a.classList.toggle('active', n === i); });
      if (i >= 0 && o[i]) o[i].scrollIntoView({ block: 'nearest' });
      active = i;
    }
    function render() {
      var term = input.value.trim().toLowerCase();
      active = -1;
      if (!term) { box.innerHTML = ''; input.setAttribute('aria-expanded', 'false'); return; }
      var hits = entries.filter(function (e) {
        return (e.name + ' ' + e.role + ' ' + e.no).toLowerCase().indexOf(term) !== -1;
      }).slice(0, 8);
      box.innerHTML = hits.map(function (e) {
        return '<li role="option"><a href="' + esc(e.href) + '"><span class="no">№. ' + esc(e.no) +
          '</span><span class="nm">' + esc(e.name) + '</span><span class="rl">' + esc(e.role) + '</span></a></li>';
      }).join('');
      input.setAttribute('aria-expanded', hits.length ? 'true' : 'false');
    }
    input.addEventListener('input', render);
    input.addEventListener('focus', render);
    document.addEventListener('click', function (ev) { if (!ev.target.closest('.nav-search')) box.innerHTML = ''; });
    input.addEventListener('keydown', function (ev) {
      var o = opts();
      if (ev.key === 'ArrowDown') { ev.preventDefault(); highlight(Math.min(active + 1, o.length - 1)); }
      else if (ev.key === 'ArrowUp') { ev.preventDefault(); highlight(Math.max(active - 1, 0)); }
      else if (ev.key === 'Enter') { if (active >= 0 && o[active]) { ev.preventDefault(); o[active].click(); } }
      else if (ev.key === 'Escape') { input.value = ''; box.innerHTML = ''; input.blur(); if (form) form.classList.remove('open'); }
    });
  }
  if (window.JCS_ENTRIES) init();
  else document.addEventListener('DOMContentLoaded', init);
})();
