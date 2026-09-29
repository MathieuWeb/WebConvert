// Cookie consent + Google Analytics, loaded on every page.
//
// Nothing from Google is requested before the visitor clicks "Accepter":
// gtag.js is only injected once consent is granted (CNIL-compliant "basic"
// consent mode). The choice is kept in localStorage — acceptance for 13
// months, refusal for 6 months (CNIL guidance) — then the banner is shown
// again. Any link with [data-consent-open] (footer "Gérer les cookies")
// reopens the banner so the visitor can change their mind.
(function () {
  "use strict";

  var script = document.currentScript;
  var GA_ID = script && script.getAttribute("data-ga-id");
  if (!GA_ID) return;

  var KEY = "wc-consent";
  var MONTH = 30 * 24 * 60 * 60 * 1000;
  var TTL = { granted: 13 * MONTH, denied: 6 * MONTH };

  function readChoice() {
    try {
      var saved = JSON.parse(localStorage.getItem(KEY) || "null");
      if (saved && TTL[saved.v] && Date.now() - saved.t < TTL[saved.v]) return saved.v;
    } catch (e) {}
    return null;
  }

  function saveChoice(value) {
    try {
      localStorage.setItem(KEY, JSON.stringify({ v: value, t: Date.now() }));
    } catch (e) {}
  }

  var gaLoaded = false;
  function loadAnalytics() {
    if (gaLoaded) return;
    gaLoaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () {
      window.dataLayer.push(arguments);
    };
    window.gtag("js", new Date());
    window.gtag("config", GA_ID);
    var tag = document.createElement("script");
    tag.async = true;
    tag.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(GA_ID);
    document.head.appendChild(tag);
  }

  // Remove the _ga / _ga_<id> cookies on this domain and its parent.
  function clearAnalyticsCookies() {
    var host = location.hostname;
    var domains = ["", host, "." + host, "." + host.replace(/^www\./, "")];
    document.cookie.split(";").forEach(function (c) {
      var name = c.split("=")[0].trim();
      if (name === "_ga" || name.indexOf("_ga_") === 0) {
        domains.forEach(function (d) {
          document.cookie =
            name + "=; Max-Age=0; path=/" + (d ? "; domain=" + d : "");
        });
      }
    });
  }

  var banner = null;
  function buildBanner() {
    banner = document.createElement("section");
    banner.className = "consent";
    banner.setAttribute("role", "region");
    banner.setAttribute("aria-label", "Cookies de mesure d'audience");
    banner.innerHTML =
      '<p class="consent__text"><strong>Mesure d’audience</strong> ' +
      "Avec votre accord, Google Analytics mesure la fréquentation du site. " +
      "Vos images, elles, ne quittent jamais votre appareil. " +
      '<a href="/confidentialite/#cookies">En savoir plus</a></p>' +
      '<div class="consent__actions">' +
      '<button type="button" class="btn btn-secondary consent__btn" data-consent="denied">Refuser</button>' +
      '<button type="button" class="btn btn-primary consent__btn" data-consent="granted">Accepter</button>' +
      "</div>";
    banner.addEventListener("click", function (e) {
      var btn = e.target.closest("[data-consent]");
      if (btn) decide(btn.getAttribute("data-consent"));
    });
    document.body.appendChild(banner);
  }

  function showBanner() {
    if (!banner) buildBanner();
    banner.hidden = false;
  }
  function hideBanner() {
    if (banner) banner.hidden = true;
  }

  function decide(value) {
    var previous = readChoice();
    saveChoice(value);
    hideBanner();
    if (value === "granted") {
      loadAnalytics();
    } else {
      clearAnalyticsCookies();
      // gtag.js already running on this page can't be unloaded: reload so
      // the refusal takes effect immediately.
      if (previous === "granted" || gaLoaded) location.reload();
    }
  }

  function init() {
    var choice = readChoice();
    if (choice === "granted") loadAnalytics();
    else if (choice === null) showBanner();

    document.addEventListener("click", function (e) {
      var link = e.target.closest("[data-consent-open]");
      if (!link) return;
      e.preventDefault();
      showBanner();
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
