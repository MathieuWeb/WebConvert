// Remove photo metadata (/supprimer-metadonnees-photo/). Shows what each
// photo reveals (GPS position, device, date...) read with exifr, then
// strips it:
//   - JPG, PNG, WebP: the metadata blocks are cut out of the file, pixels
//     untouched (no re-encoding, no quality loss);
//   - a JPG whose EXIF orientation isn't "normal" (most phone photos taken
//     sideways) is re-encoded upright instead, since removing the tag would
//     leave it displayed rotated;
//   - HEIC, AVIF, TIFF: re-encoded as JPG, which carries no metadata.
import { FORMATS } from "../formats-data.js";
import { decodeToCanvas, encodeCanvas, formatIdForFile, outputFileName } from "../conversion.js";
import { downloadAsZip, triggerDownload } from "../zip.js";
import { formatBytes, el, bindDropzone, notice, DOWNLOAD_ICON } from "../common.js";

const EXIFR = "https://cdn.jsdelivr.net/npm/exifr@7.1.3/dist/full.esm.mjs";
const LOSSLESS = new Set(["jpg", "png", "webp"]);
const REENCODE = new Set(["heic", "avif", "tiff"]);

let exifrPromise = null;
function loadExifr() {
  if (!exifrPromise) exifrPromise = import(EXIFR).then((m) => m.default ?? m);
  return exifrPromise;
}

export function init(config) {
  const $ = (sel) => document.querySelector(sel);
  const toolMain = $("[data-tool]");
  const filesBox = $("[data-queue-card]");
  const list = $("[data-queue-list]");
  const summary = $("[data-queue-summary]");
  const zipButton = $("[data-download-all]");
  const state = { items: [] };

  async function addFiles(files) {
    notice("");
    let rejected = 0;
    for (const file of files) {
      const formatId = formatIdForFile(file);
      if (!formatId || !(LOSSLESS.has(formatId) || REENCODE.has(formatId))) {
        rejected++;
        continue;
      }
      const item = { id: crypto.randomUUID(), file, name: file.name, formatId, status: "converting", meta: null };
      state.items.push(item);
      render();
      try {
        item.meta = await readMeta(file);
        item.result = await clean(file, formatId, item.meta);
        item.thumbUrl = URL.createObjectURL(item.result.blob);
        item.status = "done";
      } catch (err) {
        item.status = "error";
        notice("Le nettoyage de " + file.name + " a échoué (" + (err && err.message ? err.message : "erreur inconnue") + ").");
      }
      render();
    }
    if (rejected) notice(rejected + " fichier" + (rejected > 1 ? "s ignorés" : " ignoré") + " : formats pris en charge JPG, PNG, WebP, HEIC, AVIF et TIFF.");
  }
  bindDropzone(addFiles, { accept: ".jpg,.jpeg,.png,.webp,.heic,.heif,.avif,.tif,.tiff,image/jpeg,image/png,image/webp,image/heic,image/avif,image/tiff" });

  function outName(item) {
    const ext = item.result.format === item.formatId ? item.name.split(".").pop() : FORMATS[item.result.format].exts[0];
    return outputFileName(item.name, ext).replace(/(\.[A-Za-z0-9]+)$/, "-sans-metadonnees$1");
  }

  function render() {
    const count = state.items.length;
    toolMain.classList.toggle("has-files", count > 0);
    filesBox.classList.toggle("is-visible", count > 0);
    list.innerHTML = "";
    for (const item of state.items) {
      const row = el("li", "file file--meta is-" + item.status);
      const thumb = el("span", "file__thumb");
      if (item.thumbUrl) {
        const img = el("img");
        img.src = item.thumbUrl;
        img.alt = "";
        thumb.appendChild(img);
      }
      row.appendChild(thumb);
      const name = el("span", "file__name");
      name.appendChild(el("span", "file__filename", item.name));
      let line = item.status === "converting" ? "Analyse…" : item.status === "error" ? "Échec" : item.result.note;
      name.appendChild(el("span", "file__conv", line));
      row.appendChild(name);
      row.appendChild(el("span", "file__bar"));
      row.appendChild(el("span", "file__size", item.status === "done" ? formatBytes(item.file.size) + " → " + formatBytes(item.result.blob.size) : ""));
      row.appendChild(el("span", "file__gain", item.status === "done" ? "Nettoyée" : ""));
      if (item.status === "done") {
        const dl = el("button", "file__dl");
        dl.type = "button";
        const fname = outName(item);
        dl.title = "Télécharger " + fname;
        dl.setAttribute("aria-label", "Télécharger " + fname);
        dl.innerHTML = DOWNLOAD_ICON;
        dl.addEventListener("click", () => triggerDownload(item.result.blob, fname));
        row.appendChild(dl);
      } else {
        row.appendChild(el("span", "file__dl-slot"));
      }
      if (item.status === "done") row.appendChild(metaList(item.meta));
      list.appendChild(row);
    }
    const done = state.items.filter((i) => i.status === "done");
    const withGps = done.filter((i) => i.meta && i.meta.gps).length;
    summary.textContent = count === 0 ? "" :
      count + " photo" + (count > 1 ? "s" : "") + " · " + done.length + " nettoyée" + (done.length > 1 ? "s" : "") +
      (withGps ? " · " + withGps + " contenai" + (withGps > 1 ? "ent" : "t") + " une position GPS" : "");
    zipButton.hidden = done.length < 2;
  }

  zipButton.addEventListener("click", async () => {
    const done = state.items.filter((i) => i.status === "done");
    zipButton.disabled = true;
    try {
      await downloadAsZip(done.map((i) => ({ name: outName(i), blob: i.result.blob })), config.zipName || "photos-sans-metadonnees.zip");
    } finally {
      zipButton.disabled = false;
    }
  });
}

