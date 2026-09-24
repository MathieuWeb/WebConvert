import { FORMATS, acceptAttrFor, acceptAttrForAny } from "./formats-data.js";
import { convertImage, outputFileName, formatIdForFile, supportsEncoding } from "./conversion.js";
import { downloadAsZip, triggerDownload } from "./zip.js";

// Every page sets window.WC_CONFIG inline before this module loads:
//   input: a format id ("png") or "any" (homepage)
//   output: the format id the tool converts to by default — always concrete,
//     even on the homepage/hub pages, so the tool works the instant a file
//     is dropped. The format-picker at the top of the page (same component
//     everywhere) is the only thing that changes it, either by updating this
//     in place (see setOutput below) or by navigating to the matching page.
//   zipName: filename for the "download all" archive
function resolveConfig() {
  const c = window.WC_CONFIG || {};
  return {
    input: c.input || "any",
    output: c.output || "webp",
    zipName: c.zipName || "webconvert.zip",
  };
}

/** "3,4 Mo" / "612 Ko" — French thousand/decimal formatting to match the design. */
export function formatBytes(bytes) {
  if (bytes >= 1_000_000) {
    return (bytes / 1_000_000).toFixed(1).replace(".", ",") + " Mo";
  }
  return Math.round(bytes / 1000) + " Ko";
}

function savingsLabel(originalSize, newSize) {
  const pct = Math.round((1 - newSize / originalSize) * 100);
  return pct >= 0
    ? { pct, grew: false, text: "-" + pct + "%" }
    : { pct, grew: true, text: "+" + Math.abs(pct) + "%" };
}

function qualityTier(q) {
  if (q < 60) return ["Très léger", "Compression forte, pour les vignettes."];
  if (q < 85) return ["Équilibré", "Réglage conseillé pour le web."];
  if (q < 96) return ["Haute fidélité", "Pour les textures fines et les aplats."];
  return ["Qualité maximale", "Perte minimale, pour l'archivage."];
}

function debounce(fn, delay) {
  let handle;
  return (...args) => {
    clearTimeout(handle);
    handle = setTimeout(() => fn(...args), delay);
  };
}

