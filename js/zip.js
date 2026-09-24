// JSZip is the site's one bundling dependency, fetched from the CDN only
// when the user actually clicks "Tout télécharger" — nothing loads it on
// first paint.
let jszipPromise = null;

async function loadJSZip() {
  if (!jszipPromise) {
    jszipPromise = import("https://cdn.jsdelivr.net/npm/jszip@3.10.1/+esm").then(
      (mod) => mod.default ?? mod
    );
  }
  return jszipPromise;
}

/**
 * Build a ZIP from converted results and trigger a download.
 * @param {{name: string, blob: Blob}[]} files
 */
export async function downloadAsZip(files, zipName = "webconvert.zip") {
  const JSZip = await loadJSZip();
  const zip = new JSZip();
  for (const { name, blob } of files) {
    zip.file(name, blob);
  }
  const zipBlob = await zip.generateAsync({ type: "blob" });
  triggerDownload(zipBlob, zipName);
}

export function triggerDownload(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 4000);
}
