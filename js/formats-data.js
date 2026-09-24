// Single client-side registry of every image format the site knows about.
// Mirrors the FORMATS dict in build/generate.py (which renders the pages
// that reference these ids) — keep the two in sync when adding a format.
export const FORMATS = {
  jpg: { id: "jpg", label: "JPG", exts: ["jpg", "jpeg"], mime: "image/jpeg", canDecode: true, canEncode: true, lossy: true },
  png: { id: "png", label: "PNG", exts: ["png"], mime: "image/png", canDecode: true, canEncode: true, lossy: false },
  webp: { id: "webp", label: "WebP", exts: ["webp"], mime: "image/webp", canDecode: true, canEncode: true, lossy: true },
  avif: { id: "avif", label: "AVIF", exts: ["avif"], mime: "image/avif", canDecode: true, canEncode: true, lossy: true },
  gif: { id: "gif", label: "GIF", exts: ["gif"], mime: "image/gif", canDecode: true, canEncode: false, lossy: false },
  bmp: { id: "bmp", label: "BMP", exts: ["bmp"], mime: "image/bmp", canDecode: true, canEncode: true, lossy: false },
  ico: { id: "ico", label: "ICO", exts: ["ico"], mime: "image/x-icon", canDecode: true, canEncode: true, lossy: false },
  svg: { id: "svg", label: "SVG", exts: ["svg"], mime: "image/svg+xml", canDecode: true, canEncode: false, lossy: false },
  tiff: { id: "tiff", label: "TIFF", exts: ["tiff", "tif"], mime: "image/tiff", canDecode: true, canEncode: false, lossy: false },
  heic: { id: "heic", label: "HEIC", exts: ["heic", "heif"], mime: "image/heic", canDecode: true, canEncode: false, lossy: false },
};

export const INPUT_FORMAT_IDS = Object.values(FORMATS).filter((f) => f.canDecode).map((f) => f.id);
export const OUTPUT_FORMAT_IDS = Object.values(FORMATS).filter((f) => f.canEncode).map((f) => f.id);

export function acceptAttrFor(formatId) {
  const fmt = FORMATS[formatId];
  return [fmt.mime, ...fmt.exts.map((e) => "." + e)].join(",");
}

export function acceptAttrForAny() {
  return INPUT_FORMAT_IDS.map((id) => acceptAttrFor(id)).join(",");
}