export function initApp() {
  const config = resolveConfig();
  const state = {
    quality: 80,
    output: config.output,
    queue: [], // { id, file, name, inputFormatId, status, originalSize, result }
  };

  function currentFormat() {
    return FORMATS[state.output];
  }

  // If the current output can't actually be encoded by this browser, say so
  // up front instead of waiting for every conversion to fail silently. Only
  // relevant for formats encoded via canvas.toBlob(mime) — BMP and ICO are
  // hand-rolled (see conversion.js) and always work regardless of browser
  // canvas.toBlob support for their own MIME type.
  const NATIVE_ENCODE_FORMATS = new Set(["jpg", "png", "webp", "avif"]);
  function checkOutputSupport() {
    const fmt = currentFormat();
    if (!NATIVE_ENCODE_FORMATS.has(fmt.id)) {
      hideNotice();
      return;
    }
    supportsEncoding(fmt.mime).then((ok) => {
      if (state.output !== fmt.id) return; // output changed again meanwhile
      if (ok) hideNotice();
      else showNotice(fmt.label + " n'est pas pris en charge par votre navigateur actuel. Essayez la dernière version de Chrome ou Firefox, ou choisissez un autre format ci-dessus.");
    });
  }

  // Set by the format-picker below when it changes the output in place
  // (homepage, before an input format is chosen) rather than navigating.
  function setOutput(id, { reconvert = true } = {}) {
    state.output = id;
    renderQualityVisibility();
    checkOutputSupport();
    if (reconvert) scheduleQueueReconvert();
  }

  // ---------------- Quality slider ----------------
  const qualityCard = document.querySelector("[data-quality-card]");
  const qualitySlider = document.querySelector("[data-quality-slider]");
  const qualityFill = document.querySelector("[data-quality-fill]");
  const qualityThumb = document.querySelector("[data-quality-thumb]");
  const qualityNumber = document.querySelector("[data-quality-number]");
  const qualityTierEl = document.querySelector("[data-quality-tier]");
  const qualityNote = document.querySelector("[data-quality-note]");

  function renderQualityVisibility() {
    if (!qualityCard) return;
    qualityCard.classList.toggle("is-hidden", !currentFormat().lossy);
  }

  function renderQuality() {
    const pct = ((state.quality - 40) / 60) * 100;
    qualityFill.style.width = pct + "%";
    qualityThumb.style.left = pct + "%";
    qualityNumber.textContent = String(state.quality);
    qualitySlider.setAttribute("aria-valuenow", String(state.quality));
    const [tier, note] = qualityTier(state.quality);
    qualityTierEl.textContent = tier;
    qualityNote.textContent = note;
  }

  function setQuality(value) {
    const snapped = Math.round(value / 5) * 5;
    state.quality = Math.max(40, Math.min(100, snapped));
    renderQuality();
    scheduleQueueReconvert();
  }

  function qualityFromPointer(e) {
    const rect = qualitySlider.getBoundingClientRect();
    const t = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
    return 40 + t * 60;
  }

  if (qualitySlider) {
    qualitySlider.addEventListener("pointerdown", (e) => {
      qualitySlider.setPointerCapture(e.pointerId);
      setQuality(qualityFromPointer(e));
    });
    qualitySlider.addEventListener("pointermove", (e) => {
      if (e.buttons !== 1) return;
      setQuality(qualityFromPointer(e));
    });
    qualitySlider.addEventListener("keydown", (e) => {
      const deltas = { ArrowLeft: -5, ArrowDown: -5, ArrowRight: 5, ArrowUp: 5, PageUp: 10, PageDown: -10 };
      if (e.key in deltas) {
        e.preventDefault();
        setQuality(state.quality + deltas[e.key]);
      } else if (e.key === "Home") {
        e.preventDefault();
        setQuality(40);
      } else if (e.key === "End") {
        e.preventDefault();
        setQuality(100);
      }
    });
    renderQuality();
  }

  renderQualityVisibility();

  // ---------------- Dropzone / file intake ----------------
  const dropzone = document.querySelector("[data-dropzone]");
  const fileInput = document.querySelector("[data-file-input]");
  const pickButton = document.querySelector("[data-pick-button]");
  const toolNotice = document.querySelector("[data-tool-notice]");

  if (config.input === "any") {
    fileInput.setAttribute("accept", acceptAttrForAny());
  } else {
    fileInput.setAttribute("accept", acceptAttrFor(config.input));
  }

  pickButton.addEventListener("click", () => fileInput.click());
  fileInput.addEventListener("change", () => {
    addFiles(fileInput.files);
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
    addFiles(e.dataTransfer.files);
  });

  function showNotice(message) {
    if (!toolNotice) return;
    toolNotice.textContent = message;
    toolNotice.classList.add("is-visible");
  }
  function hideNotice() {
    if (!toolNotice) return;
    toolNotice.classList.remove("is-visible");
  }

  checkOutputSupport();

  function acceptedInputFormatId(file) {
    const detected = formatIdForFile(file);
    if (!detected || !FORMATS[detected].canDecode) return null;
    if (config.input !== "any" && detected !== config.input) return null;
    return detected;
  }

  function addFiles(fileList) {
    const files = Array.from(fileList);
    const accepted = [];
    let rejected = 0;
    for (const file of files) {
      const inputFormatId = acceptedInputFormatId(file);
      if (inputFormatId) accepted.push({ file, inputFormatId });
      else rejected++;
    }
    if (rejected > 0 && accepted.length === 0) {
      showNotice(
        config.input === "any"
          ? "Ces fichiers ne sont pas dans un format d'image pris en charge."
          : "Ce fichier n'est pas au format " + FORMATS[config.input].label + "."
      );
      return;
    }
    hideNotice();
    for (const { file, inputFormatId } of accepted) {
      state.queue.push({
        id: crypto.randomUUID(),
        file,
        name: file.name,
        inputFormatId,
        status: "waiting",
        originalSize: file.size,
        result: null,
      });
    }
    renderQueue();
    processQueue();
  }

  // ---------------- Queue processing ----------------
  const queueCard = document.querySelector("[data-queue-card]");
  const queueList = document.querySelector("[data-queue-list]");
  const queueSummary = document.querySelector("[data-queue-summary]");

  function renderQueue() {
    if (state.queue.length === 0) {
      queueCard.classList.remove("is-visible");
      return;
    }
    queueCard.classList.add("is-visible");
    const done = state.queue.filter((f) => f.status === "done").length;
    const totalBytes = state.queue.reduce((sum, f) => sum + f.originalSize, 0);
    queueSummary.textContent =
      state.queue.length + " fichier" + (state.queue.length > 1 ? "s" : "") +
      (done < state.queue.length ? ", " + done + " terminé" + (done > 1 ? "s" : "") : ", " + formatBytes(totalBytes));

    queueList.innerHTML = "";
    for (const item of state.queue) {
      const row = document.createElement("div");
      row.className = "queue-row";

      const name = document.createElement("span");
      name.className = "queue-row__name";
      name.textContent = item.name;
      row.appendChild(name);

      if (item.status === "done") {
        const check = document.createElement("span");
        check.className = "queue-row__check";
        check.textContent = "✓";
        row.appendChild(check);
      } else if (item.status === "converting") {
        const bar = document.createElement("span");
        bar.className = "queue-row__bar";
        const fill = document.createElement("span");
        fill.className = "queue-row__bar-fill is-active";
        bar.appendChild(fill);
        row.appendChild(bar);
      }

      const status = document.createElement("span");
      status.className = "queue-row__status" + (item.status === "error" ? " is-error" : "");
      status.textContent =
        item.status === "done" ? "terminé" : item.status === "converting" ? "conversion…" :
        item.status === "error" ? "erreur" : "en attente";
      row.appendChild(status);

      queueList.appendChild(row);
    }
  }

  let processing = false;
  async function processQueue() {
    if (processing) return;
    processing = true;
    try {
      for (const item of state.queue) {
        if (item.status !== "waiting") continue;
        item.status = "converting";
        renderQueue();
        try {
          const result = await convertImage(item.file, item.inputFormatId, state.quality, state.output);
          item.result = result;
          item.status = "done";
        } catch (err) {
          item.status = "error";
          showNotice(
            "La conversion de " + item.name + " a échoué (" +
              (err && err.message ? err.message : "erreur inconnue") + ")."
          );
        }
        renderQueue();
      }
    } finally {
      processing = false;
    }
    renderResults();
  }

  const scheduleQueueReconvert = debounce(async () => {
    const finished = state.queue.filter((f) => f.status === "done" || f.status === "error");
    if (finished.length === 0) return;
    for (const item of finished) item.status = "waiting";
    renderQueue();
    await processQueue();
  }, 300);

  // ---------------- Results ----------------
  const resultsSection = document.querySelector("[data-results]");
  const resultsPct = document.querySelector("[data-results-pct]");
  const resultsDetail = document.querySelector("[data-results-detail]");
  const resultsList = document.querySelector("[data-results-list]");
  const downloadAllBtn = document.querySelector("[data-download-all]");

  function currentExt() {
    return currentFormat().exts[0];
  }

  function renderResults() {
    const done = state.queue.filter((f) => f.status === "done" && f.result);
    if (done.length === 0) {
      resultsSection.classList.remove("is-visible");
      return;
    }
    resultsSection.classList.add("is-visible");

    const totalOriginal = done.reduce((s, f) => s + f.originalSize, 0);
    const totalOut = done.reduce((s, f) => s + f.result.blob.size, 0);
    const savings = savingsLabel(totalOriginal, totalOut);

    resultsPct.textContent = savings.text;
    resultsDetail.innerHTML =
      (savings.grew ? "de poids en plus sur le lot" : "de poids en moins sur le lot") +
      "<br><span class=\"mono\">" +
      formatBytes(totalOriginal) + " vers " + formatBytes(totalOut) + ", " +
      done.length + " fichier" + (done.length > 1 ? "s" : "") + "</span>";
    downloadAllBtn.textContent = "Tout télécharger, ZIP " + formatBytes(totalOut);

    resultsList.innerHTML = "";
    for (const item of done) {
      const row = document.createElement("div");
      row.className = "result-row";

      const name = document.createElement("span");
      name.className = "result-row__name";
      name.textContent = outputFileName(item.name, currentExt());
      row.appendChild(name);

      const weights = document.createElement("span");
      weights.className = "result-row__weights";
      weights.textContent = formatBytes(item.originalSize) + " vers " + formatBytes(item.result.blob.size);
      row.appendChild(weights);

      const save = document.createElement("span");
      save.className = "result-row__save";
      save.textContent = savingsLabel(item.originalSize, item.result.blob.size).text;
      row.appendChild(save);

      const dl = document.createElement("button");
      dl.type = "button";
      dl.className = "btn btn-secondary result-row__download";
      dl.textContent = "Télécharger";
      dl.addEventListener("click", () => triggerDownload(item.result.blob, outputFileName(item.name, currentExt())));
      row.appendChild(dl);

      resultsList.appendChild(row);
    }
  }

  downloadAllBtn.addEventListener("click", async () => {
    const done = state.queue.filter((f) => f.status === "done" && f.result);
    if (done.length === 0) return;
    downloadAllBtn.disabled = true;
    const originalLabel = downloadAllBtn.textContent;
    downloadAllBtn.textContent = "Préparation du ZIP…";
    try {
      await downloadAsZip(
        done.map((f) => ({ name: outputFileName(f.name, currentExt()), blob: f.result.blob })),
        config.zipName
      );
    } finally {
      downloadAllBtn.disabled = false;
      downloadAllBtn.textContent = originalLabel;
    }
  });

  // ---------------- FAQ ----------------
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

  // ---------------- Format picker ----------------
  // Same widget on every page. Changing "depuis" always navigates (to the
  // matching pair page when a "vers" is already set and differs from it,
  // otherwise to that format's hub page). Changing "vers" navigates too,
  // *except* when "depuis" is still empty (only possible on the homepage,
  // before any input format is chosen) — there it just updates the tool's
  // active output in place, since there is no dedicated page for
  // "any format to X" to send the visitor to.
  const pickerForm = document.querySelector("[data-format-picker]");
  if (pickerForm) {
    const fromSelect = pickerForm.querySelector("[data-picker-from]");
    const toSelect = pickerForm.querySelector("[data-picker-to]");

    const goToPair = (from, to) => (window.location.href = "/" + from + "-en-" + to + "/");
    const goToHub = (from) => (window.location.href = "/convertisseur-" + from + "/");

    const submit = () => {
      const from = fromSelect.value;
      const to = toSelect.value;
      if (from && to && from !== to) goToPair(from, to);
      else if (from) goToHub(from);
      else if (to) dropzone.scrollIntoView({ behavior: "smooth", block: "center" });
    };
    pickerForm.addEventListener("submit", (e) => {
      e.preventDefault();
      submit();
    });
    fromSelect.addEventListener("change", () => {
      const from = fromSelect.value;
      const to = toSelect.value;
      if (!from) return;
      if (to && to !== from) goToPair(from, to);
      else goToHub(from);
    });
    // Each select sits invisibly over a format card; mirror the chosen
    // option onto the card face (only visible when the page doesn't
    // navigate away, i.e. picking "vers" on the homepage).
    const syncCard = (select) => {
      const card = select.closest(".fcard");
      if (!card) return;
      const opt = select.options[select.selectedIndex];
      if (select.value) card.querySelector("[data-fcard-label]").textContent = opt.textContent;
      card.classList.toggle("is-empty", !select.value);
    };
    toSelect.addEventListener("change", () => {
      const from = fromSelect.value;
      const to = toSelect.value;
      if (!to) return;
      if (from) {
        if (to !== from) goToPair(from, to);
        // else: picked the same format as the input — ignore, there is no
        // page for that and it's clearly not what the visitor meant.
      } else {
        syncCard(toSelect);
        setOutput(to);
      }
    });

    // Swap button: goes to the reverse pair page. Rendered disabled when
    // the reverse conversion doesn't exist (e.g. output-only/input-only formats).
    const swapButton = pickerForm.querySelector("[data-picker-swap]");
    if (swapButton) {
      swapButton.addEventListener("click", () => {
        const from = fromSelect.value;
        const to = toSelect.value;
        if (from && to && from !== to) goToPair(to, from);
      });
    }
  }
}
