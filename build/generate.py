# -*- coding: utf-8 -*-
"""Generates every static page of Webconvert.fr from the data in data.py /
articles.py, using the templates in templates.py. Run with:

    cd build && python3 generate.py

Writes clean-URL pages as <root>/<path>/index.html (served without a
trailing .html by any static file server that resolves directory indexes:
python3 -m http.server, Apache with mod_dir, etc). Also (re)writes
sitemap.xml, robots.txt and site.webmanifest from the same page list.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from data import FORMATS, INPUT_IDS, OUTPUT_IDS, PAIRS, FEATURED_PAIRS, get_pair_copy, get_hub_copy
from articles import ARTICLES
import templates as t

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

SITEMAP_URLS = []  # (path, changefreq, priority)


def write_page(path, html):
    """path like '/' or '/png-en-webp/' -> <ROOT><path>index.html"""
    assert path == "/" or (path.startswith("/") and path.endswith("/"))
    out_dir = os.path.join(ROOT, path.strip("/"))
    os.makedirs(out_dir, exist_ok=True) if path != "/" else None
    out_file = os.path.join(ROOT, "index.html") if path == "/" else os.path.join(out_dir, "index.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html)


def register(path, changefreq, priority):
    SITEMAP_URLS.append((path, changefreq, priority))


# ---------------------------------------------------------------------------
# Homepage
# ---------------------------------------------------------------------------

def build_homepage():
    title = "Convertisseur d'images en ligne gratuit et privé (JPG, PNG, WebP, AVIF, HEIC...) | Webconvert.fr"
    meta = ("Convertissez vos images en ligne entre JPG, PNG, WebP, AVIF, GIF, BMP, ICO, SVG, TIFF et HEIC. "
            "100% dans votre navigateur : aucun fichier envoyé sur un serveur. Gratuit, sans compte.")

    faq_items = [
        ("Mes images sont-elles envoyées quelque part ?",
         "Non. Tout le traitement se déroule dans votre navigateur grâce à l'API Canvas et, pour le HEIC et le "
         "TIFF, à de petites librairies de décodage chargées depuis un CDN public — mais jamais vos fichiers "
         "eux-mêmes. Vous pouvez le vérifier dans l'onglet Réseau de votre navigateur : aucune requête ne "
         "contient vos images."),
        ("Quels formats sont pris en charge ?",
         "En entrée : JPG, PNG, WebP, AVIF, GIF, BMP, ICO, SVG, TIFF et HEIC. En sortie : JPG, PNG, WebP, AVIF, "
         "BMP et ICO. Le détail de chaque conversion possible est listé plus bas sur cette page."),
        ("Le site fonctionne-t-il hors connexion ?",
         "Une fois la page chargée, la conversion elle-même ne nécessite pas le réseau (sauf la toute première "
         "fois pour un fichier HEIC ou TIFF, le temps de charger le petit décodeur correspondant)."),
        ("Y a-t-il une limite de taille ou de nombre de fichiers ?",
         "La seule limite est la mémoire disponible sur votre appareil. Des lots de plusieurs dizaines d'images "
         "passent sans problème sur une machine récente."),
        ("Est-ce vraiment gratuit ?",
         "Oui, sans limite artificielle et sans création de compte. Le site ne fait tourner aucun serveur de "
         "conversion à faire payer : tout le travail est fait par votre propre navigateur."),
    ]

    default_output = t.default_output_for("any")

    catalog_pairs = [(t.label(i), t.label(o), FORMATS[o]["short"].capitalize(), f"/{i}-en-{o}/")
                     for i, o in FEATURED_PAIRS[:5]]

    how_body = """    <div class="prose">
      <p>Chaque fichier est décodé directement par votre navigateur, dessiné sur une zone de dessin invisible (un <code>&lt;canvas&gt;</code> hors écran), puis ré-encodé dans le format choisi via les fonctions natives du navigateur. Pour les formats que les navigateurs ne savent pas lire nativement (HEIC, TIFF), une petite librairie de décodage est chargée à la demande depuis un CDN public — elle traite le fichier localement, sans jamais le transmettre.</p>
      <p>Le résultat est un nouveau fichier, généré en mémoire, que vous téléchargez directement. Votre fichier d'origine n'est jamais modifié ni envoyé où que ce soit.</p>
      <p>C'est la même approche que <a href="/guide/confidentialite-conversion-image-navigateur/">l'article sur la confidentialité</a> détaille plus en profondeur : à la différence d'un convertisseur classique, il n'y a structurellement rien à intercepter, puisqu'aucune requête réseau ne transporte vos images.</p>
    </div>"""

    body = f"""<main id="contenu">
{t.intro_html(
        crumbs=[("Accueil", None)],
        h1="Convertisseur d'images en ligne, gratuit et privé",
        subtitle="JPG, PNG, WebP, AVIF, HEIC et bien d'autres. Tout se passe dans votre navigateur : vos fichiers ne quittent jamais votre appareil.",
    )}
{t.tool_markup(input_id="any", default_output=default_output)}

