// Real client-side image conversion. Nothing here ever touches the network
// for the images themselves: files stay in memory in this tab. A handful of
// pure decoder/encoder libraries (TIFF, HEIC, ZIP) are fetched lazily from a
// CDN only when a file of that exact format needs them — never the images.
import { FORMATS } from "./formats-data.js";

/** Quality slider is 40-100 (design/UX scale); canvas.toBlob expects 0-1. */
export function sliderToCanvasQuality(sliderValue) {
  return sliderValue / 100;
}

export function outputFileName(originalName, ext) {
  const dot = originalName.lastIndexOf(".");
  const base = dot > 0 ? originalName.slice(0, dot) : originalName;
  return base + "." + ext;
}

/** Guess the registered format id for a File, from its extension first (most
 * reliable across OSes/browsers), falling back to the reported MIME type. */
export function formatIdForFile(file) {
  const name = file.name || "";
  const dot = name.lastIndexOf(".");
  const ext = dot > -1 ? name.slice(dot + 1).toLowerCase() : "";
  for (const fmt of Object.values(FORMATS)) {
    if (fmt.exts.includes(ext)) return fmt.id;
  }
  for (const fmt of Object.values(FORMATS)) {
    if (fmt.mime === file.type) return fmt.id;
  }
  return null;
}

// ---------------- Lazy third-party loading ----------------
const scriptPromises = new Map();
function loadScriptOnce(src) {
  if (!scriptPromises.has(src)) {
    scriptPromises.set(
      src,
      new Promise((resolve, reject) => {
        const s = document.createElement("script");
        s.src = src;
        s.onload = () => resolve();
        s.onerror = () => reject(new Error("Impossible de charger " + src));
        document.head.appendChild(s);
      })
    );
  }
  return scriptPromises.get(src);
}

async function ensureTiffDecoder() {
  await loadScriptOnce("https://cdn.jsdelivr.net/npm/pako@2.1.0/dist/pako.min.js");
  await loadScriptOnce("https://cdn.jsdelivr.net/npm/utif@3.1.0/UTIF.js");
}

async function ensureHeicDecoder() {
  await loadScriptOnce("https://cdn.jsdelivr.net/npm/heic2any@0.0.4/dist/heic2any.min.js");
}

// ---------------- Decoding (any accepted format -> a drawable canvas) ----------------

/** Decode a raster File/Blob into an ImageBitmap, with an <img> fallback for
 * browsers/formats createImageBitmap rejects (some SVGs, older Safari). The
 * blob's MIME is forced to the format's registered MIME so decoding does not
 * depend on the OS/browser having set file.type correctly (notably SVG). */
async function decodeRaster(file, formatId) {
  const mime = FORMATS[formatId].mime;
  const blob = file.type === mime ? file : new Blob([await file.arrayBuffer()], { type: mime });
  if (typeof createImageBitmap === "function") {
    try {
      return await createImageBitmap(blob);
    } catch {
      // fall through to the <img> fallback below
    }
  }
  const url = URL.createObjectURL(blob);
  try {
    const img = new Image();
    img.decoding = "async";
    await new Promise((resolve, reject) => {
      img.onload = resolve;
      img.onerror = () => reject(new Error("Décodage impossible pour " + file.name));
      img.src = url;
    });
    return img;
  } finally {
    URL.revokeObjectURL(url);
  }
}

async function decodeTiff(file) {
  await ensureTiffDecoder();
  const buf = await file.arrayBuffer();
  const ifds = window.UTIF.decode(buf);
  if (!ifds.length) throw new Error("TIFF illisible");
  window.UTIF.decodeImage(buf, ifds[0]);
  const rgba = window.UTIF.toRGBA8(ifds[0]);
  const width = ifds[0].width;
  const height = ifds[0].height;
  const canvas = document.createElement("canvas");
  canvas.width = width;
  canvas.height = height;
  canvas.getContext("2d").putImageData(new ImageData(new Uint8ClampedArray(rgba), width, height), 0, 0);
  return canvas;
}

async function decodeHeic(file) {
  await ensureHeicDecoder();
  const converted = await window.heic2any({ blob: file, toType: "image/png", quality: 0.92 });
  const pngBlob = Array.isArray(converted) ? converted[0] : converted;
  return decodeRaster(pngBlob, "png");
}

/** Decode any accepted format into a drawable source (ImageBitmap, <img> or
 * <canvas>), all of which `ctx.drawImage()` accepts identically. */
async function decodeSource(file, formatId) {
  if (formatId === "tiff") return decodeTiff(file);
  if (formatId === "heic") return decodeHeic(file);
  return decodeRaster(file, formatId);
}

// ---------------- Encoding (canvas -> Blob in the target format) ----------------

const encodeSupportCache = new Map();
/** Feature-detect canvas.toBlob support for a MIME type (relevant for AVIF,
 * whose browser support varies), cached after the first probe. */
export function supportsEncoding(mime) {
  if (encodeSupportCache.has(mime)) return encodeSupportCache.get(mime);
  const probe = new Promise((resolve) => {
    try {
      const c = document.createElement("canvas");
      c.width = 1;
      c.height = 1;
      c.toBlob((blob) => resolve(!!blob && blob.type === mime), mime);
    } catch {
      resolve(false);
    }
  });
  encodeSupportCache.set(mime, probe);
  return probe;
}

function canvasToBlob(canvas, mime, quality) {
  return new Promise((resolve, reject) => {
    canvas.toBlob((blob) => (blob ? resolve(blob) : reject(new Error("Échec de l'encodage " + mime))), mime, quality);
  });
}

