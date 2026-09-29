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

from data import (FORMATS, INPUT_IDS, OUTPUT_IDS, PAIRS, FEATURED_PAIRS, TARGET_SIZES, TARGET_USES, DEMARCHES,
                  get_pair_copy, get_hub_copy)
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

def compress_teaser_html():
    chips = "\n".join(f'      <a class="chip" href="/compresser-image-{slug}/">{text}</a>'
                      for slug, _b, text in TARGET_SIZES)
    return f"""    <div class="catalog__group">
      <p class="catalog__label">Par poids maximum</p>
      <div class="chips">
{chips}
      </div>
    </div>
    <div class="catalog__group">
      <p class="catalog__label">Par démarche</p>
{t.link_list_html(demarche_links())}
    </div>"""


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
{t.section_html("compresser", "Compresser à une taille précise", compress_teaser_html(),
                intro="Un site exige moins de 1 Mo ou de 200 Ko ? Choisissez la limite, l'outil trouve la meilleure qualité qui tient dessous.")}
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
# Compression to a target weight: /compresser-image/, /compresser-image-{seuil}/,
# /compresser-photo-{démarche}/
# ---------------------------------------------------------------------------

COMPRESS_HUB = "/compresser-image/"


def threshold_links(exclude=None):
    return [(f"Moins de {text}", TARGET_USES[slug].capitalize() + ".", f"/compresser-image-{slug}/")
            for slug, _b, text in TARGET_SIZES if slug != exclude]


def demarche_links(exclude=None):
    return [(d["crumb"], d["intro"].split(".")[0] + ".", d["path"])
            for key, d in DEMARCHES.items() if key != exclude]


def compress_how_html(limit_text):
    return f"""    <div class="prose">
      <p>Pour chaque image, l'outil cherche la meilleure qualité d'encodage dont le résultat pèse moins de {limit_text} : il essaie plusieurs réglages et garde le plus élevé qui respecte la limite. Vous n'avez rien à régler à la main.</p>
      <p>Si même une qualité basse ne suffit pas (photo très grande, ou format sans perte comme le PNG), l'image est réduite en dimensions, par petites étapes, jusqu'à passer sous la limite. Le détail est affiché pour chaque fichier : qualité retenue et, le cas échéant, nouvelles dimensions.</p>
      <p>Une image déjà assez légère et déjà au bon format est rendue telle quelle, sans perte. Tout se passe dans votre navigateur : vos fichiers ne sont envoyés sur aucun serveur.</p>
    </div>"""


def compress_faq(limit_text):
    return [
        (f"Comment réduire une photo à moins de {limit_text} ?",
         f"Déposez-la dans l'outil ci-dessus avec la limite « {limit_text} » : elle est recompressée automatiquement "
         "avec la meilleure qualité possible sous cette limite, puis vous la téléchargez."),
        ("La qualité de l'image va-t-elle baisser ?",
         "Le moins possible : la qualité n'est abaissée que jusqu'au point nécessaire, et les dimensions ne sont "
         "réduites que si la qualité seule ne suffit pas. Le détail est indiqué pour chaque fichier."),
        ("Quelle différence entre Ko et Mo ?",
         "1 Mo vaut 1 000 Ko. L'outil compte 1 Ko = 1 000 octets, ce qui garantit aussi le respect des sites qui "
         "comptent 1 Ko = 1 024 octets."),
    ] + list(t.PRIVACY_FAQ[:1])


def build_compress_page(*, path, crumbs, h1, subtitle, title, meta, target, output, sections, faq_items,
                        app_name, priority):
    body = f"""<main id="contenu">
{t.intro_html(crumbs=crumbs, h1=h1, subtitle=subtitle)}
{t.tool_markup(input_id="any", default_output=output, target=target)}

{sections}
{t.privacy_aside_html()}
{t.faq_html(faq_items)}
</main>"""
    crumb_ld = [(c, h if h else path) for c, h in crumbs]
    json_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "BreadcrumbList", "itemListElement": t.breadcrumb_json_ld(crumb_ld)},
            {"@type": "WebApplication", "@id": BASE_ID(path.strip("/") + "/#app"), "name": app_name,
             "url": t.BASE_URL + path, "applicationCategory": "MultimediaApplication",
             "operatingSystem": "Tout navigateur web", "browserRequirements": "Navigateur compatible HTML5 Canvas",
             "inLanguage": "fr-FR", "description": meta,
             "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}},
            t.faq_json_ld(faq_items),
        ],
    }
    html = t.render_page(
        path=path, title=title + " | Webconvert.fr", meta_description=meta, body_html=body, json_ld=json_ld,
        include_js=True,
        wc_config={"input": "any", "output": output, "target": target,
                   "zipName": path.strip("/") + ".zip"},
    )
    write_page(path, html)
    register(path, "monthly", priority)