{t.format_catalog_html(catalog_pairs)}
{t.section_html("comment-ca-marche", "Comment fonctionne la conversion", how_body, tag="article")}
{t.privacy_aside_html()}
{t.quality_aside_html()}
{t.guide_grid_html(ARTICLES[-3:][::-1], heading_id="hub-guides", heading="Derniers guides")}
{t.faq_html(faq_items)}
</main>"""

    json_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebSite", "@id": BASE_ID("#website"), "url": t.BASE_URL + "/", "name": t.SITE_NAME,
             "inLanguage": "fr-FR", "description": "Convertisseur d'images gratuit et 100% local."},
            {"@type": "WebApplication", "@id": BASE_ID("#app"), "name": t.SITE_NAME, "url": t.BASE_URL + "/",
             "applicationCategory": "MultimediaApplication", "operatingSystem": "Tout navigateur web",
             "browserRequirements": "Navigateur compatible HTML5 Canvas", "inLanguage": "fr-FR",
             "description": "Convertisseur d'images multi-formats fonctionnant entièrement dans le navigateur, "
                             "sans envoi de fichier sur un serveur.",
             "featureList": ["Conversion par lot", "Qualité d'encodage réglable", "Téléchargement groupé en ZIP",
                              "Traitement local sans upload", "10 formats d'entrée, 6 formats de sortie"],
             "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}},
            t.faq_json_ld(faq_items) | {"@id": BASE_ID("#faq")},
            {"@type": "Organization", "@id": BASE_ID("#organization"), "name": t.SITE_NAME, "url": t.BASE_URL + "/",
             "logo": t.BASE_URL + "/assets/logo-square.png"},
        ],
    }

    html = t.render_page(
        path="/", title=title, meta_description=meta, body_html=body, json_ld=json_ld,
        include_js=True,
        wc_config={"input": "any", "output": default_output, "zipName": "webconvert.zip"},
    )
    write_page("/", html)
    register("/", "weekly", "1.0")


def BASE_ID(fragment):
    return t.BASE_URL + "/" + fragment


# ---------------------------------------------------------------------------
# Hub pages: /convertisseur-{format}/
# ---------------------------------------------------------------------------

def build_hub_page(input_id):
    f = FORMATS[input_id]
    override = get_hub_copy(input_id)
    others = [o for o in OUTPUT_IDS if o != input_id]

    page_title = (override["title"] if override else f"Convertisseur {f['label']} en ligne") + " | Webconvert.fr"
    h1 = override["title"] if override else f"Convertisseur {f['label']} en ligne"
    meta = override["meta"] if override else (
        f"Convertissez vos fichiers {f['label']} en {', '.join(t.label(o) for o in others)} directement dans "
        f"votre navigateur. Gratuit, rapide, sans envoi de fichier sur un serveur."
    )
    subtitle = override["intro"] if override else (
        f"{f['short'].capitalize()} : convertissez-les vers {', '.join(t.label(o) for o in others)} en un clic."
    )

    conv_items = [
        (f["label"], t.label(o), FORMATS[o]["short"].capitalize(), f"/{input_id}-en-{o}/")
        for o in others
    ]

    strengths = "".join(f"<li>{s}</li>" for s in f["strengths"])
    weaknesses = "".join(f"<li>{s}</li>" for s in f["weaknesses"])
    note_p = ""
    for key in ("decode_note", "encode_note"):
        if f.get(key):
            note_p = f"<p>{f[key]}</p>"

    faq_items = list(t.PRIVACY_FAQ)
    faq_items.append((
        f"Quels sont les points forts et les limites du {f['label']} ?",
        "Points forts : " + " ; ".join(f["strengths"]).lower() + ". Limites : " + " ; ".join(f["weaknesses"]).lower() + "."
    ))

    about_body = f"""    <div class="prose">
      <p>{f['what_it_is']}</p>
      <p>Points forts :</p>
      <ul>{strengths}</ul>
      <p>Limites :</p>
      <ul>{weaknesses}</ul>
      {note_p}
    </div>"""
    default_output = t.default_output_for(input_id)

    body = f"""<main id="contenu">
{t.intro_html(
        crumbs=[("Accueil", "/"), (f"Convertisseur {f['label']}", None)],
        h1=h1, subtitle=subtitle,
    )}
{t.tool_markup(input_id=input_id, preset_from=input_id, default_output=default_output)}