/** 24-bit uncompressed BMP (BITMAPINFOHEADER), bottom-up row order, rows
 * padded to a 4-byte boundary. Canvas.toBlob has no BMP support in any
 * browser, so this is a small hand-rolled encoder. */
function encodeBmp(canvas) {
  const w = canvas.width;
  const h = canvas.height;
  const data = canvas.getContext("2d").getImageData(0, 0, w, h).data;
  const rowSize = Math.floor((w * 3 + 3) / 4) * 4;
  const pixelArraySize = rowSize * h;
  const fileSize = 54 + pixelArraySize;
  const buffer = new ArrayBuffer(fileSize);
  const view = new DataView(buffer);

  view.setUint8(0, 0x42);
  view.setUint8(1, 0x4d);
  view.setUint32(2, fileSize, true);
  view.setUint32(10, 54, true);
  view.setUint32(14, 40, true);
  view.setInt32(18, w, true);
  view.setInt32(22, h, true);
  view.setUint16(26, 1, true);
  view.setUint16(28, 24, true);
  view.setUint32(30, 0, true);
  view.setUint32(34, pixelArraySize, true);
  view.setInt32(38, 2835, true);
  view.setInt32(42, 2835, true);

  let offset = 54;
  for (let y = h - 1; y >= 0; y--) {
    for (let x = 0; x < w; x++) {
      const i = (y * w + x) * 4;
      view.setUint8(offset++, data[i + 2]);
      view.setUint8(offset++, data[i + 1]);
      view.setUint8(offset++, data[i]);
    }
    offset += rowSize - w * 3;
  }
  return Promise.resolve(new Blob([buffer], { type: "image/bmp" }));
}

/** ICO container wrapping a single PNG-compressed image (the modern ICO
 * format, supported everywhere since Windows Vista). Capped to 256px, the
 * spec's practical maximum and the standard favicon size. */
async function encodeIco(canvas) {
  const MAX = 256;
  let src = canvas;
  if (canvas.width > MAX || canvas.height > MAX) {
    const scale = MAX / Math.max(canvas.width, canvas.height);
    const w = Math.max(1, Math.round(canvas.width * scale));
    const h = Math.max(1, Math.round(canvas.height * scale));
    src = document.createElement("canvas");
    src.width = w;
    src.height = h;
    src.getContext("2d").drawImage(canvas, 0, 0, w, h);
  }
  const pngBlob = await canvasToBlob(src, "image/png");
  const pngBuf = await pngBlob.arrayBuffer();
  const headerSize = 6 + 16;
  const buffer = new ArrayBuffer(headerSize + pngBuf.byteLength);
  const view = new DataView(buffer);
  view.setUint16(0, 0, true);
  view.setUint16(2, 1, true);
  view.setUint16(4, 1, true);
  view.setUint8(6, src.width >= 256 ? 0 : src.width);
  view.setUint8(7, src.height >= 256 ? 0 : src.height);
  view.setUint8(8, 0);
  view.setUint8(9, 0);
  view.setUint16(10, 1, true);
  view.setUint16(12, 32, true);
  view.setUint32(14, pngBuf.byteLength, true);
  view.setUint32(18, headerSize, true);
  new Uint8Array(buffer, headerSize).set(new Uint8Array(pngBuf));
  return new Blob([buffer], { type: "image/x-icon" });
}

const NATIVE_ENCODE_MIME = { jpg: "image/jpeg", png: "image/png", webp: "image/webp", avif: "image/avif" };

async function encodeCanvas(canvas, outputFormatId, sliderQuality) {
  const quality = sliderToCanvasQuality(sliderQuality);
  if (outputFormatId in NATIVE_ENCODE_MIME) {
    return canvasToBlob(canvas, NATIVE_ENCODE_MIME[outputFormatId], quality);
  }
  if (outputFormatId === "bmp") return encodeBmp(canvas);
  if (outputFormatId === "ico") return encodeIco(canvas);
  throw new Error("Format de sortie non pris en charge : " + outputFormatId);
}

// ---------------- Public conversion entry point ----------------

/**
 * Convert a single image file from `inputFormatId` to `outputFormatId` at the
 * given slider quality (40-100, ignored by lossless outputs).
 * @param {File|Blob} file
 * @param {string} inputFormatId
 * @param {number} sliderQuality
 * @param {string} outputFormatId
 */
export async function convertImage(file, inputFormatId, sliderQuality, outputFormatId) {
  const source = await decodeSource(file, inputFormatId);
  const width = source.width ?? source.naturalWidth;
  const height = source.height ?? source.naturalHeight;
  if (!width || !height) {
    throw new Error(
      "Dimensions introuvables pour " + file.name + " (SVG sans largeur/hauteur ni viewBox explicite ?)"
    );
  }

  const canvas = document.createElement("canvas");
  canvas.width = width;
  canvas.height = height;
  const ctx = canvas.getContext("2d");

  // JPG and BMP have no alpha channel: flatten source transparency onto white
  // (what users converting for print/legacy software expect) instead of the
  // black a bare canvas would otherwise produce.
  if (outputFormatId === "jpg" || outputFormatId === "bmp") {
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(0, 0, width, height);
  }
  ctx.drawImage(source, 0, 0, width, height);
  if (source.close) source.close(); // release ImageBitmap memory promptly

  const blob = await encodeCanvas(canvas, outputFormatId, sliderQuality);
  return { blob, width, height };
}
