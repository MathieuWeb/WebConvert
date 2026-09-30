// Entry point of every tool page. window.WC_CONFIG.tool picks the tool:
// missing → the converter / compressor (ui.js); "resize", "pdf", "exif" →
// their own module, loaded only on their pages.
import { initFaq } from "./common.js";

const TOOLS = {
  resize: () => import("./tools/resize.js"),
  pdf: () => import("./tools/pdf.js"),
  exif: () => import("./tools/exif.js"),
};

async function start() {
  initFaq();
  const tool = (window.WC_CONFIG || {}).tool;
  if (TOOLS[tool]) {
    (await TOOLS[tool]()).init(window.WC_CONFIG);
  } else if (document.querySelector("[data-dropzone]")) {
    (await import("./ui.js")).initApp();
  }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", start);
} else {
  start();
}
