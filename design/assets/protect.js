/* Casual-save deterrent for images: blocks the right-click menu and drag-to-save
   on <img> elements (and gallery/emblem figures). This is a speed bump, NOT real
   protection — screenshots, DevTools, the direct image URL, and the browser cache
   all still work and cannot be prevented. The real safeguards are the CC BY-SA
   license, visible provenance (the record seals), and watermarking. */
(function () {
  function onImage(t) {
    return t && (t.tagName === 'IMG' ||
      (t.closest && t.closest('.slide, .entry-emblem, figure')));
  }
  document.addEventListener('contextmenu', function (e) {
    if (onImage(e.target)) e.preventDefault();
  });
  document.addEventListener('dragstart', function (e) {
    if (e.target && e.target.tagName === 'IMG') e.preventDefault();
  });
})();
