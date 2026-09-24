# -*- coding: utf-8 -*-
"""HTML rendering for every page on Webconvert.fr. Pure string templates,
no external templating dependency — mirrors the hand-written HTML structure
of the sibling project (webpconvert.fr) so the two sites share one design
language."""
import json
from data import FORMATS, INPUT_IDS, OUTPUT_IDS, FEATURED_PAIRS

BASE_URL = "https://webconvert.fr"
SITE_NAME = "Webconvert.fr"
THEME_COLOR = "#f4efe9"

FONTS_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com" />\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />\n'
    '<link href="https://fonts.googleapis.com/css2?family=Familjen+Grotesk:wght@500;600;700&'
    'family=Instrument+Sans:wght@400;500;600&family=Inconsolata:wght@400;500;600&display=swap" '
    'rel="stylesheet" />'
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


def exts_hint(ids):
    seen = []
    for i in ids:
        for e in FORMATS[i]["exts"]:
            if e not in seen:
                seen.append(e)
    return ", ".join(seen)


# ---------------------------------------------------------------------------
# Inline icons (stroke-based, inherit currentColor — no icon font/request)
# ---------------------------------------------------------------------------

def icon(name, size=18):
    paths = {
        "file": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/>',
        "image": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><circle cx="10" cy="12" r="1.5"/><path d="m19 17-3.5-3.5L8 21"/>',
        "upload": '<path d="M7 18a4.5 4.5 0 0 1-.6-8.96A6 6 0 0 1 18 8.5a4 4 0 0 1-.5 9.5"/><path d="M12 12v8"/><path d="m8.5 15.5 3.5-3.5 3.5 3.5"/>',
        "plus-file": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="M12 11v6"/><path d="M9 14h6"/>',
        "swap": '<path d="M17 4l3 3-3 3"/><path d="M20 7H9"/><path d="M7 20l-3-3 3-3"/><path d="M4 17h11"/>',
        "chevron": '<path d="m6 9 6 6 6-6"/>',
        "shield": '<path d="M12 3 5 6v5c0 4.5 3 8.3 7 10 4-1.7 7-5.5 7-10V6z"/><path d="m9 12 2 2 4-4"/>',
        "grid": '<rect x="4" y="4" width="7" height="7" rx="1.5"/><rect x="13" y="4" width="7" height="7" rx="1.5"/><rect x="4" y="13" width="7" height="7" rx="1.5"/><rect x="13" y="13" width="7" height="7" rx="1.5"/>',
        "cpu": '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M10 10h4v4h-4z"/><path d="M9 3v3M15 3v3M9 18v3M15 18v3M3 9h3M3 15h3M18 9h3M18 15h3"/>',
        "wifi-off": '<path d="M3 3l18 18"/><path d="M8.5 16.5a5 5 0 0 1 7 0"/><path d="M5 12.9a10 10 0 0 1 5.2-2.7M19 12.9a10 10 0 0 0-2.4-1.7"/><path d="M2 9a15 15 0 0 1 4.5-2.8M22 9A15 15 0 0 0 11 5.1"/><circle cx="12" cy="20" r=".5"/>',
        "gift": '<rect x="4" y="9" width="16" height="11" rx="1.5"/><path d="M3 9h18M12 9v11"/><path d="M12 9S10.5 4 8 4a2 2 0 0 0 0 4.5M12 9s1.5-5 4-5a2 2 0 0 1 0 4.5"/>',
        "book": '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 21V5M8 7h7"/>',
        "help": '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 0 1 4.8 1c0 1.7-2.3 2-2.3 3.5"/><circle cx="12" cy="17" r=".5"/>',
        "sliders": '<path d="M4 6h10M18 6h2M4 12h4M12 12h8M4 18h12M20 18h0"/><circle cx="16" cy="6" r="2"/><circle cx="10" cy="12" r="2"/><circle cx="18" cy="18" r="2"/>',
        "arrow": '<path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>',
    }
    return (f'<svg class="icon" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
            f'{paths[name]}</svg>')


# ---------------------------------------------------------------------------
# <head> + shell
# ---------------------------------------------------------------------------