// ---------------- Reading ----------------
async function readMeta(file) {
  let tags = null;
  try {
    const exifr = await loadExifr();
    tags = await exifr.parse(file, { tiff: true, exif: true, gps: true, xmp: true, iptc: true, icc: false, mergeOutput: true, translateValues: false });
  } catch {
    tags = null; // unreadable or no metadata: still cleaned below
  }
  if (!tags) return { count: 0, orientation: 1 };
  const meta = { count: Object.keys(tags).length, orientation: Number(tags.Orientation) || 1 };
  if (typeof tags.latitude === "number" && typeof tags.longitude === "number") {
    meta.gps = { lat: tags.latitude, lon: tags.longitude };
  }
  const device = [tags.Make, tags.Model].filter(Boolean).join(" ").replace(/\s+/g, " ").trim();
  if (device) meta.device = device;
  const date = tags.DateTimeOriginal || tags.CreateDate || tags.ModifyDate;
  if (date) meta.date = date instanceof Date ? date.toLocaleString("fr-FR") : String(date);
  if (tags.Software) meta.software = String(tags.Software);
  const who = [tags.Artist, tags.Copyright, tags.creator, tags.Creator].filter(Boolean).map(String);
  if (who.length) meta.author = [...new Set(who)].join(", ");
  if (tags.LensModel) meta.lens = String(tags.LensModel);
  return meta;
}

function metaList(meta) {
  const box = el("div", "meta");
  if (!meta || meta.count === 0) {
    box.appendChild(el("p", "meta__none", "Aucune métadonnée lisible trouvée : le fichier est rendu propre par précaution."));
    return box;
  }
  const dl = el("dl", "meta__list");
  const add = (term, value, node) => {
    dl.appendChild(el("dt", null, term));
    const dd = el("dd", null, value);
    if (node) dd.appendChild(node);
    dl.appendChild(dd);
  };
  if (meta.gps) {
    const coords = meta.gps.lat.toFixed(5) + ", " + meta.gps.lon.toFixed(5);
    const link = el("a", "meta__map", "voir sur une carte ↗");
    link.href = "https://www.openstreetmap.org/?mlat=" + meta.gps.lat + "&mlon=" + meta.gps.lon + "#map=16/" + meta.gps.lat + "/" + meta.gps.lon;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.title = "Ouvre OpenStreetMap dans un nouvel onglet (les coordonnées sont envoyées à ce site)";
    add("Position GPS", coords + " · ", link);
  }
  if (meta.device) add("Appareil", meta.device);
  if (meta.lens) add("Objectif", meta.lens);
  if (meta.date) add("Prise de vue", meta.date);
  if (meta.software) add("Logiciel", meta.software);
  if (meta.author) add("Auteur", meta.author);
  add("Total", meta.count + " information" + (meta.count > 1 ? "s" : "") + " supprimée" + (meta.count > 1 ? "s" : ""));
  box.appendChild(dl);
  return box;
}

