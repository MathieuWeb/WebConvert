// Resize / crop to an exact size (/redimensionner-image/ and the platform
// pages such as /taille-banniere-linkedin/). Every image is cropped to fill
// the requested width × height ("cover"): the visitor frames it by dragging
// and zooming in the editor. With "Conserver les proportions", only the
// width is imposed and nothing is cropped.
import { FORMATS, acceptAttrForAny } from "../formats-data.js";
import { decodeToCanvas, encodeCanvas, compressCanvasToTarget, formatIdForFile, outputFileName } from "../conversion.js";
import { downloadAsZip, triggerDownload } from "../zip.js";
import { formatBytes, el, debounce, bindDropzone, notice, DOWNLOAD_ICON } from "../common.js";

const MAX_SIDE = 10000;

export function init(config) {
  const $ = (sel) => document.querySelector(sel);
  const widthInput = $("[data-resize-width]");
  const heightInput = $("[data-resize-height]");
  const keepInput = $("[data-resize-keep]");
  const formatSelect = $("[data-resize-format]");
  const targetSelect = $("[data-resize-target]");
  const editor = $("[data-editor]");
  const stage = $("[data-editor-stage]");
  const canvas = $("[data-editor-canvas]");
  const zoomInput = $("[data-editor-zoom]");
  const toolMain = $("[data-tool]");
  const filesBox = $("[data-queue-card]");
  const list = $("[data-queue-list]");
  const summary = $("[data-queue-summary]");
  const zipButton = $("[data-download-all]");

  const state = {
    items: [], // { id, name, source (canvas), zoom, fx, fy, result, thumbUrl, status }
    selected: null,
  };

  const readInt = (input) => {
    const n = parseInt(input.value, 10);
    return Number.isFinite(n) && n > 0 ? Math.min(n, MAX_SIDE) : null;
  };
  const settings = () => ({
    width: readInt(widthInput),
    height: readInt(heightInput),
    keep: keepInput.checked,
    format: formatSelect.value,
    target: Number(targetSelect.value) || null,
  });

  // Output size for one image: exact W×H, or W × proportional height.
  function outputSize(item, s) {
    const iw = item.source.width;
    const ih = item.source.height;
    if (s.keep || !s.height || !s.width) {
      if (s.width) return [s.width, Math.max(1, Math.round((s.width * ih) / iw))];
      if (s.height) return [Math.max(1, Math.round((s.height * iw) / ih)), s.height];
      return [iw, ih];
    }
    return [s.width, s.height];
  }

  // Draw `item` into a W×H canvas: cover-fit, then zoom, then focus point
  // (fx, fy in 0..1: which part of the overflow stays visible).
  function draw(ctx, item, W, H, s) {
    const iw = item.source.width;
    const ih = item.source.height;
    if (s.format === "jpg") {
      ctx.fillStyle = "#ffffff";
      ctx.fillRect(0, 0, W, H);
    } else {
      ctx.clearRect(0, 0, W, H);
    }
    const cropping = !(s.keep || !s.height || !s.width);
    const scale = cropping ? Math.max(W / iw, H / ih) * item.zoom : W / iw;
    const dw = iw * scale;
    const dh = ih * scale;
    const x = cropping ? (W - dw) * item.fx : 0;
    const y = cropping ? (H - dh) * item.fy : 0;
    ctx.imageSmoothingQuality = "high";
    ctx.drawImage(item.source, x, y, dw, dh);
    return { dw, dh };
  }

  // ---------------- Editor (preview of the selected image) ----------------
  function renderEditor() {
    const item = state.items.find((i) => i.id === state.selected);
    const s = settings();
    const cropping = !(s.keep || !s.height || !s.width);
    editor.hidden = !item;
    if (!item) return;
    editor.classList.toggle("is-static", !cropping);
    zoomInput.disabled = !cropping;
    const [W, H] = outputSize(item, s);
    const maxW = stage.clientWidth || 600;
    const maxH = 320;
    const k = Math.min(maxW / W, maxH / H);
    canvas.width = Math.max(1, Math.round(W * k * devicePixelRatio));
    canvas.height = Math.max(1, Math.round(H * k * devicePixelRatio));
    canvas.style.width = Math.round(W * k) + "px";
    canvas.style.height = Math.round(H * k) + "px";
    const ctx = canvas.getContext("2d");
    ctx.save();
    ctx.scale(canvas.width / W, canvas.height / H);
    draw(ctx, item, W, H, s);
    ctx.restore();
    zoomInput.value = String(item.zoom);
  }

  let drag = null;
  canvas.addEventListener("pointerdown", (e) => {
    const item = state.items.find((i) => i.id === state.selected);
    if (!item || editor.classList.contains("is-static")) return;
    canvas.setPointerCapture(e.pointerId);
    drag = { x: e.clientX, y: e.clientY, fx: item.fx, fy: item.fy };
  });
  canvas.addEventListener("pointermove", (e) => {
    if (!drag) return;
    const item = state.items.find((i) => i.id === state.selected);
    const s = settings();
    const [W, H] = outputSize(item, s);
    const k = canvas.clientWidth / W; // display px per output px
    const scale = Math.max(W / item.source.width, H / item.source.height) * item.zoom;
    const overflowX = W - item.source.width * scale; // <= 0
    const overflowY = H - item.source.height * scale;
    const dx = (e.clientX - drag.x) / k;
    const dy = (e.clientY - drag.y) / k;
    item.fx = overflowX < 0 ? clamp(drag.fx + dx / overflowX) : 0.5;
    item.fy = overflowY < 0 ? clamp(drag.fy + dy / overflowY) : 0.5;
    renderEditor();
  });
  const endDrag = () => {
    if (!drag) return;
    drag = null;
    rerender(state.selected);
  };
  canvas.addEventListener("pointerup", endDrag);
  canvas.addEventListener("pointercancel", endDrag);
  canvas.addEventListener("keydown", (e) => {
    const item = state.items.find((i) => i.id === state.selected);
    const moves = { ArrowLeft: [-0.05, 0], ArrowRight: [0.05, 0], ArrowUp: [0, -0.05], ArrowDown: [0, 0.05] };
    if (!item || !(e.key in moves)) return;
    e.preventDefault();
    item.fx = clamp(item.fx - moves[e.key][0]);
    item.fy = clamp(item.fy - moves[e.key][1]);
    renderEditor();
    rerender(item.id);
  });
  canvas.tabIndex = 0;
  zoomInput.addEventListener("input", () => {
    const item = state.items.find((i) => i.id === state.selected);
    if (!item) return;
    item.zoom = Number(zoomInput.value);
    renderEditor();
    rerender(item.id);
  });
  new ResizeObserver(() => renderEditor()).observe(stage);

  function clamp(v) {
    return Math.max(0, Math.min(1, v));
  }

  // ---------------- Encoding ----------------
  async function encode(item) {
    const s = settings();
    const [W, H] = outputSize(item, s);
    const out = document.createElement("canvas");
    out.width = W;
    out.height = H;
    draw(out.getContext("2d"), item, W, H, s);
    if (s.target) {
      const r = await compressCanvasToTarget(out, s.format, s.target, { allowResize: false });
      return { blob: r.blob, width: W, height: H, fits: r.fits, format: s.format };
    }
    const blob = await encodeCanvas(out, s.format, 90);
    return { blob, width: W, height: H, fits: true, format: s.format };
  }

  const pending = new Set();
  let running = false;
  async function processPending() {
    if (running) return;
    running = true;
    try {
      while (pending.size) {
        const id = pending.values().next().value;
        pending.delete(id);
        const item = state.items.find((i) => i.id === id);
        if (!item) continue;
        item.status = "converting";
        renderList();
        try {
          const result = await encode(item);
          if (item.thumbUrl) URL.revokeObjectURL(item.thumbUrl);
          item.result = result;
          item.thumbUrl = URL.createObjectURL(result.blob);
          item.status = "done";
        } catch (err) {
          item.status = "error";
          notice("Le traitement de " + item.name + " a échoué (" + (err && err.message ? err.message : "erreur inconnue") + ").");
        }
        renderList();
      }
    } finally {
      running = false;
    }
  }
  const rerender = debounce((id) => {
    if (id) pending.add(id);
    else state.items.forEach((i) => pending.add(i.id));
    processPending();
  }, 250);

  // ---------------- File list ----------------
  function fileName(item) {
    const r = item.result;
    return outputFileName(item.name, FORMATS[r.format].exts[0]).replace(/(\.[a-z]+)$/, "-" + r.width + "x" + r.height + "$1");
  }

  function renderList() {
    const count = state.items.length;
    toolMain.classList.toggle("has-files", count > 0);
    filesBox.classList.toggle("is-visible", count > 0);
    list.innerHTML = "";
    for (const item of state.items) {
      const row = el("li", "file is-" + item.status + (item.id === state.selected ? " is-selected" : ""));
      if (item.status === "done" && !item.result.fits) row.classList.add("is-over");
      const thumb = el("span", "file__thumb");
      if (item.thumbUrl) {
        const img = el("img");
        img.src = item.thumbUrl;
        img.alt = "";
        thumb.appendChild(img);
      }
      row.appendChild(thumb);

      const name = el("button", "file__name file__pick");
      name.type = "button";
      name.title = "Cadrer cette image";
      name.appendChild(el("span", "file__filename", item.name));
      let conv = "En attente";
      if (item.status === "done") {
        const r = item.result;
        conv = r.width + "×" + r.height + " px · " + FORMATS[r.format].label;
        if (!r.fits) conv += " · au-dessus du poids maximum";
      } else if (item.status === "converting") conv = "Traitement…";
      else if (item.status === "error") conv = "Échec";
      name.appendChild(el("span", "file__conv", conv));
      name.addEventListener("click", () => {
        state.selected = item.id;
        renderList();
        renderEditor();
      });
      row.appendChild(name);

      row.appendChild(el("span", "file__bar"));
      row.appendChild(el("span", "file__size", item.status === "done" ? formatBytes(item.result.blob.size) : ""));
      row.appendChild(el("span", "file__gain", ""));
      if (item.status === "done") {
        const dl = el("button", "file__dl");
        dl.type = "button";
        const fname = fileName(item);
        dl.title = "Télécharger " + fname;
        dl.setAttribute("aria-label", "Télécharger " + fname);
        dl.innerHTML = DOWNLOAD_ICON;
        dl.addEventListener("click", () => triggerDownload(item.result.blob, fname));
        row.appendChild(dl);
      } else {
        row.appendChild(el("span", "file__dl-slot"));
      }
      list.appendChild(row);
    }
    const done = state.items.filter((i) => i.status === "done");
    const s = settings();
    summary.textContent = count === 0 ? "" :
      count + " image" + (count > 1 ? "s" : "") +
      (count > 1 ? " · cliquez sur un nom pour la cadrer" : "") +
      (s.target ? " · max " + formatBytes(s.target) : "");
    zipButton.hidden = done.length < 2;
  }

  zipButton.addEventListener("click", async () => {
    const done = state.items.filter((i) => i.status === "done");
    zipButton.disabled = true;
    try {
      await downloadAsZip(done.map((i) => ({ name: fileName(i), blob: i.result.blob })), config.zipName || "images.zip");
    } finally {
      zipButton.disabled = false;
    }
  });

  // ---------------- Intake + settings ----------------
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
        const source = await decodeToCanvas(file, formatId, "png");
        const item = { id: crypto.randomUUID(), name: file.name, source, zoom: 1, fx: 0.5, fy: 0.5, status: "waiting" };
        state.items.push(item);
        if (!state.selected) state.selected = item.id;
        pending.add(item.id);
      } catch (err) {
        rejected++;
      }
    }
    if (rejected) notice(rejected + " fichier" + (rejected > 1 ? "s ignorés : format" : " ignoré : format") + " non pris en charge ou illisible.");
    renderList();
    renderEditor();
    processPending();
  }
  bindDropzone(addFiles, { accept: acceptAttrForAny() });

  function syncFace(select) {
    const card = select.closest(".fcard");
    if (card) card.querySelector("[data-fcard-label]").textContent = select.options[select.selectedIndex].textContent;
  }
  function syncKeep() {
    heightInput.disabled = keepInput.checked;
  }
  [formatSelect, targetSelect].forEach((sel) =>
    sel.addEventListener("change", () => {
      syncFace(sel);
      renderEditor();
      rerender();
    })
  );
  keepInput.addEventListener("change", () => {
    syncKeep();
    renderEditor();
    rerender();
  });
  [widthInput, heightInput].forEach((input) =>
    input.addEventListener("input", () => {
      renderEditor();
      rerender();
    })
  );
  syncKeep();
}