def render_page(*, path, title, meta_description, body_html, json_ld=None,
                 include_js=False, wc_config=None, og_alt=None, robots="index, follow, max-image-preview:large"):
    canonical = BASE_URL + path
    og_image_alt = og_alt or (SITE_NAME + " — convertisseur d'images gratuit et local")

    json_ld_html = ""
    if json_ld:
        json_ld_html = '<script type="application/ld+json">' + json.dumps(json_ld, ensure_ascii=False) + "</script>\n"

    wc_config_html = ""
    if wc_config is not None:
        wc_config_html = (
            "<script>\nwindow.WC_CONFIG = " + json.dumps(wc_config, ensure_ascii=False) + ";\n</script>\n"
        )

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
<link rel="canonical" href="{canonical}" />
<link rel="alternate" hreflang="fr" href="{canonical}" />

{ICON_LINKS}

<meta property="og:type" content="website" />
<meta property="og:locale" content="fr_FR" />
<meta property="og:site_name" content="{SITE_NAME}" />
<meta property="og:url" content="{canonical}" />
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
</head>
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
        return ' is-current" aria-current="page' if current_path.startswith(prefix) else ""
    return f"""<header role="banner" class="site-header">
  <div class="site-header__bar">
    <a href="/" class="brand">
      <span class="brand-mark" aria-hidden="true">
        <span class="brand-mark__tab"></span>
        <span class="brand-mark__lines"><span></span><span></span><span></span></span>
      </span>
      <span class="brand-name">Webconvert<span class="tld">.fr</span></span>
    </a>
    <nav class="site-header__nav" aria-label="Navigation principale">
      <a href="/#formats" class="nav-link">Formats</a>
      <a href="/guide/" class="nav-link{cur('/guide')}">Guides</a>
      <a href="/#questions" class="nav-link">FAQ</a>
    </nav>
    <a href="/confidentialite/" class="site-header__badge" title="Aucun fichier n'est envoyé : tout est converti dans votre navigateur">
      {icon("shield", 16)}<span>100&nbsp;% local</span>
    </a>
  </div>
</header>"""


def site_footer():
    return """<footer role="contentinfo" class="site-footer">
  <div class="site-footer__bar">
    <span class="site-footer__brand">Webconvert.fr</span>
    <a href="/confidentialite/" title="Politique de confidentialité de Webconvert.fr">Confidentialité</a>
    <a href="/guide/" title="Guides Webconvert.fr">Guides</a>
    <a href="https://mathieu-perez.fr" title="Portfolio de Mathieu Perez, créateur de Webconvert.fr">À propos</a>
    <span class="site-footer__push">Aucune donnée collectée</span>
  </div>
</footer>"""


def breadcrumbs_nav(items):
    """items: [(label, href|None), ...], last item has href=None (current page)."""
    parts = []
    for i, (text, href) in enumerate(items):
        if i > 0:
            parts.append('<span aria-hidden="true">/</span>')
        if href:
            parts.append(f'<a href="{href}">{text}</a>')
        else:
            parts.append(f'<span aria-current="page">{text}</span>')
    return '<nav class="breadcrumbs" aria-label="Fil d\'Ariane">' + " ".join(parts) + "</nav>"


def breadcrumbs_html(items):
    """Standalone breadcrumb row for text pages (guides, confidentialité).
    Tool pages put the same breadcrumb inside the hero instead (hero_html)."""
    return f"""<div class="crumbs-bar">
  {breadcrumbs_nav(items)}
</div>"""


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
# Reusable content blocks
# ---------------------------------------------------------------------------

def faq_html(items, heading_id="questions", heading="Questions fréquentes"):
    rows = []
    for q, a in items:
        rows.append(f"""      <div class="faq-item" data-faq-item data-open="false">
        <h3><button type="button" class="faq-item__trigger" data-faq-trigger aria-expanded="false">
          {q}
          <span class="faq-item__sign" data-faq-sign aria-hidden="true">+</span>
        </button></h3>
        <p class="faq-item__answer">{a}</p>
      </div>""")
    return f"""<section class="block faq" aria-labelledby="{heading_id}">
  {section_head("help", heading, heading_id)}
{chr(10).join(rows)}
</section>"""


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


