# -*- coding: utf-8 -*-
"""HTML rendering for every page on Webconvert.fr. Pure string templates,
no external templating dependency.

Design "Pierre": soft stone background, centred headline, and the tool
presented as an application window (sidebar with the format picker and the
quality slider, main pane with the dropzone and the file list). Content
sections below the tool share one layout: heading on the left, content on
the right, separated by hairlines. See README.md, "Charte graphique"."""
import json
from data import FORMATS, INPUT_IDS, OUTPUT_IDS, FEATURED_PAIRS, TARGET_SIZES

BASE_URL = "https://webconvert.fr"
SITE_NAME = "Webconvert.fr"
# Stone background of the site (css --bg); also site.webmanifest colours.
THEME_COLOR = "#e7e4dd"
# Google Analytics 4 measurement ID. Only loaded after the visitor accepts
# the consent banner (js/consent.js); set to "" to remove analytics entirely.
GA_ID = "G-99CDZX4JZD"

AUTHOR_NAME = "Mathieu Perez"
AUTHOR_URL = "https://mathieu-perez.fr"
REPO_URL = "https://github.com/MathieuWeb/WebConvert"
AUTHOR_LD = {"@type": "Person", "name": AUTHOR_NAME, "url": AUTHOR_URL}

# Figtree is self-hosted (css/styles.css @font-face); preload the latin
# subset, needed by every page, so text doesn't flash in the fallback font.
FONTS_LINK = (
    '<link rel="preload" href="/assets/fonts/figtree-latin-wght-normal.woff2" as="font" '
    'type="font/woff2" crossorigin />'
)

# ?v= busts browsers' favicon cache (Chrome keeps the old icon for weeks);
# bump it whenever the icons change. The 192 px PNG is the one Google Search
# prefers for its results (multiple of 48 px).
ICON_VERSION = "2"
ICON_LINKS = (
    f'<link rel="icon" type="image/x-icon" href="/assets/icons/favicon.ico?v={ICON_VERSION}" />\n'
    f'<link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32x32.png?v={ICON_VERSION}" />\n'
    f'<link rel="icon" type="image/png" sizes="192x192" href="/assets/icons/android-chrome-192x192.png?v={ICON_VERSION}" />\n'
    f'<link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png?v={ICON_VERSION}" />\n'
    '<link rel="manifest" href="/site.webmanifest" />'
)


def fmt(id_):
    return FORMATS[id_]


def label(id_):
    return FORMATS[id_]["label"]


def default_output_for(input_id):
    """Sensible default target format so the tool works the instant a file
    is dropped, before the visitor has touched the format picker."""
    return "jpg" if input_id == "webp" else "webp"


# ---------------------------------------------------------------------------
# Inline icons (stroke-based, inherit currentColor — no icon font/request)
# ---------------------------------------------------------------------------

def icon(name, size=18):
    paths = {
        "swap": '<path d="M8 4v16"/><path d="m4 8 4-4 4 4"/><path d="M16 20V4"/><path d="m20 16-4 4-4-4"/>',
        "chevron": '<path d="m6 9 6 6 6-6"/>',
        "lock": '<rect x="4.5" y="10.5" width="15" height="10" rx="2.5"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/>',
        "download": '<path d="M12 4v11"/><path d="m7 10 5 5 5-5"/><path d="M5 20h14"/>',
        # Tool cards (outils): simple stroke pictograms, no brand logos.
        "convert": '<path d="M4 8h13"/><path d="m14 4 4 4-4 4"/><path d="M20 16H7"/><path d="m10 12-4 4 4 4"/>',
        "phone": '<rect x="6.5" y="2.5" width="11" height="19" rx="2.5"/><path d="M10.5 18.5h3"/>',
        "compress": '<path d="M4 14h6v6"/><path d="M20 10h-6V4"/><path d="m14 10 7-7"/><path d="m3 21 7-7"/>',
        "doc": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="m9 14 2 2 4-4"/>',
        "resize": '<path d="M15 3h6v6"/><path d="M9 21H3v-6"/><path d="m21 3-7 7"/><path d="m3 21 7-7"/>',
        "banner": '<rect x="2.5" y="7" width="19" height="10" rx="2"/><path d="m6 14 3-3 3 3 2-2 3 3"/>',
        "portrait": '<rect x="4" y="3" width="16" height="18" rx="2.5"/><circle cx="12" cy="10" r="3"/><path d="M7 18a5 5 0 0 1 10 0"/>',
        "play": '<rect x="2.5" y="5" width="19" height="14" rx="2.5"/><path d="m10 9 5 3-5 3z"/>',
        "smile": '<circle cx="12" cy="12" r="9"/><path d="M8.5 14a4 4 0 0 0 7 0"/><path d="M9 9.5h.01M15 9.5h.01"/>',
        "pdf": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="M9 13h6M9 17h4"/>',
        "pin-off": '<path d="M12 21s-6-5.5-6-11a6 6 0 0 1 10.3-4.2"/><path d="M18 10c0 2.2-1 4.4-2.3 6.3"/><path d="m3 3 18 18"/>',
        "image": '<rect x="3" y="4" width="18" height="16" rx="2.5"/><circle cx="9" cy="10" r="1.8"/><path d="m21 16-5-5-9 9"/>',
    }
    return (f'<svg class="icon" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
            f'{paths[name]}</svg>')


