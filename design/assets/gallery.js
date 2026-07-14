/* The Jersey City Sound — gallery slideshow.
 * Progressive enhancement: the markup is already a native scroll-snap carousel
 * that swipes without JS. This layers on prev/next arrows, dot navigation, a
 * counter, and keyboard control. No dependencies. */
(function () {
  "use strict";

  function init(box) {
    var track = box.querySelector(".slideshow__track");
    var slides = Array.prototype.slice.call(box.querySelectorAll(".slide"));
    var prev = box.querySelector(".slideshow__nav--prev");
    var next = box.querySelector(".slideshow__nav--next");
    var dotsWrap = box.querySelector(".slideshow__dots");
    var counter = box.querySelector(".slideshow__count");
    if (!track || slides.length === 0) return;
    if (slides.length <= 1) return;  // single image (e.g. a logo): no arrows, dots, or counter

    box.classList.add("is-enhanced");
    var current = 0;

    // Build dots
    var dots = [];
    if (dotsWrap) {
      slides.forEach(function (_, i) {
        var d = document.createElement("button");
        d.type = "button";
        d.className = "slideshow__dot";
        d.setAttribute("role", "tab");
        d.setAttribute("aria-label", "Image " + (i + 1) + " of " + slides.length);
        d.addEventListener("click", function () { go(i); });
        dotsWrap.appendChild(d);
        dots.push(d);
      });
    }

    function go(i) {
      i = Math.max(0, Math.min(slides.length - 1, i));
      var target = slides[i];
      track.scrollTo({ left: target.offsetLeft - track.offsetLeft, behavior: "smooth" });
    }

    function setActive(i) {
      current = i;
      dots.forEach(function (d, di) {
        var on = di === i;
        d.classList.toggle("is-active", on);
        d.setAttribute("aria-selected", on ? "true" : "false");
      });
      if (counter) counter.textContent = (i + 1) + " / " + slides.length;
      if (prev) prev.disabled = i === 0;
      if (next) next.disabled = i === slides.length - 1;
    }

    // Track which slide is centered via scroll position
    var raf = null;
    function onScroll() {
      if (raf) return;
      raf = requestAnimationFrame(function () {
        raf = null;
        var center = track.scrollLeft + track.clientWidth / 2;
        var best = 0, bestDist = Infinity;
        slides.forEach(function (s, i) {
          var mid = s.offsetLeft - track.offsetLeft + s.clientWidth / 2;
          var dist = Math.abs(mid - center);
          if (dist < bestDist) { bestDist = dist; best = i; }
        });
        if (best !== current) setActive(best);
      });
    }
    track.addEventListener("scroll", onScroll, { passive: true });

    if (prev) { prev.hidden = false; prev.addEventListener("click", function () { go(current - 1); }); }
    if (next) { next.hidden = false; next.addEventListener("click", function () { go(current + 1); }); }

    track.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { e.preventDefault(); go(current + 1); }
      else if (e.key === "ArrowLeft") { e.preventDefault(); go(current - 1); }
      else if (e.key === "Home") { e.preventDefault(); go(0); }
      else if (e.key === "End") { e.preventDefault(); go(slides.length - 1); }
    });

    setActive(0);
  }

  function boot() {
    document.querySelectorAll("[data-slideshow]").forEach(init);
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