{t.pair_list_section_html("hub-conversions", f"Conversions depuis {f['label']}", conv_items,
                              intro=f"Choisissez le format de sortie de vos fichiers {f['label']}.")}
{t.section_html("a-propos-format", f"Le format {f['label']}", about_body, tag="article")}
{t.privacy_aside_html()}
{t.faq_html(faq_items)}
</main>"""

    json_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "BreadcrumbList", "itemListElement": t.breadcrumb_json_ld([("Accueil", "/"), (f"Convertisseur {f['label']}", f"/convertisseur-{input_id}/")])},
            {"@type": "WebApplication", "@id": BASE_ID(f"convertisseur-{input_id}/#app"),
             "name": f"Convertisseur {f['label']}", "url": t.BASE_URL + f"/convertisseur-{input_id}/",
             "applicationCategory": "MultimediaApplication", "operatingSystem": "Tout navigateur web",
             "browserRequirements": "Navigateur compatible HTML5 Canvas", "inLanguage": "fr-FR",
             "description": meta, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}},
            t.faq_json_ld(faq_items),
        ],
    }

    html = t.render_page(
        path=f"/convertisseur-{input_id}/", title=page_title, meta_description=meta, body_html=body,
        json_ld=json_ld, include_js=True,
        wc_config={"input": input_id, "output": t.default_output_for(input_id),
                   "zipName": f"convertisseur-{input_id}.zip"},
    )
    write_page(f"/convertisseur-{input_id}/", html)
    register(f"/convertisseur-{input_id}/", "monthly", "0.8")


# ---------------------------------------------------------------------------
# Pair pages: /{input}-en-{output}/
# ---------------------------------------------------------------------------

def build_generic_pair_copy(i, o):
    fi, fo = FORMATS[i], FORMATS[o]
    title = f"Convertir {fi['label']} en {fo['label']}"
    meta = (f"Convertissez vos fichiers {fi['label']} en {fo['label']} gratuitement, 100% dans votre "
            f"navigateur. Aucun fichier envoyé sur un serveur.")
    intro = f"Vos fichiers {fi['label']} deviennent des {fo['label']}, {fo['output_benefit']}."
    paragraphs = [
        fi["what_it_is"],
        f"En convertissant vers {fo['label']}, vous obtenez {fo['output_benefit']}. {fo['what_it_is']}",
    ]
    faq = [
        ("Mes fichiers sont-ils envoyés quelque part ?",
         "Non. Tout le traitement se déroule dans votre navigateur ; aucun fichier ni aucune miniature ne "
         "quitte votre machine."),
        (f"Puis-je convertir plusieurs {fi['label']} à la fois ?",
         "Oui, déposez-en autant que vous voulez : ils sont convertis en lot puis téléchargeables un par un ou "
         "groupés dans une archive ZIP."),
    ]
    return dict(title=title, meta=meta, intro=intro, paragraphs=paragraphs, faq=faq)


def build_pair_page(i, o):
    fi, fo = FORMATS[i], FORMATS[o]
    override = get_pair_copy(i, o)
    copy = override if override else build_generic_pair_copy(i, o)

    page_title = copy["title"] + " | Webconvert.fr"
    h1 = copy["title"]
    meta = copy["meta"]
    subtitle = copy["intro"]

    notes = []
    for fmt_ in (fi, fo):
        for key in ("decode_note", "encode_note"):
            if fmt_.get(key):
                notes.append(fmt_[key])

    faq_items = list(copy["faq"])
    if notes:
        faq_items.append(("Y a-t-il des limites à connaître ?", " ".join(notes)))

    see_also = []
    if o in INPUT_IDS and i in OUTPUT_IDS:
        see_also.append((fo["label"], fi["label"], "Le sens inverse.", f"/{o}-en-{i}/"))
    for other_o in OUTPUT_IDS:
        if other_o in (o, i):
            continue
        see_also.append((fi["label"], t.label(other_o), f"Convertir en {t.label(other_o)}.", f"/{i}-en-{other_o}/"))
        if len(see_also) >= 5:
            break

    paragraphs_html = "".join(f"<p>{p}</p>" for p in copy["paragraphs"])

    why_body = f"""    <div class="prose">
      {paragraphs_html}
    </div>
{t.format_info_html([i, o])}"""

    body = f"""<main id="contenu">
{t.intro_html(
        crumbs=[("Accueil", "/"), (f"Convertisseur {fi['label']}", f"/convertisseur-{i}/"), (f"{fi['label']} en {fo['label']}", None)],
        h1=h1, subtitle=subtitle,
    )}
{t.tool_markup(input_id=i, preset_from=i, preset_to=o, default_output=o)}

