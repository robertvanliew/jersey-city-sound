// Place pages: load Leaflet and an OpenStreetMap tile layer only when the reader asks for
// the map, so no third-party request happens on page load. Pin and label come from the
// .place-map element's data attributes.
(function () {
  var box = document.querySelector('.place-map');
  if (!box) return;
  var btn = box.querySelector('[data-act="show-map"]');
  if (!btn) return;
  function load(src, isCss) {
    return new Promise(function (res, rej) {
      var el = isCss ? document.createElement('link') : document.createElement('script');
      if (isCss) { el.rel = 'stylesheet'; el.href = src; } else { el.src = src; el.defer = true; }
      el.onload = res; el.onerror = rej;
      document.head.appendChild(el);
    });
  }
  btn.addEventListener('click', function () {
    btn.disabled = true; btn.textContent = 'Loading map…';
    var lat = parseFloat(box.getAttribute('data-lat')), lng = parseFloat(box.getAttribute('data-lng'));
    Promise.all([
      load('https://unpkg.com/leaflet@1.9.4/dist/leaflet.css', true),
      load('https://unpkg.com/leaflet@1.9.4/dist/leaflet.js', false)
    ]).then(function () {
      var div = document.createElement('div');
      div.className = 'place-map__canvas';
      div.setAttribute('aria-label', 'Map: ' + box.getAttribute('data-name'));
      box.insertBefore(div, btn);
      btn.remove();
      var map = L.map(div, { scrollWheelZoom: false }).setView([lat, lng], 16);
      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19, attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(map);
      L.marker([lat, lng]).addTo(map).bindPopup(box.getAttribute('data-name')).openPopup();
    }).catch(function () { btn.disabled = false; btn.textContent = 'Map unavailable'; });
  });
})();