def tool_markup(*, input_id, dropzone_label_override=None):
    """The tool is always the same shape everywhere: dropzone, quality slider,
    queue, results. No output picker lives here — the format-picker above
    (same component on every page) is the only place that chooses formats,
    so the layout never changes shape when a format gets selected."""
    if input_id == "any":
        dz_title = "Sélectionnez vos images"
        formats_hint = exts_hint(INPUT_IDS)
    else:
        f = fmt(input_id)
        dz_title = dropzone_label_override or f"Sélectionnez vos fichiers {f['label']}"
        formats_hint = exts_hint([input_id])

    return f"""<div class="tool-single">
  <div class="card dropzone-card dropzone" data-dropzone>
    <span class="dropzone__icon">{icon("upload", 30)}</span>
    <div class="dropzone__title">{dz_title}</div>
    <div class="dropzone__formats">ou glissez-les ici &nbsp;·&nbsp; <span>{formats_hint}</span></div>
    <button type="button" class="btn btn-primary dropzone__pick" data-pick-button>{icon("plus-file", 18)}<span>Choisir des fichiers</span></button>
    <input type="file" data-file-input class="visually-hidden" multiple aria-label="Choisir des fichiers image à convertir" />
  </div>

  <div class="quality-card" data-quality-card>
    <div class="quality-card__row">
      <span class="quality-card__label">Qualité d'encodage</span>
      <span class="quality-card__value">
        <span class="quality-card__tier" data-quality-tier>Équilibré</span>
        <span class="quality-card__number" data-quality-number>80</span>
      </span>
    </div>
    <div
      class="quality-slider"
      data-quality-slider
      tabindex="0"
      role="slider"
      aria-label="Qualité d'encodage"
      aria-valuemin="40"
      aria-valuemax="100"
      aria-valuenow="80"
    >
      <div class="quality-slider__track">
        <div class="quality-slider__fill" data-quality-fill></div>
      </div>
      <div class="quality-slider__thumb" data-quality-thumb></div>
    </div>
    <p class="quality-card__note" data-quality-note>Réglage conseillé pour le web.</p>
  </div>

  <p class="tool-notice" data-tool-notice role="alert"></p>

  <div class="card queue-card" data-queue-card>
    <div class="queue-card__header">
      <span>File d'attente</span>
      <span data-queue-summary></span>
    </div>
    <div data-queue-list></div>
  </div>
</div>

<section class="card results" data-results aria-live="polite">
  <div class="results__header">
    <div class="results__stat">
      <span class="results__pct" data-results-pct>0%</span>
      <span class="results__detail" data-results-detail></span>
    </div>
    <button type="button" class="btn btn-primary results__download-all" data-download-all>Tout télécharger</button>
  </div>
  <div data-results-list></div>
</section>"""


def format_picker_html(preset_from=None, preset_to=None):
    """The single format-selection widget, identical on every page (home,
    hub, pair): two format cards ("depuis" / "vers") around a swap button.
    Each card is a native <select> stretched invisibly over a styled face,
    so it stays fully keyboard/screen-reader accessible and ui.js keeps
    driving it exactly as before — only the pre-selected options change
    between pages, never the card sizes or positions."""
    def options(ids, placeholder, selected=None):
        opts = [f'<option value="">{placeholder}</option>']
        for i in ids:
            sel = " selected" if i == selected else ""
            opts.append(f'<option value="{i}"{sel}>{label(i)}</option>')
        return "\n".join(opts)

    def card(role, ids, selected, aria, placeholder_face):
        face = label(selected) if selected else placeholder_face
        empty = "" if selected else " is-empty"
        target = " fcard--target" if role == "to" else ""
        return f"""  <label class="fcard{target}{empty}">
    <span class="fcard__icon">{icon("image", 26)}</span>
    <span class="fcard__label" data-fcard-label>{face}</span>
    <span class="fcard__chevron">{icon("chevron", 14)}</span>
    <select class="fcard__select" data-picker-{role} aria-label="{aria}">
{options(ids, "Choisir un format…", selected)}
    </select>
  </label>"""

    can_swap = bool(preset_from and preset_to and preset_from in OUTPUT_IDS and preset_to in INPUT_IDS)
    swap_attrs = "" if can_swap else " disabled"
    swap_title = (f"Inverser : {label(preset_to)} en {label(preset_from)}" if can_swap
                  else "Choisissez deux formats pour inverser la conversion")

    return f"""<form class="format-picker" data-format-picker>
  <div class="format-picker__rings" aria-hidden="true"></div>
{card("from", INPUT_IDS, preset_from, "Format d'origine", "Tous")}
  <div class="format-picker__mid">
    <button type="button" class="format-picker__swap" data-picker-swap title="{swap_title}" aria-label="{swap_title}"{swap_attrs}>{icon("swap", 16)}</button>
    <span class="format-picker__en" aria-hidden="true">en</span>
  </div>
{card("to", OUTPUT_IDS, preset_to, "Format de sortie", "Choisir")}
</form>"""