{t.section_html("a-propos-conversion", f"Pourquoi convertir {fi['label']} en {fo['label']}", why_body, tag="article")}
{t.privacy_aside_html()}
{t.pair_list_section_html("hub-autres", "Voir aussi", see_also)}
{t.faq_html(faq_items)}
</main>"""

    json_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "BreadcrumbList", "itemListElement": t.breadcrumb_json_ld([
                ("Accueil", "/"), (f"Convertisseur {fi['label']}", f"/convertisseur-{i}/"),
                (f"{fi['label']} en {fo['label']}", f"/{i}-en-{o}/"),
            ])},
            {"@type": "WebApplication", "@id": BASE_ID(f"{i}-en-{o}/#app"),
             "name": f"Convertisseur {fi['label']} vers {fo['label']}", "url": t.BASE_URL + f"/{i}-en-{o}/",
             "applicationCategory": "MultimediaApplication", "operatingSystem": "Tout navigateur web",
             "browserRequirements": "Navigateur compatible HTML5 Canvas", "inLanguage": "fr-FR",
             "description": meta, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}},
            t.faq_json_ld(faq_items),
        ],
    }

    html = t.render_page(
        path=f"/{i}-en-{o}/", title=page_title, meta_description=meta, body_html=body,
        json_ld=json_ld, include_js=True,
        wc_config={"input": i, "output": o, "zipName": f"{i}-en-{o}.zip"},
    )
    write_page(f"/{i}-en-{o}/", html)
    priority = "0.9" if (i, o) in FEATURED_PAIRS else "0.6"
    register(f"/{i}-en-{o}/", "monthly", priority)


# ---------------------------------------------------------------------------
# Guide
# ---------------------------------------------------------------------------

def build_guide_index():
    title = "Guides : formats d'image, confidentialité et performance web | Webconvert.fr"
    meta = ("Guides pratiques sur les formats d'image (WebP, AVIF, HEIC...), la confidentialité et la "
            "performance web, pour bien choisir et convertir vos images.")
    body = f"""<main id="contenu" class="wrap page">
  <div class="page-intro">
    {t.breadcrumbs_nav([("Accueil", "/"), ("Guides", None)])}
    <h1>Guides</h1>
    <p>Formats d'image, confidentialité et performance web : de quoi convertir vos images en connaissance de cause.</p>
  </div>

  {t.guide_index_cards_html(ARTICLES[::-1])}
</main>"""
    html = t.render_page(path="/guide/", title=title, meta_description=meta, body_html=body)
    write_page("/guide/", html)
    register("/guide/", "weekly", "0.7")


def build_guide_article(article):
    page_title = article["title"] + " | Webconvert.fr"
    body = f"""<main id="contenu" class="wrap page">
  <article class="article">
    {t.breadcrumbs_nav([("Accueil", "/"), ("Guides", "/guide/"), (article["title"], None)])}
    <p class="article__meta">{article['tag']} · {article['published']} · {article['reading_time']} de lecture</p>
    <h1>{article['title']}</h1>
    <p class="lede">{article['lede']}</p>
    {article['body_html']}

    <div class="article-footer-cta">
      <h2>Convertissez vos images maintenant</h2>
      <p>Le convertisseur Webconvert.fr traite vos fichiers directement dans votre navigateur, gratuitement et sans limite.</p>
      <p><a class="btn btn--dark" href="/">Ouvrir le convertisseur →</a></p>
    </div>
  </article>
