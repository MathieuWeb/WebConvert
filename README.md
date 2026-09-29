# Webconvert.fr

Convertisseur d'images multi-formats (JPG, PNG, WebP, AVIF, GIF, BMP, ICO, SVG, TIFF, HEIC), entièrement
dans le navigateur : aucun fichier n'est jamais envoyé à un serveur.

## Structure du projet

```
index.html, convertisseur-*/index.html, *-en-*/index.html   Pages générées (voir build/)
guide/index.html, guide/<slug>/index.html                    Articles générés (voir build/articles.py)
confidentialite/index.html                                   Page générée
sitemap.xml, robots.txt, site.webmanifest, .htaccess          Générés par build/generate.py
css/styles.css       Tout le CSS du site (custom properties --bg, --win, --ink, --muted, --line, --ok...)
js/
  formats-data.js     Registre des formats côté client (miroir de build/data.py::FORMATS)
  conversion.js       Décodage/encodage réel : Canvas API + UTIF.js (TIFF) + heic2any (HEIC) + encodeurs
                       BMP/ICO écrits à la main (aucun navigateur ne sait encoder ces deux formats nativement)
  ui.js               Dropzone, sélecteur de format de sortie, file d'attente, résultats, FAQ, picker homepage
  zip.js               Chargement paresseux de JSZip et génération du ZIP groupé
  consent.js           Bandeau de consentement cookies + chargement de Google Analytics après accord
  main.js               Point d'entrée
assets/               Favicons, og-image.jpg, logo-square.png (générés par build/gen_assets.py)
build/
  data.py              FORMATS (source de vérité), PAIR_OVERRIDES, HUB_OVERRIDES
  articles.py          Contenu des 7 guides
  templates.py         Rendu HTML (head, header/footer, tool, pickers, grids, FAQ...)
  generate.py           Orchestrateur : génère les 74 pages + sitemap/robots/manifest/.htaccess
  gen_assets.py          Génère favicons/og-image/logo (Pillow), à relancer seulement si la charte change
```

## Régénérer le site

Toute page HTML du site est générée, jamais éditée à la main. Après avoir modifié `build/data.py`,
`build/articles.py` ou `build/templates.py` :

```bash
cd build && python3 generate.py
```

Cela réécrit toutes les pages, `sitemap.xml`, `robots.txt`, `site.webmanifest` et `.htaccess` à la racine.

## Charte graphique (« Pierre »)

Fond minéral doux, titre centré, outil présenté comme une fenêtre d'application avec barre latérale.

| Rôle | Variable CSS | Valeur |
|---|---|---|
| Fond (pierre), `THEME_COLOR`, manifest | `--bg` | `#e7e4dd` |
| Fenêtre de l'outil, cartes, puces | `--win` | `#fbfaf8` |
| Barre latérale | `--side` | `#f2f0eb` |
| Texte, boutons sombres, logo | `--ink` | `#23221f` |
| Texte secondaire (contraste 5,4:1 sur le fond) | `--muted` | `#5d5a53` |
| Filets et bordures | `--line` | `#dcd8cf` |
| Gain de poids (barres, pourcentages) | `--ok` | `#2f6b3b` |

- **Police** : Figtree (Google Fonts), graisses 400/500/600/700/800. Titres en 800, interlettrage négatif.
- **Formes** : fenêtre en rayon 18 px, zone de dépôt et encadrés 14 px, champs et boutons 10 px, puces de
  format en pilule. Ombres quasi nulles (1 px), filets `--line` pour séparer.
- **Pages outil** (accueil, `/convertisseur-x/`, `/x-en-y/`) : bloc d'intro à hauteur fixe sur ordinateur
  (texte aligné en bas), puis la fenêtre : barre latérale (sélecteurs « De »/« Vers » = vrais `<select>`,
  qualité, mention de traitement local) et zone principale (dépôt, liste des fichiers rendue par
  `js/ui.js`, pied avec « Tout télécharger (ZIP) »). Le sélecteur et la zone de dépôt sont ainsi au même
  pixel sur toutes les pages outil. Sous 900 px, la barre latérale se replie au-dessus de la zone de dépôt.