# ---------------------------------------------------------------------------
# <head> + shell
# ---------------------------------------------------------------------------

def render_page(*, path, title, meta_description, body_html, json_ld=None,
                 include_js=False, wc_config=None, og_alt=None, robots=None, canonical=True, extra_scripts=""):
    robots = robots or "index, follow, max-image-preview:large"
    # Google cuts titles around 60 characters: keep the brand suffix only
    # when the whole title still fits (Google usually shows the site name anyway).
    suffix = " | " + SITE_NAME
    if title.endswith(suffix) and len(title) > 60:
        title = title[: -len(suffix)]
    canonical_url = BASE_URL + path
    canonical_html = f'<link rel="canonical" href="{canonical_url}" />\n' if canonical else ""
    og_image_alt = og_alt or (SITE_NAME + " — convertisseur d'images gratuit et local")

    json_ld_html = ""
    if json_ld:
        json_ld_html = '<script type="application/ld+json">' + json.dumps(json_ld, ensure_ascii=False) + "</script>\n"

    wc_config_html = ""
    if wc_config is not None:
        wc_config_html = (
            "<script>\nwindow.WC_CONFIG = " + json.dumps(wc_config, ensure_ascii=False) + ";\n</script>\n"
        )

    consent_html = ""
    if GA_ID:
        consent_html = f'<script src="/js/consent.js" data-ga-id="{GA_ID}" defer></script>\n'

    app_js_html = ""
    if include_js:
        app_js_html = wc_config_html + '<script type="module" src="/js/main.js"></script>\n'

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title}</title>
<meta name="description" content="{meta_description}" />
<meta name="robots" content="{robots}" />
<meta name="theme-color" content="{THEME_COLOR}" />
<meta name="format-detection" content="telephone=no" />
<meta name="apple-mobile-web-app-title" content="Webconvert" />
{canonical_html}
{ICON_LINKS}

<meta property="og:type" content="website" />
<meta property="og:locale" content="fr_FR" />
<meta property="og:site_name" content="{SITE_NAME}" />
<meta property="og:url" content="{canonical_url}" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{meta_description}" />
<meta property="og:image" content="{BASE_URL}/assets/og-image.jpg" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:alt" content="{og_image_alt}" />

<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{title}" />
<meta name="twitter:description" content="{meta_description}" />
<meta name="twitter:image" content="{BASE_URL}/assets/og-image.jpg" />

{json_ld_html}
{FONTS_LINK}
<link rel="stylesheet" href="/css/styles.css" />
{consent_html}</head>
<body>
<a class="skip-link" href="#contenu">Aller au contenu</a>

{site_header(path)}

{body_html}