</main>"""

    json_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "BreadcrumbList", "itemListElement": t.breadcrumb_json_ld([
                ("Accueil", "/"), ("Guides", "/guide/"), (article["title"], f"/guide/{article['slug']}/"),
            ])},
            {"@type": "Article", "headline": article["title"], "description": article["meta"],
             "datePublished": article["published"], "inLanguage": "fr-FR",
             "author": {"@type": "Organization", "name": t.SITE_NAME},
             "publisher": {"@type": "Organization", "name": t.SITE_NAME, "logo": {"@type": "ImageObject", "url": t.BASE_URL + "/assets/logo-square.png"}},
             "mainEntityOfPage": t.BASE_URL + f"/guide/{article['slug']}/"},
        ],
    }

    html = t.render_page(
        path=f"/guide/{article['slug']}/", title=page_title, meta_description=article["meta"],
        body_html=body, json_ld=json_ld,
    )
    write_page(f"/guide/{article['slug']}/", html)
    register(f"/guide/{article['slug']}/", "yearly", "0.5")


# ---------------------------------------------------------------------------
# Static pages
# ---------------------------------------------------------------------------

def build_confidentialite():
    title = "Politique de confidentialité | Webconvert.fr"
    meta = ("Vos images ne quittent jamais votre appareil : la conversion a lieu entièrement dans votre "
            "navigateur. Seule une mesure d'audience, soumise à votre accord, est utilisée.")
    body = f"""<main id="contenu" class="wrap page">
<article class="article doc">
  {t.breadcrumbs_nav([("Accueil", "/"), ("Confidentialité", None)])}
  <h1>Politique de confidentialité</h1>
  <p>Webconvert.fr est un outil de conversion d'images qui fonctionne entièrement dans votre navigateur. Vos images ne sont jamais collectées. La seule donnée recueillie est une mesure d'audience anonyme, et uniquement si vous l'acceptez.</p>

  <h2>Vos images</h2>
  <p>Les fichiers que vous déposez ne quittent jamais votre appareil. La conversion est réalisée localement via l'API Canvas de votre navigateur. Aucune image, miniature ou métadonnée n'est envoyée à un serveur, à Webconvert.fr ou à un tiers.</p>

  <h2>Formats nécessitant une librairie de décodage (HEIC, TIFF)</h2>
  <p>Les navigateurs ne savent pas lire nativement les fichiers HEIC et TIFF. Pour ces deux formats uniquement, une petite librairie technique (respectivement heic2any et UTIF.js, avec pako pour la décompression) est chargée depuis un CDN public (jsDelivr) au moment où vous déposez un fichier de ce type. Cette librairie est un simple script : elle s'exécute dans votre navigateur et ne transmet jamais vos fichiers à un serveur distant, y compris au fournisseur du CDN.</p>

  <h2 id="cookies">Cookies et mesure d'audience</h2>
  <p>Avec votre accord, le site utilise Google Analytics pour mesurer sa fréquentation : pages consultées, durée de visite, type d'appareil, pays approximatif. Ces statistiques servent uniquement à améliorer le site. Google Analytics dépose des cookies (<code>_ga</code>, <code>_ga_*</code>) et les données sont traitées par Google Ireland Limited, qui peut les transférer aux États-Unis dans le cadre du Data Privacy Framework.</p>
  <p>Tant que vous n'avez pas cliqué sur « Accepter », aucun script Google Analytics n'est chargé et aucun cookie n'est déposé. Votre choix est conservé 13 mois si vous acceptez, 6 mois si vous refusez, puis la question vous est reposée. Google Analytics ne reçoit jamais vos images : elles ne quittent pas votre appareil, que vous acceptiez ou non.</p>
  <p>Aucun cookie publicitaire ni pixel de suivi n'est utilisé.</p>
  <p><a href="#cookies" data-consent-open>Modifier mon choix concernant les cookies</a></p>

  <h2>Hébergement</h2>
  <p>Le site est constitué de fichiers statiques (HTML, CSS, JavaScript) servis tels quels par l'hébergeur. Seules les polices de caractères (Google Fonts) et trois librairies JavaScript ponctuelles — JSZip pour l'archive ZIP groupée, UTIF.js/pako pour le TIFF, heic2any pour le HEIC — sont chargées depuis un CDN public ; ce sont de simples fichiers de code, sans transmission de vos images.</p>

  <h2>Contact</h2>
  <p>Pour toute question, vous pouvez contacter l'éditeur du site via <a href="https://mathieu-perez.fr">mathieu-perez.fr</a>.</p>
