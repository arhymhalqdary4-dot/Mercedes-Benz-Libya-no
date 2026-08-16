/* Decakila Libya — mobile navigation toggle.
   The only script on the site: opens/closes the drawer that the nav collapses
   into below 1024px, and keeps `aria-expanded` in sync for screen readers. */

(function () {
  "use strict";

  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("main-nav");

  if (!toggle || !nav) return;

  function setOpen(open) {
    nav.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  }

  toggle.addEventListener("click", function () {
    setOpen(toggle.getAttribute("aria-expanded") !== "true");
  });

  /* Tapping a link closes the drawer before the page navigates. */
  nav.addEventListener("click", function (event) {
    if (event.target.closest("a")) setOpen(false);
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && nav.classList.contains("is-open")) {
      setOpen(false);
      toggle.focus();
    }
  });

  /* Reset state when the viewport grows back to the desktop layout. */
  window.addEventListener("resize", function () {
    if (window.innerWidth > 1024) setOpen(false);
  });
})();