// ---------------- Cleaning ----------------
async function clean(file, formatId, meta) {
  const bytes = new Uint8Array(await file.arrayBuffer());
  if (formatId === "jpg" && meta.orientation === 1) {
    return { blob: new Blob([stripJpeg(bytes)], { type: "image/jpeg" }), format: "jpg", note: "Métadonnées retirées, image intacte" };
  }
  if (formatId === "png") {
    return { blob: new Blob([stripPng(bytes)], { type: "image/png" }), format: "png", note: "Métadonnées retirées, image intacte" };
  }
  if (formatId === "webp") {
    return { blob: new Blob([stripWebp(bytes)], { type: "image/webp" }), format: "webp", note: "Métadonnées retirées, image intacte" };
  }
  // Rotated JPG, HEIC, AVIF, TIFF: redraw upright (browsers apply the EXIF
  // orientation when decoding) and re-encode as a metadata-free JPG.
  const canvas = await decodeToCanvas(file, formatId, "jpg");
  const blob = await encodeCanvas(canvas, "jpg", 95);
  const why = formatId === "jpg" ? "réencodée (qualité 95) pour garder la bonne orientation" : "convertie en JPG (qualité 95), sans métadonnées";
  return { blob, format: "jpg", note: "Métadonnées retirées, " + why };
}

/** JPEG: drop APP1 (EXIF, XMP), APP13 (IPTC/Photoshop) and COM segments;
 * keep JFIF, ICC colour profile (APP2), Adobe (APP14) and all image data. */
function stripJpeg(b) {
  if (b[0] !== 0xff || b[1] !== 0xd8) throw new Error("JPEG invalide");
  const out = [b.subarray(0, 2)];
  let i = 2;
  while (i < b.length) {
    if (b[i] !== 0xff) throw new Error("structure JPEG inattendue");
    const marker = b[i + 1];
    if (marker === 0xda) { // start of scan: the rest is image data
      out.push(b.subarray(i));
      break;
    }
    if (marker === 0xd8 || (marker >= 0xd0 && marker <= 0xd7) || marker === 0x01) {
      out.push(b.subarray(i, i + 2));
      i += 2;
      continue;
    }
    const len = (b[i + 2] << 8) | b[i + 3];
    const seg = b.subarray(i, i + 2 + len);
    const drop = marker === 0xe1 || marker === 0xed || marker === 0xfe;
    if (!drop) out.push(seg);
    i += 2 + len;
  }
  return concat(out);
}

/** PNG: drop textual and EXIF chunks (tEXt, zTXt, iTXt, eXIf) and tIME. */
function stripPng(b) {
  const sig = b.subarray(0, 8);
  const out = [sig];
  let i = 8;
  const drop = new Set(["tEXt", "zTXt", "iTXt", "eXIf", "tIME"]);
  while (i < b.length) {
    const len = ((b[i] << 24) >>> 0) + (b[i + 1] << 16) + (b[i + 2] << 8) + b[i + 3];
    const type = String.fromCharCode(b[i + 4], b[i + 5], b[i + 6], b[i + 7]);
    const end = i + 12 + len;
    if (!drop.has(type)) out.push(b.subarray(i, end));
    i = end;
    if (type === "IEND") break;
  }
  return concat(out);
}

/** WebP (RIFF): drop EXIF and XMP chunks and clear their VP8X flags. */
function stripWebp(b) {
  const tag = (o) => String.fromCharCode(b[o], b[o + 1], b[o + 2], b[o + 3]);
  if (tag(0) !== "RIFF" || tag(8) !== "WEBP") throw new Error("WebP invalide");
  const out = [];
  let i = 12;
  while (i + 8 <= b.length) {
    const type = tag(i);
    const len = b[i + 4] | (b[i + 5] << 8) | (b[i + 6] << 16) | (b[i + 7] << 24);
    const end = i + 8 + len + (len & 1);
    if (type !== "EXIF" && type !== "XMP ") {
      const chunk = b.slice(i, end);
      if (type === "VP8X") chunk[8] &= ~(0x08 | 0x04); // EXIF and XMP flags
      out.push(chunk);
    }
    i = end;
  }
  const body = concat(out);
  const header = new Uint8Array(12);
  header.set(b.subarray(0, 12));
  const size = body.length + 4;
  header[4] = size & 0xff;
  header[5] = (size >> 8) & 0xff;
  header[6] = (size >> 16) & 0xff;
  header[7] = (size >> 24) & 0xff;
  return concat([header, body]);
}

function concat(parts) {
  const total = parts.reduce((s, p) => s + p.length, 0);
  const out = new Uint8Array(total);
  let o = 0;
  for (const p of parts) {
    out.set(p, o);
    o += p.length;
  }
  return out;
}
