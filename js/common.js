// Helpers shared by every tool page (converter, resize, PDF, metadata).

/** "3,4 Mo" / "612 Ko" / "1 Mo" — French decimal formatting, 1 Ko = 1 000 octets. */
export function formatBytes(bytes) {
  if (bytes >= 1_000_000) {
    return (bytes / 1_000_000).toFixed(1).replace(/\.0$/, "").replace(".", ",") + " Mo";
  }
  return Math.max(1, Math.round(bytes / 1000)) + " Ko";
}

// "−65 %" (true minus sign, non-breaking space before %, French typography).
export function savingsLabel(originalSize, newSize) {
  const pct = Math.round((1 - newSize / originalSize) * 100);
  if (pct === 0) return { pct, grew: false, text: "0 %" };
  return pct > 0
    ? { pct, grew: false, text: "−" + pct + " %" }
    : { pct, grew: true, text: "+" + Math.abs(pct) + " %" };
}

export function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text != null) node.textContent = text;
  return node;
}

export function debounce(fn, delay) {
  let handle;
  return (...args) => {
    clearTimeout(handle);
    handle = setTimeout(() => fn(...args), delay);
  };
}

export const DOWNLOAD_ICON =
  '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v11"/><path d="m7 10 5 5 5-5"/><path d="M5 20h14"/></svg>';

/** FAQ accordion, on every page that has one. */
export function initFaq() {
  document.querySelectorAll("[data-faq-item]").forEach((item) => {
    const trigger = item.querySelector("[data-faq-trigger]");
    const sign = item.querySelector("[data-faq-sign]");
    trigger.addEventListener("click", () => {
      const open = item.getAttribute("data-open") === "true";
      item.setAttribute("data-open", String(!open));
      trigger.setAttribute("aria-expanded", String(!open));
      sign.textContent = open ? "+" : "–";
    });
  });
}

/**
 * Wire the tool window's dropzone: click anywhere / button → file dialog,
 * drag and drop, file input change. Calls onFiles(File[]).
 */
export function bindDropzone(onFiles, { accept } = {}) {
  const dropzone = document.querySelector("[data-dropzone]");
  const fileInput = document.querySelector("[data-file-input]");
  const pickButton = document.querySelector("[data-pick-button]");
  if (accept) fileInput.setAttribute("accept", accept);

  pickButton.addEventListener("click", (e) => {
    e.stopPropagation();
    fileInput.click();
  });
  dropzone.addEventListener("click", (e) => {
    if (e.target === fileInput || e.target.closest("button")) return;
    fileInput.click();
  });
  fileInput.addEventListener("change", () => {
    onFiles(Array.from(fileInput.files));
    fileInput.value = "";
  });
  ["dragenter", "dragover"].forEach((evt) =>
    dropzone.addEventListener(evt, (e) => {
      e.preventDefault();
      dropzone.classList.add("is-dragover");
    })
  );
  ["dragleave", "dragend"].forEach((evt) =>
    dropzone.addEventListener(evt, () => dropzone.classList.remove("is-dragover"))
  );
  dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.classList.remove("is-dragover");
    onFiles(Array.from(e.dataTransfer.files));
  });
  return dropzone;
}

/** Show/hide the tool's inline notice (errors, unsupported format...). */
export function notice(message) {
  const box = document.querySelector("[data-tool-notice]");
  if (!box) return;
  box.textContent = message || "";
  box.classList.toggle("is-visible", !!message);
}