{site_footer()}
{app_js_html}{extra_scripts}<script src="/js/nav.js" defer></script>
</body>
</html>
"""


# Header "Outils" menu: a few tools per category + link to each category of
# /outils/ (the #hash preselects its filter tab).
NAV_MENU = [
    ("Convertir", "convertir", [("Convertisseur d'images", "/"), ("HEIC en JPG", "/heic-en-jpg/"),
                                ("PNG en WebP", "/png-en-webp/")]),
    ("Compresser", "compresser", [("À une taille précise", "/compresser-image/"),
                                  ("Photo pour l'ANTS", "/compresser-photo-ants/"),
                                  ("Photo pour un e-mail", "/compresser-photo-pour-mail/")]),
    ("Redimensionner", "redimensionner", [("Redimensionner une image", "/redimensionner-image/"),
                                          ("Bannière LinkedIn", "/banniere-linkedin/"),
                                          ("Miniature YouTube", "/miniature-youtube/"),
                                          ("Sticker WhatsApp", "/sticker-whatsapp/")]),
    ("PDF et confidentialité", "pdf", [("Images en PDF", "/images-en-pdf/"),
                                       ("Supprimer les métadonnées", "/supprimer-metadonnees-photo/")]),
]


def nav_menu_html(current_path):
    cols = []
    for name, cat, links in NAV_MENU:
        items = "".join(f'<li><a href="{href}">{text}</a></li>' for text, href in links)
        cols.append(f"""<div class="nav-menu__col">
          <a class="nav-menu__cat" href="/outils/#{cat}">{name}</a>
          <ul>{items}</ul>
        </div>""")
    current = ' aria-current="page"' if current_path.startswith("/outils") else ""
    return f"""<details class="nav-menu" data-nav-menu>
      <summary{current}>Outils {icon("chevron", 14)}</summary>
      <div class="nav-menu__panel">
        {"".join(cols)}
        <a class="nav-menu__all link-arrow" href="/outils/">Voir tous les outils →</a>
      </div>
    </details>"""


def site_header(current_path):
    def cur(prefix):
        return ' aria-current="page"' if current_path.startswith(prefix) else ""
    return f"""<header role="banner" class="site-header wrap">
  <a href="/" class="brand"><span class="brand__mark" aria-hidden="true"></span>Webconvert</a>
  <nav class="site-nav" aria-label="Navigation principale">
    <a href="/#formats">Formats</a>
    {nav_menu_html(current_path)}
    <a href="/guide/"{cur('/guide')}>Guides</a>
    <a href="/#questions">FAQ</a>
  </nav>
</header>"""


def site_footer():
    return """<footer role="contentinfo" class="site-footer">
  <div class="wrap site-footer__bar">
    <span class="site-footer__brand"><span class="brand__mark" aria-hidden="true"></span>Webconvert.fr</span>
    <nav class="site-footer__links" aria-label="Liens de pied de page">
      <a href="/confidentialite/" title="Politique de confidentialité de Webconvert.fr">Confidentialité</a>
      <a href="/guide/" title="Guides Webconvert.fr">Guides</a>
      <a href="/a-propos/">À propos</a>
      <a href="/mentions-legales/">Mentions légales</a>
      <a href="/confidentialite/#cookies" data-consent-open>Gérer les cookies</a>
    </nav>
  </div>
</footer>"""


def breadcrumbs_nav(items):
    """items: [(label, href|None), ...], last item has href=None (current page).
    A single-item trail (homepage) stays in the markup but is visually hidden."""
    parts = []
    for i, (text, href) in enumerate(items):
        if i > 0:
            parts.append('<span class="breadcrumbs__sep" aria-hidden="true">/</span>')
        if href:
            parts.append(f'<a href="{href}">{text}</a>')
        else:
            parts.append(f'<span aria-current="page">{text}</span>')
    hidden = " visually-hidden" if len(items) < 2 else ""
    return f'<nav class="breadcrumbs{hidden}" aria-label="Fil d\'Ariane">' + " ".join(parts) + "</nav>"


def breadcrumb_json_ld(items):
    """items: [(label, href|None), ...] — href None resolved to the canonical of the last entry by caller."""
    elements = []
    for i, (text, href) in enumerate(items):
        elements.append({
            "@type": "ListItem", "position": i + 1, "name": text,
            "item": (BASE_URL + href) if href else None,
        })
    return elements


# ---------------------------------------------------------------------------
# Tool pages (home, hubs, pairs): intro + application window
# ---------------------------------------------------------------------------

def intro_html(*, crumbs, h1, subtitle):
    """Centred headline above the tool. On desktop the block has a fixed
    height and its text is bottom-aligned, so the tool window below starts
    at exactly the same y on every tool page, whatever the headline length."""
    return f"""<div class="intro wrap">
  {breadcrumbs_nav(crumbs)}
  <div class="intro__text">
    <h1>{h1}</h1>
    <p>{subtitle}</p>
  </div>