- **Sections de contenu** : titre à gauche, contenu à droite, séparées par des filets (une seule colonne
  sur mobile). Pages texte (guides, confidentialité) : colonne de lecture de 720 px.
- **Logo** : carré sombre arrondi avec un carré au trait couleur pierre (CSS `.brand__mark`), repris par
  `build/gen_assets.py` pour les favicons, `logo-square.png` et `og-image.jpg`.
- À éviter (refusé lors du choix de la charte) : fonds quadrillés, halos, pastilles « badge », icônes dans
  des carrés teintés, rangées de trois cartes, métaphores thématiques, violet.

## Formats pris en charge

- **Entrée** (décodage) : JPG, PNG, WebP, AVIF, GIF, BMP, ICO, SVG, TIFF, HEIC.
- **Sortie** (encodage) : JPG, PNG, WebP, AVIF, BMP, ICO.
- GIF/SVG/TIFF/HEIC sont entrée uniquement : encoder un GIF animé ou un SVG vectoriel sans navigateur ni
  librairie lourde n'a pas de solution fiable ; ce sont des formats de destination trop spécifiques pour
  justifier une dépendance de plus.
- BMP et ICO sont encodés à la main dans `conversion.js` (`encodeBmp`/`encodeIco`) : aucun navigateur
  n'implémente `canvas.toBlob('image/bmp'|'image/x-icon')`.
- TIFF (via UTIF.js + pako) et HEIC (via heic2any) sont chargés depuis jsDelivr à la demande, uniquement
  quand un fichier de ce format est effectivement déposé — jamais au chargement de la page.

## Lancer le projet en local

Site 100% statique avec des URLs propres (`/convertisseur-png/`, `/png-en-webp/`...) servies comme des
répertoires contenant un `index.html` — un simple serveur de fichiers statique suffit :

```bash
python3 -m http.server 8000
```

## Ajouter un format ou une paire de conversion

1. Ajouter l'entrée dans `FORMATS` (`build/data.py`) **et** dans `js/formats-data.js` (les deux doivent
   rester synchronisés — le premier pilote la génération des pages, le second le comportement client).
2. Si le format nécessite un décodeur/encodeur spécifique, l'ajouter dans `js/conversion.js`.
3. Relancer `python3 build/generate.py` : les nouvelles pages `/convertisseur-x/` et `/x-en-y/` sont créées
   automatiquement pour toutes les combinaisons valides.
4. Pour un texte éditorial sur mesure plutôt que le gabarit générique, ajouter une entrée dans
   `PAIR_OVERRIDES` ou `HUB_OVERRIDES` (`build/data.py`).

## Déployer

Identique au projet frère (webpconvert.fr) : `git push`, puis côté hébergement, Git Version Control →
Pull or Deploy pour récupérer les derniers commits.

## Dépendances externes

- **JSZip** 3.10.1 — archive ZIP groupée, chargée au clic sur « Tout télécharger ».
- **UTIF.js** 3.1.0 + **pako** 2.1.0 — décodage TIFF, chargés au premier fichier `.tiff`/`.tif` déposé.
- **heic2any** 0.0.4 — décodage HEIC (libheif en WebAssembly), chargé au premier fichier `.heic`/`.heif`.
- **Google Fonts** — Figtree (400 à 800), seule police du site.

Toutes chargées depuis cdn.jsdelivr.net (ou fonts.googleapis.com), jamais appelées avec les images de
l'utilisateur : ce sont de simples fichiers de code. Aucun backend, aucune API.

## Mesure d'audience (Google Analytics)

- **Google Analytics 4** (`G-99CDZX4JZD`, constante `GA_ID` dans `build/templates.py`) : chargé par
  `js/consent.js` **uniquement après clic sur « Accepter »** dans le bandeau de consentement (conformité
  CNIL). Choix conservé 13 mois (accepté) / 6 mois (refusé) dans `localStorage`, modifiable via le lien
  « Gérer les cookies » du pied de page. Mettre `GA_ID = ""` pour retirer entièrement la mesure d'audience.
- **Google Search Console** : propriété de type Domaine, validée par un enregistrement DNS TXT (aucune
  balise dans le code).