def build_compress_hub():
    sections = (
        t.section_html("seuils", "Choisir une limite de poids", t.link_list_html(threshold_links()),
                       intro="Une page par limite courante, avec le bon réglage déjà sélectionné.")
        + "\n"
        + t.section_html("demarches", "Pour une démarche précise", t.link_list_html(demarche_links()),
                         intro="La limite exigée par le site de destination, déjà réglée.")
        + "\n"
        + t.section_html("comment-compresser", "Comment fonctionne la compression", compress_how_html("la limite choisie"),
                         tag="article")
    )
    build_compress_page(
        path=COMPRESS_HUB,
        crumbs=[("Accueil", "/"), ("Compresser une image", None)],
        h1="Compresser une image à une taille précise",
        subtitle="Choisissez un poids maximum : chaque image est compressée avec la meilleure qualité qui tient dessous. Rien n'est envoyé sur un serveur.",
        title="Compresser une image à une taille précise (Ko ou Mo), gratuit",
        meta=("Réduisez le poids de vos images sous une limite précise (50 Ko, 200 Ko, 1 Mo, 2 Mo…) avec la "
              "meilleure qualité possible. Gratuit, par lot, 100% dans votre navigateur."),
        target=1_000_000, output="jpg", sections=sections,
        faq_items=compress_faq("la limite choisie"),
        app_name="Compresseur d'images à taille cible", priority="0.9",
    )


def build_threshold_page(slug, target, text):
    uses = TARGET_USES[slug]
    sections = (
        t.section_html("comment-compresser", f"Réduire une image à moins de {text}", compress_how_html(text),
                       tag="article")
        + "\n"
        + t.section_html("seuils", "Autres limites", t.link_list_html(threshold_links(exclude=slug)))
        + "\n"
        + t.section_html("demarches", "Pour une démarche précise", t.link_list_html(demarche_links()))
    )
    build_compress_page(
        path=f"/compresser-image-{slug}/",
        crumbs=[("Accueil", "/"), ("Compresser une image", COMPRESS_HUB), (f"Moins de {text}", None)],
        h1=f"Compresser une image à moins de {text}",
        subtitle=f"Pour {uses}. Meilleure qualité possible sous {text}, sans envoi sur un serveur.",
        title=f"Compresser une image à moins de {text} (JPG, PNG, WebP)",
        meta=(f"Réduisez une photo ou une image à moins de {text} en quelques secondes, avec la meilleure qualité "
              f"possible. Gratuit, par lot, sans envoyer vos fichiers sur un serveur."),
        target=target, output="jpg", sections=sections, faq_items=compress_faq(text),
        app_name=f"Compresser une image à moins de {text}", priority="0.8",
    )


def build_demarche_page(key):
    d = DEMARCHES[key]
    limit_text = next(text for _s, b, text in TARGET_SIZES if b == d["target"])
    paragraphs = "".join(f"<p>{p}</p>" for p in d["paragraphs"])
    sections = (
        t.section_html("demarche", "Ce qu'il faut savoir", f'    <div class="prose">{paragraphs}</div>',
                       tag="article")
        + "\n"
        + t.section_html("comment-compresser", "Comment fonctionne la compression", compress_how_html(limit_text),
                         tag="article")
        + "\n"
        + t.section_html("demarches", "Autres démarches", t.link_list_html(demarche_links(exclude=key)))
        + "\n"
        + t.section_html("seuils", "Toutes les limites", t.link_list_html(threshold_links()))
    )
    build_compress_page(
        path=d["path"],
        crumbs=[("Accueil", "/"), ("Compresser une image", COMPRESS_HUB), (d["crumb"], None)],
        h1=d["h1"], subtitle=d["intro"], title=d["title"], meta=d["meta"],
        target=d["target"], output=d["output"], sections=sections,
        faq_items=list(d["faq"]), app_name=d["title"], priority="0.8",
    )


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
    build_compress_hub()
    for slug, target, text in TARGET_SIZES:
        build_threshold_page(slug, target, text)
    for key in DEMARCHES:
        build_demarche_page(key)
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