</article>
</main>"""
    html = t.render_page(path="/confidentialite/", title=title, meta_description=meta, body_html=body,
                          robots="index, follow")
    write_page("/confidentialite/", html)
    register("/confidentialite/", "yearly", "0.2")


# ---------------------------------------------------------------------------
# Sitemap / robots / manifest / htaccess
# ---------------------------------------------------------------------------

def build_sitemap():
    entries = []
    for path, freq, prio in SITEMAP_URLS:
        entries.append(f"  <url>\n    <loc>{t.BASE_URL}{path}</loc>\n    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>\n  </url>")
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(entries) + "\n</urlset>\n"
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)


def build_robots():
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\n\nSitemap: https://webconvert.fr/sitemap.xml\n")


def build_manifest():
    import json
    manifest = {
        "name": "Webconvert.fr",
        "short_name": "Webconvert",
        "description": "Convertisseur d'images multi-formats, 100% local dans le navigateur.",
        "start_url": "/",
        "display": "standalone",
        "background_color": t.THEME_COLOR,
        "theme_color": t.THEME_COLOR,
        "lang": "fr",
        "icons": [
            {"src": "/assets/icons/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/assets/icons/android-chrome-512x512.png", "sizes": "512x512", "type": "image/png"},
        ],
    }
    with open(os.path.join(ROOT, "site.webmanifest"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


def build_htaccess():
    content = """# Cache static assets: HTML re-validates every visit, everything else is
# fingerprint-free but changes rarely, so a moderate cache is a fair trade-off.
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/html "access plus 0 seconds"
  ExpiresByType text/css "access plus 0 seconds"
  ExpiresByType application/javascript "access plus 0 seconds"
  ExpiresByType text/javascript "access plus 0 seconds"
  ExpiresByType image/jpeg "access plus 30 days"
  ExpiresByType image/png "access plus 30 days"
  ExpiresByType image/webp "access plus 30 days"
  ExpiresByType image/x-icon "access plus 30 days"
  ExpiresByType application/manifest+json "access plus 7 days"
</IfModule>

<IfModule mod_headers.c>
  # CSS/JS have no fingerprint in their URL: make browsers revalidate them
  # (cheap 304 via ETag) so a deploy never pairs new HTML with stale CSS/JS.
  <FilesMatch "\\.(css|js)$">
    Header set Cache-Control "public, no-cache"
  </FilesMatch>
  <FilesMatch "\\.(jpg|jpeg|png|webp|gif|ico|webmanifest)$">
    Header set Cache-Control "public, max-age=2592000"
  </FilesMatch>
  <FilesMatch "\\.html$">
    Header set Cache-Control "public, max-age=0, must-revalidate"
  </FilesMatch>
</IfModule>

<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript text/javascript application/manifest+json image/svg+xml
</IfModule>

# Clean URLs: /convertisseur-png/ etc are real directories with an index.html,
# resolved automatically by mod_dir. No rewrite rules needed.
"""
    with open(os.path.join(ROOT, ".htaccess"), "w", encoding="utf-8") as f:
        f.write(content)


def main():
    build_homepage()
    for input_id in INPUT_IDS:
        build_hub_page(input_id)
    for i, o in PAIRS:
        build_pair_page(i, o)
    build_guide_index()
    for article in ARTICLES:
        build_guide_article(article)
    build_confidentialite()

    build_sitemap()
    build_robots()
    build_manifest()
    build_htaccess()

    print(f"Generated {len(SITEMAP_URLS)} pages.")


if __name__ == "__main__":
    main()
