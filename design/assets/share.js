/* The Jersey City Sound — entry sharing.
 * Native share sheet (mobile), "Share to Story" (shares the branded card image
 * as a file so it drops straight into Instagram/other Stories), X, Facebook,
 * and copy-link. All progressive: falls back to download / prompt where unsupported. */
(function () {
  "use strict";

  function flash(el, msg) {
    if (!el) return;
    var prev = el.getAttribute("data-label") || el.textContent;
    el.setAttribute("data-label", prev);
    el.textContent = msg;
    setTimeout(function () { el.textContent = prev; }, 1600);
  }

  function init(box) {
    var url = box.dataset.url, title = box.dataset.title,
        name = box.dataset.name || "The Jersey City Sound", card = box.dataset.card;

    function btn(act) { return box.querySelector('[data-act="' + act + '"]'); }
    function on(act, fn) { var el = btn(act); if (el) el.addEventListener("click", fn); }

    function copyLink() {
      var done = function () { flash(btn("copy"), "Copied!"); };
      var fail = function () { window.prompt("Copy this link:", url); };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(done, fail);
      } else { fail(); }
    }

    on("native", function (e) {
      e.preventDefault();
      if (navigator.share) {
        navigator.share({ title: title, text: name + " — The Jersey City Sound", url: url })
          .catch(function () {});
      } else { copyLink(); }
    });

    on("copy", function (e) { e.preventDefault(); copyLink(); });

    on("story", function (e) {
      e.preventDefault();
      var b = btn("story");
      var slug = name.replace(/[^\w]+/g, "-").toLowerCase().replace(/^-|-$/g, "");
      fetch(card).then(function (r) { return r.blob(); }).then(function (blob) {
        var file = new File([blob], "jersey-city-sound-" + slug + ".png", { type: "image/png" });
        if (navigator.canShare && navigator.canShare({ files: [file] })) {
          return navigator.share({ files: [file], title: title, text: name + " · jerseycitysound.com", url: url });
        }
        throw new Error("no-file-share");
      }).catch(function () {
        // Fallback: download the card so it can be posted manually
        var a = document.createElement("a");
        a.href = card; a.download = "jersey-city-sound-" + slug + ".png";
        document.body.appendChild(a); a.click(); a.remove();
        flash(b, "Card saved");
      });
    });
  }

  function boot() { document.querySelectorAll(".share").forEach(init); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