def hero_html(*, crumbs, h1, subtitle, preset_from=None, preset_to=None):
    """Full-bleed tinted band shared by home, hub and pair pages: text on the
    left, format cards on the right. The band has a fixed height and the
    text reserves room for two lines of headline, so switching formats
    never moves the picker or the tool card that overlaps the band's edge."""
    return f"""<section class="hero">
  <div class="hero__inner">
    <div class="hero__text">
      {breadcrumbs_nav(crumbs)}
      <h1>{h1}</h1>
      <p>{subtitle}</p>
    </div>
    {format_picker_html(preset_from, preset_to)}
  </div>
</section>"""


def section_head(icon_name, heading, heading_id, intro=None):
    """Small accent icon + heading (+ optional lead paragraph), the header
    of every content block below the tool."""
    intro_html = f'\n    <p class="block__intro">{intro}</p>' if intro else ""
    return f"""<div class="block__head">
    <h2 id="{heading_id}"><span class="block__icon">{icon(icon_name, 17)}</span>{heading}</h2>{intro_html}
  </div>"""


def format_catalog_html(pairs, pairs_heading="Conversions courantes", heading="Catalogue des formats"):
    """Monospace format chips (inputs, then outputs) beside a short list of
    common conversions — the format index of the site, on the homepage."""
    def chips(ids):
        return "\n".join(f'        <a class="chip" href="/convertisseur-{i}/">{label(i)}</a>' for i in ids)
    pair_rows = "\n".join(
        f"""        <li><a href="{href}"><span class="pair">{a} {icon("arrow", 13)} {b}</span><span class="pair__desc">{desc}</span></a></li>"""
        for a, b, desc, href in pairs
    )
    return f"""<section class="block catalog" aria-labelledby="formats">
  {section_head("grid", heading, "formats", f"Webconvert lit {len(INPUT_IDS)} formats d'image et en écrit {len(OUTPUT_IDS)}. Choisissez un format pour voir toutes ses conversions.")}
  <div class="catalog__body">
    <div class="catalog__formats">
      <div class="catalog__label"><span>Formats d'entrée</span><span>{len(INPUT_IDS)}</span></div>
      <div class="chips">
{chips(INPUT_IDS)}
      </div>
      <div class="catalog__label"><span>Formats de sortie</span><span>{len(OUTPUT_IDS)}</span></div>
      <div class="chips">
{chips(OUTPUT_IDS)}
      </div>
    </div>
    <div class="catalog__pairs">
      <div class="catalog__label"><span>{pairs_heading}</span></div>
      <ul class="pair-list">
{pair_rows}
      </ul>
    </div>
  </div>
</section>"""


def pair_list_section_html(heading_id, heading, pairs, intro=None, icon_name="grid"):
    """Same pair list as the catalog's right column, as a block of its own
    (hub pages: every conversion from one format)."""
    pair_rows = "\n".join(
        f"""      <li><a href="{href}"><span class="pair">{a} {icon("arrow", 13)} {b}</span><span class="pair__desc">{desc}</span></a></li>"""
        for a, b, desc, href in pairs
    )
    return f"""<section class="block" aria-labelledby="{heading_id}">
  {section_head(icon_name, heading, heading_id, intro)}
  <ul class="pair-list pair-list--grid">
{pair_rows}
  </ul>
</section>"""


def privacy_aside_html():
    items = [
        ("cpu", "Traitement local :", "chaque image est décodée et ré-encodée par votre propre navigateur."),
        ("wifi-off", "Aucun envoi :", "aucune requête réseau ne transporte vos fichiers, vérifiable dans l'onglet Réseau."),
        ("gift", "Gratuit, sans compte :", "pas de serveur de conversion à rentabiliser, donc rien à vous faire payer."),
    ]
    rows = "\n".join(
        f"""    <li><span class="feature-list__icon">{icon(ic, 16)}</span><span><strong>{title}</strong> {text}</span></li>"""
        for ic, title, text in items
    )
    return f"""<aside class="block" aria-labelledby="securite">
  {section_head("shield", "Vos fichiers restent chez vous", "securite", "Webconvert ne voit jamais vos images : il n'existe aucun serveur qui pourrait les recevoir.")}
  <ul class="feature-list">
{rows}
  </ul>
  <a class="link-arrow" href="/confidentialite/">Lire la politique de confidentialité {icon("arrow", 14)}</a>
</aside>"""


