// Header "Outils" menu (<details>): close it on outside click and Escape.
// Everything else is native HTML, so the menu works without this script.
(function () {
  "use strict";
  var menu = document.querySelector("[data-nav-menu]");
  if (!menu) return;
  document.addEventListener("click", function (e) {
    if (menu.open && !menu.contains(e.target)) menu.open = false;
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && menu.open) {
      menu.open = false;
      menu.querySelector("summary").focus();
    }
  });
})();
