// Images → one PDF (/images-en-pdf/ and its démarche variants). Each image
// becomes a page (A4 or its own size), embedded as JPEG. With a weight
// limit, the budget is split between pages by pixel area and each image is
// compressed to fit its share (compressCanvasToTarget). The PDF file itself
// is written by hand below: a PDF made of JPEG pages only needs a dozen
// objects, no library required.
import { FORMATS, acceptAttrForAny } from "../formats-data.js";
import { decodeToCanvas, encodeCanvas, compressCanvasToTarget, formatIdForFile } from "../conversion.js";
import { triggerDownload } from "../zip.js";
import { formatBytes, el, debounce, bindDropzone, notice } from "../common.js";

const A4 = [595.28, 841.89]; // points
const MM = 72 / 25.4;
// Long side cap: A4 at 300 dpi. Beyond that a page gains nothing printed
// or on screen, only weight.
const MAX_SIDE = 3508;
const PAGE_OVERHEAD = 600; // bytes per page of PDF structure (generous)

export function init(config) {
  const $ = (sel) => document.querySelector(sel);
  const pageSelect = $("[data-pdf-page]");
  const marginSelect = $("[data-pdf-margin]");
  const targetSelect = $("[data-pdf-target]");
  const toolMain = $("[data-tool]");
  const filesBox = $("[data-queue-card]");
  const list = $("[data-queue-list]");
  const summary = $("[data-queue-summary]");
  const button = $("[data-download-all]");

  const state = { items: [], pdf: null, building: false };

  // ---------------- Intake ----------------
  async function addFiles(files) {
    notice("");
    let rejected = 0;
    for (const file of files) {
      const formatId = formatIdForFile(file);
      if (!formatId || !FORMATS[formatId].canDecode) {
        rejected++;
        continue;
      }
      try {
        const source = capped(await decodeToCanvas(file, formatId, "jpg"));
        state.items.push({ id: crypto.randomUUID(), name: file.name, source, thumbUrl: thumbOf(source) });
      } catch {
        rejected++;
      }
    }
    if (rejected) notice(rejected + " fichier" + (rejected > 1 ? "s ignorés" : " ignoré") + " : format non pris en charge ou illisible.");
    renderList();
    rebuild();
  }
  bindDropzone(addFiles, { accept: acceptAttrForAny() });

  function capped(canvas) {
    const long = Math.max(canvas.width, canvas.height);
    if (long <= MAX_SIDE) return canvas;
    const k = MAX_SIDE / long;
    const c = document.createElement("canvas");
    c.width = Math.round(canvas.width * k);
    c.height = Math.round(canvas.height * k);
    const ctx = c.getContext("2d");
    ctx.imageSmoothingQuality = "high";
    ctx.drawImage(canvas, 0, 0, c.width, c.height);
    return c;
  }

  function thumbOf(canvas) {
    const k = 96 / Math.max(canvas.width, canvas.height);
    const c = document.createElement("canvas");
    c.width = Math.max(1, Math.round(canvas.width * k));
    c.height = Math.max(1, Math.round(canvas.height * k));
    c.getContext("2d").drawImage(canvas, 0, 0, c.width, c.height);
    return c.toDataURL("image/jpeg", 0.7);
  }

  // ---------------- List (reorder / remove) ----------------
  function move(index, delta) {
    const j = index + delta;
    if (j < 0 || j >= state.items.length) return;
    [state.items[index], state.items[j]] = [state.items[j], state.items[index]];
    renderList();
    rebuild();
  }

  function iconButton(label, path, onClick, disabled) {
    const b = el("button", "file__act");
    b.type = "button";
    b.title = label;
    b.setAttribute("aria-label", label);
    b.disabled = !!disabled;
    b.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + path + "</svg>";
    b.addEventListener("click", onClick);
    return b;
  }

  function renderList() {
    const count = state.items.length;
    toolMain.classList.toggle("has-files", count > 0);
    filesBox.classList.toggle("is-visible", count > 0);
    list.innerHTML = "";
    state.items.forEach((item, index) => {
      const row = el("li", "file is-done");
      const thumb = el("span", "file__thumb");
      const img = el("img");
      img.src = item.thumbUrl;
      img.alt = "";
      thumb.appendChild(img);
      row.appendChild(thumb);
      const name = el("span", "file__name");
      name.appendChild(el("span", "file__filename", item.name));
      name.appendChild(el("span", "file__conv", "Page " + (index + 1) + " · " + item.source.width + "×" + item.source.height + " px"));
      row.appendChild(name);
      const acts = el("span", "file__acts");
      acts.appendChild(iconButton("Monter", '<path d="m6 15 6-6 6 6"/>', () => move(index, -1), index === 0));
      acts.appendChild(iconButton("Descendre", '<path d="m6 9 6 6 6-6"/>', () => move(index, 1), index === count - 1));
      acts.appendChild(iconButton("Retirer", '<path d="M6 6l12 12M18 6 6 18"/>', () => {
        state.items.splice(index, 1);
        renderList();
        rebuild();
      }));
      row.appendChild(acts);
      list.appendChild(row);
    });
    renderSummary();
  }

  function renderSummary() {
    const target = Number(targetSelect.value) || null;
    if (!state.items.length) {
      summary.textContent = "";
      button.hidden = true;
      return;
    }
    const pages = state.items.length + " page" + (state.items.length > 1 ? "s" : "");
    if (state.building || !state.pdf) {
      summary.textContent = pages + " · création du PDF…";
      button.hidden = true;
      return;
    }
    const size = formatBytes(state.pdf.blob.size);
    let text = "PDF de " + pages + " · " + size;
    if (target) text += state.pdf.fits ? " (sous " + formatBytes(target) + ")" : " · impossible d'atteindre " + formatBytes(target);
    summary.textContent = text;
    summary.classList.toggle("is-over", !state.pdf.fits);
    button.hidden = false;
  }

  // ---------------- Build ----------------
  let generation = 0;
  const rebuild = debounce(async () => {
    const gen = ++generation;
    state.pdf = null;
    if (!state.items.length) return renderSummary();
    state.building = true;
    renderSummary();
    try {
      const pdf = await buildPdf(state.items, {
        page: pageSelect.value,
        margin: Number(marginSelect.value) * MM,
        target: Number(targetSelect.value) || null,
      });
      if (gen !== generation) return; // settings changed meanwhile
      state.pdf = pdf;
    } catch (err) {
      notice("La création du PDF a échoué (" + (err && err.message ? err.message : "erreur inconnue") + ").");
    } finally {
      if (gen === generation) {
        state.building = false;
        renderSummary();
      }
    }
  }, 300);

  button.addEventListener("click", () => {
    if (state.pdf) triggerDownload(state.pdf.blob, config.pdfName || "images.pdf");
  });

  [pageSelect, marginSelect, targetSelect].forEach((sel) =>
    sel.addEventListener("change", () => {
      const card = sel.closest(".fcard");
      if (card) card.querySelector("[data-fcard-label]").textContent = sel.options[sel.selectedIndex].textContent;
      rebuild();
    })
  );
}