</div>"""


def format_picker_html(preset_from=None, preset_to=None, default_output="webp", to_only_ids=None):
    """The single format-selection widget, identical on every page (home,
    hub, pair): "De" and "Vers" fields in the tool's sidebar. Each field is
    a native <select> stretched invisibly over a styled face, so it stays
    fully keyboard/screen-reader accessible; only the pre-selected options
    change between pages, never the sizes or positions."""
    def options(ids, placeholder, selected=None):
        opts = [f'<option value="">{placeholder}</option>']
        for i in ids:
            sel = " selected" if i == selected else ""
            opts.append(f'<option value="{i}"{sel}>{label(i)}</option>')
        return "\n".join(opts)

    def field(role, ids, selected, aria, face_empty, hint_empty, placeholder):
        face = label(selected) if selected else face_empty
        empty = "" if selected else " is-empty"
        return f"""    <label class="fcard{empty}">
      <span class="fcard__label" data-fcard-label>{face}</span>
      <span class="fcard__hint">{hint_empty}</span>
      <span class="fcard__chevron">{icon("chevron", 16)}</span>
      <select class="fcard__select" data-picker-{role} aria-label="{aria}">
{options(ids, placeholder, selected)}
      </select>
    </label>"""

    if to_only_ids:
        # Compression pages: output format only, changed in place (no "De",
        # no swap, no navigation), pre-selected on the page's default.
        return f"""<form class="picker" data-format-picker>
  <div class="picker__field">
    <div class="side-label"><span>Format de sortie</span></div>
{field("to", to_only_ids, default_output, "Format de sortie", label(default_output), "", "Choisir un format")}
  </div>
</form>"""

    can_swap = bool(preset_from and preset_to and preset_from in OUTPUT_IDS and preset_to in INPUT_IDS)
    swap_attrs = "" if can_swap else " disabled"
    swap_title = (f"Inverser : {label(preset_to)} en {label(preset_from)}" if can_swap
                  else "Choisissez deux formats pour inverser la conversion")

    return f"""<form class="picker" data-format-picker>
  <div class="picker__field">
    <div class="side-label"><span>De</span></div>
{field("from", INPUT_IDS, preset_from, "Format d'origine", "Tous", f"{len(INPUT_IDS)} formats", "Tous les formats")}
  </div>
  <div class="picker__field">
    <div class="side-label"><span>Vers</span>
      <button type="button" class="swap" data-picker-swap title="{swap_title}" aria-label="{swap_title}"{swap_attrs}>{icon("swap", 15)}<span>Inverser</span></button>
    </div>
{field("to", OUTPUT_IDS, preset_to, "Format de sortie", label(default_output), "par défaut", f"{label(default_output)} (par défaut)")}
  </div>
