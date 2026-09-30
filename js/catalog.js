// /outils/: category filter over the tool cards. Tabs stay hidden without
// JavaScript (all cards are shown). The URL hash (#compresser...) selects a
// tab, so the header menu can link straight to a category.
const tabsBox = document.querySelector("[data-cat-tabs]");
const tabs = [...document.querySelectorAll("[data-cat-tab]")];
const cards = [...document.querySelectorAll(".tool-cards [data-cat]")];

function select(cat, { updateHash = true } = {}) {
  const valid = tabs.some((t) => t.dataset.catTab === cat);
  if (!valid) cat = "";
  tabs.forEach((t) => t.setAttribute("aria-pressed", String(t.dataset.catTab === cat)));
  cards.forEach((c) => (c.hidden = !!cat && c.dataset.cat !== cat));
  if (updateHash) history.replaceState(null, "", cat ? "#" + cat : location.pathname);
}

if (tabsBox) {
  tabsBox.hidden = false;
  tabs.forEach((t) => t.addEventListener("click", () => select(t.dataset.catTab)));
  select(location.hash.slice(1), { updateHash: false });
  window.addEventListener("hashchange", () => select(location.hash.slice(1), { updateHash: false }));
}
