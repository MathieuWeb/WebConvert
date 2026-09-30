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

ICON_LINKS = (
    '<link rel="icon" type="image/x-icon" href="/assets/icons/favicon.ico" />\n'
    '<link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32x32.png" />\n'
    '<link rel="icon" type="image/png" sizes="16x16" href="/assets/icons/favicon-16x16.png" />\n'
    '<link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png" />\n'
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
    }
    return (f'<svg class="icon" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
            f'{paths[name]}</svg>')


# ---------------------------------------------------------------------------
# <head> + shell
# ---------------------------------------------------------------------------

def render_page(*, path, title, meta_description, body_html, json_ld=None,
                 include_js=False, wc_config=None, og_alt=None, robots=None, canonical=True):
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
{app_js_html}</body>
</html>
"""


def site_header(current_path):
    def cur(prefix):
        return ' aria-current="page"' if current_path.startswith(prefix) else ""
    return f"""<header role="banner" class="site-header wrap">
  <a href="/" class="brand"><span class="brand__mark" aria-hidden="true"></span>Webconvert</a>
  <nav class="site-nav" aria-label="Navigation principale">
    <a href="/#formats">Formats</a>
    <a href="/compresser-image/"{cur('/compresser')}>Compresser</a>
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


def _app_html(aria_label, dz_title, side_controls):
    return f"""<section class="app wrap" aria-label="{aria_label}">
  <div class="app__side">
    {side_controls}

    <p class="app__privacy">{icon("lock", 16)}<span>Traitement local&nbsp;: aucune image n'est envoyée sur internet.</span></p>
  </div>

  <div class="app__main" data-tool>
    <div class="dropzone" data-dropzone>
      <div class="dropzone__text">
        <p class="dropzone__title">{dz_title}</p>
        <p class="dropzone__hint">ou glissez-les ici</p>
      </div>
      <button type="button" class="btn btn--dark" data-pick-button>Choisir des fichiers</button>
      <input type="file" data-file-input class="visually-hidden" multiple tabindex="-1" aria-label="Choisir des fichiers image à convertir" />
    </div>

    <p class="tool-notice" data-tool-notice role="alert"></p>

    <div class="files" data-queue-card>
      <ul class="files__list" data-queue-list aria-label="Fichiers"></ul>
      <div class="files__foot">
        <span class="files__summary" data-queue-summary aria-live="polite"></span>
        <button type="button" class="btn btn--dark" data-download-all>Tout télécharger (ZIP)</button>
      </div>
    </div>
  </div>
</section>"""


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
    return f"""    <ul class="pair-list{extra}">
{rows}
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