</form>"""


TARGET_OUTPUT_IDS = ["jpg", "webp", "avif", "png"]


def target_field_html(target_bytes):
    """"Poids maximum" field of the compression pages: same styled-select
    component as the format fields, changed in place by js/ui.js."""
    opts = []
    face = None
    for _slug, bytes_, text in TARGET_SIZES:
        sel = ""
        if bytes_ == target_bytes:
            sel, face = " selected", text
        opts.append(f'        <option value="{bytes_}"{sel}>{text}</option>')
    return f"""<div class="picker__field">
      <div class="side-label"><span>Poids maximum</span></div>
      <label class="fcard">
        <span class="fcard__label" data-fcard-label>{face}</span>
        <span class="fcard__hint">par image</span>
        <span class="fcard__chevron">{icon("chevron", 16)}</span>
        <select class="fcard__select" data-target-select aria-label="Poids maximum par image">
{chr(10).join(opts)}
        </select>
      </label>
    </div>
    <p class="quality__note">Meilleure qualité possible sous cette limite ; les dimensions ne sont réduites que si nécessaire.</p>"""


def tool_markup(*, input_id, preset_from=None, preset_to=None, default_output="webp", target=None):
    """The application window: sidebar (format picker, quality, privacy
    note) + main pane (dropzone, then the file list rendered by js/ui.js).
    Same shape everywhere, so switching pages never moves the controls.
    With `target` (bytes), it becomes the compressor of the /compresser-*
    pages: output format + "Poids maximum" instead of the quality slider."""
    if input_id == "any":
        dz_title = "Sélectionnez vos images"
    else:
        dz_title = f"Sélectionnez vos fichiers {fmt(input_id)['label']}"

    if target:
        return _app_html(
            "Compresseur", dz_title,
            format_picker_html(default_output=default_output, to_only_ids=TARGET_OUTPUT_IDS)
            + "\n\n    " + target_field_html(target))
    return _app_html(
        "Convertisseur", dz_title,
        format_picker_html(preset_from, preset_to, default_output) + "\n\n    " + QUALITY_HTML)


QUALITY_HTML = """<div class="quality" data-quality-card>
      <div class="quality__row">
        <span class="side-label" id="quality-label"><span>Qualité d'encodage</span></span>
        <span class="quality__value"><span data-quality-number>80</span> · <span data-quality-tier>Équilibré</span></span>
      </div>
      <div class="slider" data-quality-slider tabindex="0" role="slider" aria-labelledby="quality-label"
        aria-valuemin="40" aria-valuemax="100" aria-valuenow="80">
        <div class="slider__track"><div class="slider__fill" data-quality-fill></div></div>
        <div class="slider__thumb" data-quality-thumb></div>
      </div>
      <p class="quality__note" data-quality-note>Réglage conseillé pour le web.</p>
    </div>"""


def _app_html(aria_label, dz_title, side_controls, main_extra="", tool_class="", multiple=True,
              dz_hint="ou glissez-les ici", pick_label="Choisir des fichiers", zip_label="Tout télécharger (ZIP)"):
    cls = "app wrap" + (f" {tool_class}" if tool_class else "")
    multi = " multiple" if multiple else ""
    return f"""<section class="{cls}" aria-label="{aria_label}">
  <div class="app__side">
    {side_controls}

    <p class="app__privacy">{icon("lock", 16)}<span>Traitement local&nbsp;: aucune image n'est envoyée sur internet.</span></p>
  </div>

  <div class="app__main" data-tool>
    <div class="dropzone" data-dropzone>
      <div class="dropzone__text">
        <p class="dropzone__title">{dz_title}</p>
        <p class="dropzone__hint">{dz_hint}</p>
      </div>
      <button type="button" class="btn btn--dark" data-pick-button>{pick_label}</button>
      <input type="file" data-file-input class="visually-hidden"{multi} tabindex="-1" aria-label="Choisir des fichiers image" />
    </div>

    <p class="tool-notice" data-tool-notice role="alert"></p>
{main_extra}
    <div class="files" data-queue-card>
      <ul class="files__list" data-queue-list aria-label="Fichiers"></ul>
      <div class="files__foot">
        <span class="files__summary" data-queue-summary aria-live="polite"></span>
        <button type="button" class="btn btn--dark" data-download-all>{zip_label}</button>
      </div>
    </div>
  </div>