def quality_aside_html():
    items = [
        ("sliders", "Qualité réglable :", "un curseur pour arbitrer entre poids et netteté sur les formats avec perte."),
        ("file", "Traitement par lot :", "déposez des dizaines d'images, récupérez-les une à une ou dans un ZIP."),
        ("image", "Transparence préservée :", "le canal alpha est conservé dès que le format de sortie le permet."),
    ]
    rows = "\n".join(
        f"""    <li><span class="feature-list__icon">{icon(ic, 16)}</span><span><strong>{title}</strong> {text}</span></li>"""
        for ic, title, text in items
    )
    return f"""<aside class="block" aria-labelledby="qualite">
  {section_head("sliders", "Des conversions soignées", "qualite")}
  <ul class="feature-list">
{rows}
  </ul>
</aside>"""


def format_info_cards_html(ids):
    """One card per format (description + link to its hub page), side by
    side — shown on pair pages for the source and target formats."""
    cards = []
    for i in ids:
        f = FORMATS[i]
        cards.append(f"""  <article class="format-info">
    <h3><span class="format-info__icon">{icon("image", 18)}</span>{f['label']} <span class="format-info__sub">— {f['short']}</span></h3>
    <p>{f['what_it_is']}</p>
    <a class="link-arrow" href="/convertisseur-{i}/">Convertisseur {f['label']} {icon("arrow", 14)}</a>
  </article>""")
    return '<div class="format-info-grid">\n' + "\n".join(cards) + "\n</div>"


def hub_grid_html(heading_id, heading, items, intro=None):
    cards = "\n".join(
        f"""    <a class="hub-card" href="{href}">
      <div class="hub-card__title">{title}</div>
      <div class="hub-card__desc">{desc}</div>
    </a>"""
        for title, desc, href in items
    )
    intro_html = f'\n  <p class="hub-intro">{intro}</p>' if intro else ""
    return f"""<section class="hub" aria-labelledby="{heading_id}">
  <h2 id="{heading_id}">{heading}</h2>{intro_html}
  <div class="hub-grid">
{cards}
  </div>
</section>"""


def guide_grid_html(articles, heading_id="hub-guides", heading="Guides"):
    cards = "\n".join(
        f"""    <a class="hub-card" href="/guide/{a['slug']}/">
      <div class="hub-card__title">{a['title']}</div>
      <div class="hub-card__desc">{a['excerpt']}</div>
    </a>"""
        for a in articles
    )
    return f"""<section class="block hub" aria-labelledby="{heading_id}">
  {section_head("book", heading, heading_id)}
  <div class="hub-grid">
{cards}
  </div>
</section>"""


def guide_index_cards_html(articles):
    cards = []
    for a in articles:
        cards.append(f"""  <a class="guide-card" href="/guide/{a['slug']}/">
    <span class="guide-card__tag">{a['tag']}</span>
    <div class="guide-card__title">{a['title']}</div>
    <p class="guide-card__desc">{a['excerpt']}</p>
    <span class="guide-card__meta">{a['reading_time']} de lecture</span>
  </a>""")
    return '<div class="guide-grid">\n' + "\n".join(cards) + "\n</div>"


def other_outputs_from(input_id, exclude_output_id):
    items = []
    for o in OUTPUT_IDS:
        if o == input_id or o == exclude_output_id:
            continue
        items.append((f"{label(input_id)} → {label(o)}", f"Convertir en {label(o)}.", f"/{input_id}-en-{o}/"))
    return items


def other_inputs_to(output_id, exclude_input_id):
    items = []
    for i in INPUT_IDS:
        if i == output_id or i == exclude_input_id:
            continue
        items.append((f"{label(i)} → {label(output_id)}", f"Depuis un fichier {label(i)}.", f"/{i}-en-{output_id}/"))
    return items