// Encode every page as JPEG (under its share of the budget when there is a
// weight limit), then assemble the PDF.
async function buildPdf(items, { page, margin, target }) {
  const totalArea = items.reduce((s, i) => s + i.source.width * i.source.height, 0);
  const budget = target ? target - 1000 - PAGE_OVERHEAD * items.length : null;
  let fits = true;
  const jpegs = [];
  for (const item of items) {
    let blob;
    let canvas = item.source;
    if (budget) {
      const share = Math.max(8000, Math.floor((budget * item.source.width * item.source.height) / totalArea));
      const r = await compressCanvasToTarget(item.source, "jpg", share);
      blob = r.blob;
      fits = fits && r.fits;
      if (r.width !== canvas.width) canvas = { width: r.width, height: r.height };
    } else {
      blob = await encodeCanvas(item.source, "jpg", 85);
    }
    jpegs.push({ bytes: new Uint8Array(await blob.arrayBuffer()), width: canvas.width, height: canvas.height });
  }
  const pdfBlob = writePdf(jpegs, page, margin);
  if (target && pdfBlob.size > target) fits = false;
  return { blob: pdfBlob, fits };
}

/**
 * Minimal PDF 1.4 writer: one page per JPEG (DCTDecode XObject), image
 * centred and scaled to fit the page's content box.
 * page: "a4" | "a4l" | "fit" (page = image size at 96 dpi); margin in points.
 */
function writePdf(images, page, margin) {
  const enc = new TextEncoder();
  const chunks = [];
  const offsets = [];
  let length = 0;
  const push = (data) => {
    const bytes = typeof data === "string" ? enc.encode(data) : data;
    chunks.push(bytes);
    length += bytes.length;
  };
  const obj = (n, body) => {
    offsets[n] = length;
    push(n + " 0 obj\n");
    for (const part of body) push(part);
    push("\nendobj\n");
  };
  const fmt = (v) => (Math.round(v * 100) / 100).toString();

  push("%PDF-1.4\n%\xE2\xE3\xCF\xD3\n");
  const n = images.length;
  // 1: catalog, 2: pages, then for page i: 3+3i page, 4+3i content, 5+3i image
  const kids = images.map((_, i) => 3 + 3 * i + " 0 R").join(" ");
  obj(1, ["<< /Type /Catalog /Pages 2 0 R >>"]);
  obj(2, ["<< /Type /Pages /Kids [" + kids + "] /Count " + n + " >>"]);
  images.forEach((img, i) => {
    let pw, ph;
    if (page === "fit") {
      pw = img.width * 0.75 + 2 * margin;
      ph = img.height * 0.75 + 2 * margin;
    } else {
      [pw, ph] = page === "a4l" ? [A4[1], A4[0]] : A4;
    }
    const boxW = pw - 2 * margin;
    const boxH = ph - 2 * margin;
    const k = Math.min(boxW / img.width, boxH / img.height);
    const w = img.width * k;
    const h = img.height * k;
    const x = (pw - w) / 2;
    const y = (ph - h) / 2;
    const p = 3 + 3 * i;
    obj(p, ["<< /Type /Page /Parent 2 0 R /MediaBox [0 0 " + fmt(pw) + " " + fmt(ph) + "] " +
      "/Resources << /XObject << /Im0 " + (p + 2) + " 0 R >> >> /Contents " + (p + 1) + " 0 R >>"]);
    const content = "q " + fmt(w) + " 0 0 " + fmt(h) + " " + fmt(x) + " " + fmt(y) + " cm /Im0 Do Q";
    obj(p + 1, ["<< /Length " + enc.encode(content).length + " >>\nstream\n" + content + "\nendstream"]);
    obj(p + 2, [
      "<< /Type /XObject /Subtype /Image /Width " + img.width + " /Height " + img.height +
        " /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length " + img.bytes.length + " >>\nstream\n",
      img.bytes,
      "\nendstream",
    ]);
  });
  const xref = length;
  const count = 3 + 3 * n;
  let table = "xref\n0 " + count + "\n0000000000 65535 f \n";
  for (let i = 1; i < count; i++) table += String(offsets[i]).padStart(10, "0") + " 00000 n \n";
  push(table);
  push("trailer\n<< /Size " + count + " /Root 1 0 R >>\nstartxref\n" + xref + "\n%%EOF\n");
  return new Blob(chunks, { type: "application/pdf" });
}