</section>"""


def select_field_html(label_text, data_attr, options, selected, aria, hint=""):
    """A sidebar field with the same styled-select face as the format
    picker. options: [(value, text)]."""
    face = next((t for v, t in options if str(v) == str(selected)), options[0][1])
    opts = "\n".join(
        f'        <option value="{v}"{" selected" if str(v) == str(selected) else ""}>{t}</option>'
        for v, t in options)
    hint_html = f'<span class="fcard__hint">{hint}</span>' if hint else ""
    return f"""<div class="picker__field">
      <div class="side-label"><span>{label_text}</span></div>
      <label class="fcard">
        <span class="fcard__label" data-fcard-label>{face}</span>
        {hint_html}
        <span class="fcard__chevron">{icon("chevron", 16)}</span>
        <select class="fcard__select" {data_attr} aria-label="{aria}">
{opts}
        </select>
      </label>
    </div>"""


def weight_options(none_label="Aucun"):
    return [("", none_label)] + [(b, t) for _s, b, t in TARGET_SIZES]


def resize_tool_markup(*, width, height, output="jpg", target=None, keep_ratio=False, formats=("jpg", "png", "webp")):
    """Exact-size tool: dimensions, output format, optional weight limit;
    main pane gets a crop editor (drag to frame, zoom) above the file list.
    With keep_ratio (generic /redimensionner-image/), only the width is
    imposed and nothing is cropped."""
    ratio_checked = " checked" if keep_ratio else ""
    side = f"""<div class="picker__field">
      <div class="side-label"><span>Dimensions (px)</span></div>
      <div class="dims">
        <label class="dims__box"><span class="visually-hidden">Largeur en pixels</span>
          <input type="number" min="1" max="10000" inputmode="numeric" value="{width}" data-resize-width /></label>
        <span class="dims__x" aria-hidden="true">×</span>
        <label class="dims__box"><span class="visually-hidden">Hauteur en pixels</span>
          <input type="number" min="1" max="10000" inputmode="numeric" value="{height or ''}" data-resize-height /></label>
      </div>
      <label class="check"><input type="checkbox" data-resize-keep{ratio_checked} /> Conserver les proportions (sans recadrage)</label>
    </div>

    {select_field_html("Format de sortie", "data-resize-format", [(f, label(f)) for f in formats], output, "Format de sortie")}

    {select_field_html("Poids maximum", "data-resize-target", weight_options("Sans limite"), target or "", "Poids maximum par image")}"""
    editor = """    <div class="editor" data-editor hidden>
      <div class="editor__stage" data-editor-stage>
        <canvas class="editor__canvas" data-editor-canvas aria-label="Aperçu du cadrage : faites glisser l'image pour la cadrer"></canvas>
      </div>
      <div class="editor__bar">
        <label class="editor__zoom"><span>Zoom</span>
          <input type="range" min="1" max="4" step="0.01" value="1" data-editor-zoom /></label>
        <span class="editor__hint" data-editor-hint>Faites glisser l'image pour la cadrer</span>
      </div>
    </div>
"""
    return _app_html("Redimensionner", "Sélectionnez vos images", side, main_extra=editor, tool_class="app--resize")


def pdf_tool_markup(*, target=None):
    """Images -> PDF: page size, margins, optional weight limit; the file
    list is reorderable (up/down) and one PDF is produced."""
    side = f"""{select_field_html("Format des pages", "data-pdf-page", [("a4", "A4 portrait"), ("a4l", "A4 paysage"), ("fit", "Taille de chaque image")], "a4", "Format des pages")}

    {select_field_html("Marges", "data-pdf-margin", [("10", "Petites (10 mm)"), ("0", "Aucune"), ("20", "Grandes (20 mm)")], "10", "Marges")}

    {select_field_html("Poids maximum du PDF", "data-pdf-target", weight_options("Sans limite") + [(10_000_000, "10 Mo")], target or "", "Poids maximum du PDF")}"""
    return _app_html("Images en PDF", "Sélectionnez vos images", side, tool_class="app--pdf",
                     zip_label="Télécharger le PDF")


def exif_tool_markup():
    side = """<div class="picker__field">
      <div class="side-label"><span>Ce qui est supprimé</span></div>
      <ul class="side-list">
        <li>Position GPS</li>
        <li>Date et heure de prise de vue</li>
        <li>Marque et modèle de l'appareil</li>
        <li>Logiciel, auteur, copyright</li>
        <li>Miniature intégrée</li>
      </ul>
      <p class="quality__note">JPG, PNG et WebP sont nettoyés sans réencodage : l'image reste identique au pixel près.</p>
    </div>"""
    return _app_html("Supprimer les métadonnées", "Sélectionnez vos photos", side, tool_class="app--exif",
                     zip_label="Tout télécharger (ZIP)")


# ---------------------------------------------------------------------------
# Content sections below the tool: heading left, content right
# ---------------------------------------------------------------------------

def section_html(heading_id, heading, body, intro=None, tag="section", extra_class=""):
    intro_html = f'\n    <p class="sec__intro">{intro}</p>' if intro else ""
    cls = "sec wrap" + (f" {extra_class}" if extra_class else "")
    return f"""<{tag} class="{cls}" aria-labelledby="{heading_id}">
  <div class="sec__head">
    <h2 id="{heading_id}">{heading}</h2>{intro_html}
  </div>
  <div class="sec__body">
{body}
  </div>
