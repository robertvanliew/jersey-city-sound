// Progressive form UX for The Jersey City Sound.
// 1) Any <form data-ajax> posts to Formspree in the background (Accept: JSON)
//    and shows an in-page confirmation popup — the visitor never leaves the
//    archive or sees the Formspree page.
// 2) Any [data-contact] trigger opens a branded contact modal instead of a
//    mailto: handoff.
(function () {
  var ENDPOINT = 'https://formspree.io/f/mlgyqylz';

  // ---- confirmation popup (the "it was sent" moment) --------------------
  function popup(msg, ok) {
    var w = document.createElement('div');
    w.className = 'popup';
    w.innerHTML =
      '<div class="popup__backdrop" data-close></div>' +
      '<div class="popup__card" role="alertdialog" aria-live="assertive">' +
      '<span class="popup__mark' + (ok ? '' : ' popup__mark--err') + '">' + (ok ? '&#10003;' : '!') + '</span>' +
      '<p class="popup__msg"></p>' +
      '<button class="btn-ink" data-close>Close</button></div>';
    w.querySelector('.popup__msg').textContent = msg;
    document.body.appendChild(w);
    requestAnimationFrame(function () { w.classList.add('is-in'); });
    function close() { w.classList.remove('is-in'); setTimeout(function () { w.remove(); }, 300); }
    w.addEventListener('click', function (e) { if (e.target.hasAttribute('data-close')) close(); });
    document.addEventListener('keydown', function esc(e) {
      if (e.key === 'Escape') { close(); document.removeEventListener('keydown', esc); }
    });
    if (ok) setTimeout(close, 5200);
  }

  // ---- AJAX submission --------------------------------------------------
  function ajaxify(form) {
    if (form.__ajax) return;
    form.__ajax = true;
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var btn = form.querySelector('[type=submit]');
      var label = btn ? btn.textContent : '';
      if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }
      fetch(form.getAttribute('action') || ENDPOINT, {
        method: 'POST',
        body: new FormData(form),
        headers: { 'Accept': 'application/json' }
      }).then(function (r) {
        if (r.ok) {
          form.reset();
          if (form.hasAttribute('data-modal')) closeModal();
          popup(form.getAttribute('data-done') || 'Thank you — your message was sent.', true);
        } else {
          return r.json().then(function (d) {
            var m = d && d.errors && d.errors[0] && d.errors[0].message;
            popup(m || 'Something went wrong. Please try again.', false);
          }).catch(function () { popup('Something went wrong. Please try again.', false); });
        }
      }).catch(function () {
        popup('Network error — please check your connection and try again.', false);
      }).then(function () {
        if (btn) { btn.disabled = false; btn.textContent = label; }
      });
    });
  }

  // ---- contact modal ----------------------------------------------------
  var modal, lastFocus;
  function buildModal() {
    modal = document.createElement('div');
    modal.className = 'modal';
    modal.id = 'contact-modal';
    modal.setAttribute('aria-hidden', 'true');
    modal.innerHTML =
      '<div class="modal__backdrop" data-close></div>' +
      '<div class="modal__panel" role="dialog" aria-modal="true" aria-labelledby="cm-title">' +
      '<button class="modal__x" data-close aria-label="Close">&#215;</button>' +
      '<span class="entry-no">Reach the archive</span>' +
      '<h2 id="cm-title">Contact The Jersey City Sound</h2>' +
      '<p class="modal__lead">A correction, a memory, a photo, or a question — send it here and it reaches the editors directly.</p>' +
      '<form class="edit-form" data-ajax data-modal data-done="Thank you — your message reached the archive. We read every note.">' +
      '<div class="field"><label for="cm-name">Your name</label>' +
      '<input id="cm-name" name="name" type="text" autocomplete="name"></div>' +
      '<div class="field"><label for="cm-email">Your email</label>' +
      '<input id="cm-email" name="email" type="email" autocomplete="email" required></div>' +
      '<div class="field"><label for="cm-msg">Message</label>' +
      '<textarea id="cm-msg" name="message" required></textarea></div>' +
      '<input type="hidden" name="_subject" value="Contact — The Jersey City Sound">' +
      '<input type="text" name="_gotcha" style="display:none" tabindex="-1" aria-hidden="true">' +
      '<button type="submit">Send message</button></form></div>';
    document.body.appendChild(modal);
    modal.addEventListener('click', function (e) { if (e.target.hasAttribute('data-close')) closeModal(); });
    ajaxify(modal.querySelector('form'));
  }
  function openModal() {
    if (!modal) buildModal();
    lastFocus = document.activeElement;
    modal.setAttribute('aria-hidden', 'false');
    document.body.classList.add('modal-open');
    var f = modal.querySelector('#cm-name'); if (f) f.focus();
    document.addEventListener('keydown', onEsc);
  }
  function closeModal() {
    if (!modal) return;
    modal.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('modal-open');
    document.removeEventListener('keydown', onEsc);
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  function onEsc(e) { if (e.key === 'Escape') closeModal(); }

  // ---- wire up ----------------------------------------------------------
  document.querySelectorAll('form[data-ajax]').forEach(ajaxify);
  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-contact]');
    if (t) { e.preventDefault(); openModal(); }
  });
})();