</{tag}>"""


def faq_html(items, heading_id="questions", heading="Questions fréquentes"):
    rows = []
    for q, a in items:
        rows.append(f"""    <div class="faq-item" data-faq-item data-open="false">
      <h3><button type="button" class="faq-item__trigger" data-faq-trigger aria-expanded="false">
        <span>{q}</span>
        <span class="faq-item__sign" data-faq-sign aria-hidden="true">+</span>
      </button></h3>
      <p class="faq-item__answer">{a}</p>
    </div>""")
    return section_html(heading_id, heading, "\n".join(rows), extra_class="faq")


def faq_json_ld(items):
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in items
        ],
    }


PRIVACY_FAQ = [
    ("Mes images sont-elles envoyées quelque part ?",
     "Non. Tout le traitement se déroule dans votre navigateur grâce à l'API Canvas. Aucun fichier ni aucune "
     "miniature ne quitte votre machine pendant la conversion."),
    ("Y a-t-il une limite de taille ou de nombre de fichiers ?",
     "La seule limite est la mémoire disponible sur votre appareil. Des lots de plusieurs dizaines d'images "
     "passent sans problème sur une machine récente."),
]


def pair_list_html(pairs, cls=""):
    """pairs: [(from_label, to_label, desc, href)] — rows 'PNG → WebP'."""
    rows = "\n".join(
        f"""      <li><a href="{href}"><span class="pair">{a} → {b}</span><span class="pair__desc">{desc}</span></a></li>"""
        for a, b, desc, href in pairs
    )
    extra = f" {cls}" if cls else ""
    return f"""    <ul class="pair-list{extra}">
{rows}
    </ul>"""


def format_catalog_html(pairs, pairs_heading="Conversions courantes", heading="Formats pris en charge"):
    """Format chips (every readable format, links to its hub page), the
    formats Webconvert can write, and a short list of common conversions."""
    def chips(ids):
        return "\n".join(f'      <a class="chip" href="/convertisseur-{i}/">{label(i)}</a>' for i in ids)
    body = f"""    <div class="catalog__group">
      <p class="catalog__label">Formats d'entrée · {len(INPUT_IDS)}</p>
      <div class="chips">
{chips(INPUT_IDS)}
      </div>
    </div>
    <div class="catalog__group">
      <p class="catalog__label">Formats de sortie · {len(OUTPUT_IDS)}</p>
      <div class="chips">
{chips(OUTPUT_IDS)}
      </div>
    </div>
    <div class="catalog__group">
      <p class="catalog__label">{pairs_heading}</p>
{pair_list_html(pairs)}
    </div>"""
    return section_html(
        "formats", heading, body,
        intro=f"Webconvert lit {len(INPUT_IDS)} formats d'image et en écrit {len(OUTPUT_IDS)}. Choisissez un format pour voir toutes ses conversions.",
        extra_class="catalog")


def link_list_html(items, cls="pair-list--cols"):
    """items: [(title, desc, href)] — same look as the pair rows, for links
    that aren't "X → Y" conversions (compression thresholds, démarches)."""
    rows = "\n".join(
        f"""      <li><a href="{href}"><span class="pair">{title}</span><span class="pair__desc">{desc}</span></a></li>"""
        for title, desc, href in items
    )
    extra = f" {cls}" if cls else ""
    return f"""    <ul class="pair-list pair-list--stack{extra}">
{rows}
    </ul>"""


def tool_cards_html(cards):
    """cards: [dict(title, desc, href, cat, icon)] — the iLoveIMG-style grid
    (homepage and /outils/). data-cat drives the category filter."""
    items = "\n".join(
        f"""    <li data-cat="{c['cat']}"><a class="tool-card" href="{c['href']}">
      <span class="tool-card__icon">{icon(c['icon'], 26)}</span>
      <span class="tool-card__title">{c['title']}</span>
      <span class="tool-card__desc">{c['desc']}</span>
    </a></li>"""
        for c in cards)
    return f"""<ul class="tool-cards">
{items}
  </ul>"""


def pair_list_section_html(heading_id, heading, pairs, intro=None):
    """Pair list as a section of its own (hub pages: every conversion from
    one format; pair pages: see also)."""
    return section_html(heading_id, heading, pair_list_html(pairs, "pair-list--cols"), intro=intro)


def privacy_aside_html():
    items = [
        ("Traitement local :", "chaque image est décodée et ré-encodée par votre propre navigateur."),
        ("Aucun envoi :", "aucune requête réseau ne transporte vos fichiers, vérifiable dans l'onglet Réseau."),
        ("Gratuit, sans compte :", "pas de serveur de conversion à rentabiliser, donc rien à vous faire payer."),
    ]
    rows = "\n".join(f"""      <li><strong>{title}</strong> {text}</li>""" for title, text in items)
    body = f"""    <ul class="points">
{rows}
    </ul>
    <p><a class="link-arrow" href="/confidentialite/">Lire la politique de confidentialité →</a></p>"""
    return section_html("securite", "Vos fichiers restent chez vous", body,
                        intro="Webconvert ne voit jamais vos images : il n'existe aucun serveur qui pourrait les recevoir.",
                        tag="aside")


def quality_aside_html():
    items = [
        ("Qualité réglable :", "un curseur pour arbitrer entre poids et netteté sur les formats avec perte."),
        ("Traitement par lot :", "déposez des dizaines d'images, récupérez-les une à une ou dans un ZIP."),
        ("Transparence préservée :", "le canal alpha est conservé dès que le format de sortie le permet."),
    ]
    rows = "\n".join(f"""      <li><strong>{title}</strong> {text}</li>""" for title, text in items)
    body = f"""    <ul class="points">
{rows}
    </ul>"""
    return section_html("qualite", "Des conversions soignées", body, tag="aside")


def format_info_html(ids):
    """One short description per format (+ link to its hub page), side by
    side — shown on pair pages under the "Pourquoi convertir" heading."""
    items = []
    for i in ids:
        f = FORMATS[i]
        items.append(f"""      <div class="duo__item">
        <h3>{f['label']} <span class="duo__sub">— {f['short']}</span></h3>
        <p>{f['what_it_is']}</p>
        <a class="link-arrow" href="/convertisseur-{i}/">Convertisseur {f['label']} →</a>
      </div>""")
    return '    <div class="duo">\n' + "\n".join(items) + "\n    </div>"


def guide_rows_html(articles, cls=""):
    rows = "\n".join(
        f"""      <li><a href="/guide/{a['slug']}/"><span class="guide-row__title">{a['title']}</span><span class="guide-row__desc">{a['excerpt']}</span></a></li>"""
        for a in articles
    )
    extra = f" {cls}" if cls else ""
    return f"""    <ul class="guide-rows{extra}">
{rows}
    </ul>"""


def guide_grid_html(articles, heading_id="hub-guides", heading="Guides"):
    body = guide_rows_html(articles) + '\n    <p><a class="link-arrow" href="/guide/">Tous les guides →</a></p>'
    return section_html(heading_id, heading, body)


def guide_index_cards_html(articles):
    """The guide index: one row per article inside a window panel."""
    rows = []
    for a in articles:
        rows.append(f"""  <li><a class="guide-item" href="/guide/{a['slug']}/">
    <span class="guide-item__meta">{a['tag']} · {a['reading_time']} de lecture</span>
    <span class="guide-item__title">{a['title']}</span>
    <span class="guide-item__desc">{a['excerpt']}</span>
  </a></li>""")
    return '<ul class="panel guide-list">\n' + "\n".join(rows) + "\n</ul>"
