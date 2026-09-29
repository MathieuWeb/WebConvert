# -*- coding: utf-8 -*-
"""Canonical format registry and hand-written per-pair/per-format editorial
content for Webconvert.fr. This is the single source of truth for every
generated page; keep js/formats-data.js in sync with the id/label/ext/mime
fields when a format is added or changed.
"""

# Insertion order == display order everywhere (dropdowns, pill lists, grids).
FORMATS = {
    "jpg": dict(
        id="jpg", label="JPG", exts=["jpg", "jpeg"], mime="image/jpeg",
        canDecode=True, canEncode=True, lossy=True, alpha=False,
        short="photographies et images avec dégradés",
        what_it_is="Le JPEG (JPG) est un format d'image avec perte apparu en 1992, pensé pour la photographie. "
                    "Il compresse en s'appuyant sur les limites de la perception humaine des couleurs, au prix "
                    "d'artefacts visibles si la compression est poussée trop loin.",
        strengths=["Compatible avec absolument tous les logiciels et appareils, sans exception",
                   "Fichiers légers sur les photographies",
                   "Réglage de qualité fin, du très compressé au quasi sans perte"],
        weaknesses=["Pas de transparence (aucun canal alpha)",
                    "Perd en qualité à chaque réencodage successif",
                    "Moins efficace que le WebP ou l'AVIF à qualité visuelle égale"],
        common_uses=["Photographies", "Visuels e-commerce", "Pièces jointes email"],
        best_for="les photographies destinées à être lues partout, sans aucune exception",
        output_benefit="un fichier compatible avec absolument tous les logiciels, y compris les plus anciens",
    ),
    "png": dict(
        id="png", label="PNG", exts=["png"], mime="image/png",
        canDecode=True, canEncode=True, lossy=False, alpha=True,
        short="logos, captures d'écran et images avec transparence",
        what_it_is="Le PNG est un format sans perte apparu en 1996 pour remplacer le GIF. Il conserve chaque "
                    "pixel à l'identique et gère la transparence grâce à un canal alpha sur 8 bits.",
        strengths=["Aucune perte de qualité, aucun artefact de compression",
                   "Transparence complète (canal alpha), pas seulement un pixel transparent/opaque",
                   "Idéal sur les aplats de couleurs nettes : logos, texte, interfaces"],
        weaknesses=["Fichiers volumineux sur les photographies",
                     "Pas d'animation, contrairement au GIF ou au WebP"],
        common_uses=["Logos", "Captures d'écran", "Icônes et illustrations avec transparence"],
        best_for="tout ce qui doit rester net au pixel près : logos, texte, interfaces",
        output_benefit="un fichier sans perte avec transparence, parfait pour la retouche ou l'intégration à une interface",
    ),
    "webp": dict(
        id="webp", label="WebP", exts=["webp"], mime="image/webp",
        canDecode=True, canEncode=True, lossy=True, alpha=True,
        short="images de sites web optimisées",
        what_it_is="Le WebP est un format développé par Google en 2010, disponible en mode avec perte (basé "
                    "sur le codec vidéo VP8) et en mode sans perte. Il gère la transparence et l'animation "
                    "dans un seul et même format.",
        strengths=["25 à 35% plus léger qu'un JPEG à qualité perçue équivalente",
                   "Transparence et animation supportées nativement",
                   "Pris en charge par tous les navigateurs modernes depuis 2020, Safari compris"],
        weaknesses=["Compatibilité plus limitée hors navigateur (certains logiciels desktop anciens)",
                     "Moins universel que le JPG pour l'impression"],
        common_uses=["Images de sites web", "Fiches produit e-commerce", "Optimisation des Core Web Vitals"],
        best_for="le web moderne : sites, boutiques en ligne, applications",
        output_benefit="un fichier nettement plus léger tout en restant net, pensé pour le web actuel",
    ),
    "avif": dict(
        id="avif", label="AVIF", exts=["avif"], mime="image/avif",
        canDecode=True, canEncode=True, lossy=True, alpha=True,
        short="images ultra-compressées pour le web",
        what_it_is="L'AVIF dérive du codec vidéo AV1 et a été standardisé en 2019. C'est aujourd'hui le format "
                    "le plus efficace en compression grand public, avec ou sans perte, transparence incluse.",
        strengths=["Souvent 30 à 50% plus léger qu'un WebP à qualité équivalente",
                   "Excellente gestion des dégradés et de la transparence",
                   "Supporté par les versions récentes de Chrome, Firefox et Safari"],
        weaknesses=["Encodage plus lent que le WebP ou le JPEG",
                     "Support encore partiel sur certains navigateurs et logiciels plus anciens"],
        common_uses=["Sites à fort trafic cherchant à réduire la bande passante", "Applications mobiles"],
        best_for="minimiser au maximum le poids des images quand la compatibilité totale n'est pas requise",
        output_benefit="le fichier le plus léger possible à qualité visuelle égale, la référence actuelle en compression",
    ),
    "gif": dict(
        id="gif", label="GIF", exts=["gif"], mime="image/gif",
        canDecode=True, canEncode=False, lossy=False, alpha=False,
        short="animations courtes et images à palette réduite",
        what_it_is="Le GIF, créé en 1987, utilise une palette limitée à 256 couleurs et une compression sans "
                    "perte LZW. Il reste surtout connu pour son support natif de l'animation.",
        strengths=["Animation supportée nativement", "Compatibilité universelle, y compris les logiciels anciens"],
        weaknesses=["256 couleurs maximum : dégradés et photos rendus avec du bruit visible",
                     "Très lourd comparé au WebP ou à une vidéo pour de l'animation",
                     "Pas de transparence partielle (un pixel est 100% transparent ou 100% opaque)"],
        common_uses=["Animations courtes", "Réactions et mèmes"],
        best_for="l'animation simple quand aucune autre option n'est disponible",
        decode_note="Les GIF animés sont convertis à partir de leur toute première image : l'encodeur du "
                    "navigateur ne sait produire qu'une image fixe, il n'existe pas d'équivalent « GIF animé "
                    "vers WebP animé » côté client sans librairie tierce lourde.",
    ),
    "bmp": dict(
        id="bmp", label="BMP", exts=["bmp"], mime="image/bmp",
        canDecode=True, canEncode=True, lossy=False, alpha=False,
        short="images matricielles non compressées",
        what_it_is="Le Bitmap (BMP) est un format d'image matricielle sans compression, ou très peu compressée, "
                    "introduit par Microsoft avec Windows. Chaque pixel est stocké quasiment tel quel.",
        strengths=["Structure très simple, lue instantanément par n'importe quel logiciel Windows",
                   "Aucune perte, aucun artefact de compression"],
        weaknesses=["Fichiers nettement plus lourds qu'un PNG à qualité égale", "Quasiment jamais utilisé pour le web"],
        common_uses=["Logiciels Windows historiques", "Traitement d'image bas niveau", "Certains flux d'impression"],
        best_for="les logiciels ou périphériques qui exigent explicitement ce format",
        output_benefit="un fichier brut sans compression, lisible par les logiciels qui l'exigent explicitement",
    ),
    "ico": dict(
        id="ico", label="ICO", exts=["ico"], mime="image/x-icon",
        canDecode=True, canEncode=True, lossy=False, alpha=True,
        short="favicons et icônes d'application",
        what_it_is="Le format ICO stocke une ou plusieurs tailles d'une même icône dans un seul fichier. Il est "
                    "utilisé pour les favicons de site web et les icônes d'applications Windows.",
        strengths=["Format attendu par tous les navigateurs pour favicon.ico", "Peut contenir plusieurs résolutions dans un seul fichier"],
        weaknesses=["Ne convient pas aux photographies", "Peu utile en dehors de son usage favicon/icône"],
        common_uses=["Favicons de site web", "Icônes d'exécutables Windows"],
        best_for="générer une favicon prête à l'emploi à partir d'un logo carré",
        output_benefit="une icône prête à l'emploi comme favicon de site ou icône d'application",
        encode_note="L'image est réduite à 256 px de large maximum, la taille standard des favicons et icônes.",
    ),
    "svg": dict(
        id="svg", label="SVG", exts=["svg"], mime="image/svg+xml",
        canDecode=True, canEncode=False, lossy=False, alpha=True,
        short="logos et icônes vectoriels",
        what_it_is="Le SVG est un format vectoriel basé sur XML : au lieu de pixels, il décrit des formes "
                    "géométriques. Il reste net à n'importe quelle taille d'affichage.",
        strengths=["Netteté parfaite à toute résolution, écrans très haute densité compris",
                   "Fichiers très légers pour les logos et icônes simples",
                   "Modifiable comme du texte (couleurs, formes, tracés)"],
        weaknesses=["Ne convient pas aux photographies", "Doit être rasterisé (converti en pixels) pour de nombreux usages"],
        common_uses=["Logos", "Icônes d'interface", "Illustrations plates"],
        best_for="les logos et icônes qui doivent rester nets à toutes les tailles",
        decode_note="La conversion rasterise le SVG à la taille définie par ses attributs width/height ou son "
                    "viewBox ; un SVG sans dimension explicite est rasterisé à une taille par défaut de 300×150.",
    ),
    "tiff": dict(
        id="tiff", label="TIFF", exts=["tiff", "tif"], mime="image/tiff",
        canDecode=True, canEncode=False, lossy=False, alpha=False,
        short="images professionnelles et scans",
        what_it_is="Le TIFF (Tagged Image File Format) est un format professionnel sans perte utilisé en "
                    "photographie, impression et numérisation, capable de stocker des calques et des métadonnées étendues.",
        strengths=["Fidélité maximale, aucune perte", "Standard historique de l'imprimerie et de la photo professionnelle"],
        weaknesses=["Fichiers très volumineux", "Illisible nativement dans un navigateur ou sur le web"],
        common_uses=["Photographie professionnelle retouchée", "Numérisation de documents", "Prépresse et impression"],
        best_for="l'archivage et l'impression professionnelle, pas pour la publication web",
        decode_note="Les TIFF non compressés, LZW et Deflate/ZIP sont pris en charge par le décodeur embarqué ; "
                    "les variantes de compression très spécifiques (JPEG dans TIFF, CCITT) peuvent échouer.",
    ),
    "heic": dict(
        id="heic", label="HEIC", exts=["heic", "heif"], mime="image/heic",
        canDecode=True, canEncode=False, lossy=True, alpha=False,
        short="photos iPhone et iPad",
        what_it_is="Le HEIC (High Efficiency Image Container) est le format utilisé par défaut par les iPhone "
                    "depuis iOS 11. Basé sur la même compression que le codec vidéo HEVC, il produit des "
                    "fichiers environ deux fois plus légers qu'un JPEG à qualité équivalente.",
        strengths=["Très bonne compression, qualité proche du JPEG pour environ moitié moins de poids",
                   "Standard par défaut sur iPhone et iPad récents"],
        weaknesses=["Très mal supporté hors de l'écosystème Apple",
                     "Illisible nativement sur Windows, Android et la quasi-totalité des sites web"],
        common_uses=["Photos prises directement avec un iPhone ou un iPad"],
        best_for="rester dans l'écosystème Apple ; à convertir dès qu'il faut partager ou publier ailleurs",
        decode_note="Le décodage passe par une librairie dédiée (libheif, compilée en WebAssembly) chargée à la "
                    "demande depuis un CDN public : le code s'exécute dans votre navigateur, vos photos ne sont "
                    "jamais transmises à ce service, seul le script lui-même est téléchargé.",
    ),
}

INPUT_IDS = [f["id"] for f in FORMATS.values() if f["canDecode"]]
OUTPUT_IDS = [f["id"] for f in FORMATS.values() if f["canEncode"]]
PAIRS = [(i, o) for i in INPUT_IDS for o in OUTPUT_IDS if i != o]

# Popular pairs surfaced first in cross-link grids / homepage.
FEATURED_PAIRS = [
    ("png", "webp"), ("jpg", "webp"), ("webp", "png"), ("webp", "jpg"),
    ("heic", "jpg"), ("heic", "png"), ("png", "jpg"), ("jpg", "png"),
    ("gif", "webp"), ("svg", "png"), ("avif", "jpg"), ("png", "ico"),
]

# ---------------------------------------------------------------------------
# Hand-written copy for the highest-intent pairs. Anything not listed here
# falls back to the generic template in templates.py, assembled from the
# FORMATS facts above (see build_generic_pair_copy).
# ---------------------------------------------------------------------------
PAIR_OVERRIDES = {
    ("png", "webp"): dict(
        title="Convertir PNG en WebP sans perdre la transparence",
        meta="Convertissez vos PNG en WebP en conservant le canal alpha. Idéal pour logos, icônes et captures "
             "d'écran. 100% dans le navigateur, sans upload.",
        intro="Logos, icônes et captures d'écran gardent leur canal alpha intact, pour un fichier nettement plus léger.",
        paragraphs=[
            "Le PNG compresse sans perte, ce qui le rend parfait pour les logos et les captures d'écran, mais "
            "aussi plus lourd qu'il ne devrait l'être. Le WebP propose un mode avec pertes bien plus efficace "
            "sur les images contenant des dégradés ou des photos, tout en gérant nativement la transparence "
            "comme le PNG.",
            "Résultat : vous gardez le canal alpha (les bords transparents d'un logo, une capture d'écran "
            "détourée) mais avec un fichier généralement plus léger, surtout si l'image contient autre chose "
            "que des aplats de couleur unis.",
        ],
        faq=[
            ("La transparence est-elle vraiment conservée ?", "Oui. Le canal alpha du PNG est préservé tout du "
             "long : le canvas qui sert à l'encodage garde la transparence, et le format WebP la gère nativement."),
            ("Le WebP est-il plus léger qu'un PNG pour un logo ?", "Presque toujours, mais l'écart est plus "
             "faible que sur une photo : un PNG de logo en aplats de couleur est déjà bien compressé nativement. "
             "Pour éviter tout artefact sur les aplats, réglez le curseur de qualité proche de 100."),
        ],
    ),
    ("jpg", "webp"): dict(
        title="Convertir JPG en WebP gratuitement et en ligne",
        meta="Convertissez vos JPG en WebP en un clic, 25 à 35% de poids en moins. Traitement 100% dans le "
             "navigateur, sans upload ni compte.",
        intro="Vos photos JPEG deviennent des fichiers nettement plus légers, sans perte de qualité visible.",
        paragraphs=[
            "Le JPEG reste le format le plus universel pour la photographie, mais il a plus de trente ans : le "
            "WebP applique une compression plus moderne et gagne en moyenne 25 à 35% de poids à qualité perçue "
            "équivalente.",
            "Pour un site web, ce gain se traduit directement en temps de chargement plus court et de meilleurs "
            "scores Core Web Vitals, sans que vos visiteurs remarquent la différence visuelle.",
        ],
        faq=[
            ("Vais-je perdre en qualité ?", "À réglage équivalent, la différence est imperceptible à l'œil nu. "
             "Le curseur de qualité vous laisse arbitrer entre poids et fidélité selon votre usage."),
            ("Puis-je convertir plusieurs JPG en même temps ?", "Oui, déposez-en autant que vous voulez : ils "
             "sont convertis en lot puis téléchargeables un par un ou groupés dans une archive ZIP."),
        ],
    ),
    ("webp", "png"): dict(
        title="Convertir WebP en PNG (transparence conservée)",
        meta="Reconvertissez vos WebP en PNG classique, transparence conservée, pour les logiciels qui ne "
             "lisent pas encore le WebP. 100% local, sans upload.",
        intro="Repassez en PNG universel quand un logiciel ou un usage n'accepte pas encore le WebP.",
        paragraphs=[
            "Le WebP n'est pas encore lu par tous les logiciels de retouche, CMS ou outils d'impression. Cette "
            "page reconvertit vos fichiers WebP en PNG, un format sans perte reconnu absolument partout.",
            "La transparence éventuelle du WebP source est préservée : un badge ou un logo WebP transparent "
            "redevient un PNG transparent, prêt à être réutilisé dans n'importe quel outil.",
        ],
        faq=[
            ("Pourquoi reconvertir en PNG plutôt qu'en JPG ?", "Le PNG conserve la transparence et n'introduit "
             "aucune perte supplémentaire, contrairement au JPG qui n'a pas de canal alpha et recompresse l'image."),
            ("Le fichier sera-t-il plus lourd qu'en WebP ?", "Oui, c'est attendu : le PNG sans perte pèse "
             "généralement plus qu'un WebP. C'est le compromis à faire pour la compatibilité logicielle."),
        ],
    ),
    ("webp", "jpg"): dict(
        title="Convertir WebP en JPG pour la compatibilité maximale",
        meta="Convertissez vos WebP en JPG pour les logiciels, imprimantes ou plateformes qui n'acceptent que "
             "ce format. 100% dans le navigateur.",
        intro="Pour les logiciels, imprimantes ou plateformes qui ne lisent pas encore le WebP.",
        paragraphs=[
            "Certains outils de retouche, imprimeurs en ligne ou anciennes plateformes n'acceptent encore que "
            "le JPEG. Cette page reconvertit vos WebP en JPG classique, compatible avec absolument tout.",
            "Une éventuelle transparence du WebP source est aplatie sur un fond blanc, comme s'y attend tout "
            "logiciel qui traite le JPEG comme un format opaque.",
        ],
        faq=[
            ("Que devient la transparence ?", "Le JPEG ne gère pas la transparence : les zones transparentes "
             "du WebP source sont remplies en blanc à la conversion."),
            ("Est-ce réversible ?", "Le fichier d'origine n'est jamais modifié : seul un nouveau fichier JPG "
             "est créé à côté, vous gardez votre WebP source intact."),
        ],
    ),
    ("heic", "jpg"): dict(
        title="Convertir une photo HEIC d'iPhone en JPG",
        meta="Convertissez vos photos HEIC (iPhone, iPad) en JPG lisible partout : Windows, Android, email, "
             "réseaux sociaux. 100% dans le navigateur.",
        intro="Vos photos iPhone deviennent lisibles sur Windows, Android et n'importe quel site web.",
        paragraphs=[
            "Depuis iOS 11, l'iPhone enregistre ses photos en HEIC par défaut : un format efficace, mais mal "
            "reconnu en dehors de l'écosystème Apple. Beaucoup de sites, de logiciels Windows ou d'appareils "
            "Android refusent purement et simplement ces fichiers.",
            "Cette page les convertit en JPG, le format le plus universel qui existe, lisible sans exception "
            "sur n'importe quel appareil, logiciel ou plateforme en ligne.",
        ],
        faq=[
            ("Mes photos passent-elles par un serveur Apple ou externe ?", "Non. Le décodage HEIC s'appuie sur "
             "une librairie technique (libheif) chargée une fois dans votre navigateur, mais vos photos "
             "elles-mêmes ne quittent jamais votre appareil."),
            ("Pourquoi mon iPhone enregistre-t-il en HEIC ?", "Ce format compresse environ deux fois mieux qu'un "
             "JPEG classique à qualité équivalente, ce qui économise de l'espace de stockage sur l'appareil."),
        ],
    ),
    ("heic", "png"): dict(
        title="Convertir une photo HEIC en PNG sans perte",
        meta="Convertissez vos HEIC (iPhone) en PNG sans perte de qualité, pour la retouche ou l'archivage. "
             "100% dans le navigateur, sans upload.",
        intro="Pour retoucher ou archiver vos photos iPhone dans un format sans perte et universel.",
        paragraphs=[
            "Le PNG est le choix logique quand une photo HEIC doit être retouchée ou archivée sans perte "
            "supplémentaire : contrairement au JPG, aucune recompression n'est appliquée lors de la conversion.",
            "Le fichier obtenu est plus lourd qu'un JPG équivalent, mais garantit qu'aucun détail n'est perdu "
            "par rapport à la photo HEIC d'origine.",
        ],
        faq=[
            ("Quelle différence avec une conversion en JPG ?", "Le PNG n'introduit aucune perte de qualité "
             "supplémentaire, alors que le JPG recompresse l'image. Le PNG est préférable pour la retouche, le "
             "JPG pour le partage et le poids du fichier."),
            ("Mes photos sont-elles envoyées quelque part ?", "Non, tout se déroule dans votre navigateur, y "
             "compris le décodage du fichier HEIC."),
        ],
    ),
    ("gif", "webp"): dict(
        title="Convertir un GIF en WebP",
        meta="Convertissez un GIF en image WebP statique, bien plus légère. 100% dans le navigateur, sans upload.",
        intro="Une image GIF fixe devient un WebP nettement plus léger, en conservant les couleurs.",
        paragraphs=[
            "Le GIF limite chaque image à 256 couleurs, ce qui pèse lourd et rend mal les dégradés. Le WebP "
            "n'a pas cette limite et compresse généralement bien mieux, même en gardant une transparence.",
            "Cette conversion aplatit le GIF à sa première image : un GIF animé produira un WebP statique de sa "
            "toute première frame, le Canvas du navigateur ne sachant pas ré-encoder une animation.",
        ],
        faq=[
            ("Mon GIF est animé, que se passe-t-il ?", "Seule la première image de l'animation est convertie. "
             "Encoder un WebP animé nécessite une librairie dédiée que ce convertisseur, volontairement léger, "
             "n'embarque pas."),
            ("La transparence du GIF est-elle conservée ?", "Oui, les zones transparentes du GIF sont préservées "
             "dans le WebP obtenu."),
        ],
    ),
    ("svg", "png"): dict(
        title="Convertir un SVG en PNG (rasterisation)",
        meta="Convertissez vos SVG en PNG, avec transparence conservée, pour les usages qui n'acceptent pas le "
             "vectoriel. 100% dans le navigateur.",
        intro="Transformez un logo ou une icône vectorielle en image PNG classique, transparence comprise.",
        paragraphs=[
            "De nombreux outils (réseaux sociaux, certains CMS, logiciels de présentation) n'acceptent pas le "
            "SVG et demandent une image matricielle classique. Cette page rasterise votre SVG en PNG, en "
            "conservant la transparence du fond.",
            "La taille de sortie dépend des attributs width/height ou du viewBox définis dans le fichier SVG : "
            "pour une image plus grande et plus nette, ouvrez le SVG dans un éditeur et augmentez ces valeurs "
            "avant de le convertir.",
        ],
        faq=[
            ("Le résultat est-il flou en haute résolution ?", "Non : la rasterisation part directement des "
             "tracés vectoriels, le PNG obtenu est net à la taille définie par le fichier SVG."),
            ("Puis-je obtenir une image plus grande ?", "Modifiez les attributs width et height (ou le "
             "viewBox) de votre fichier SVG avant de le déposer : la conversion se cale sur ces dimensions."),
        ],
    ),
    ("avif", "jpg"): dict(
        title="Convertir AVIF en JPG pour la compatibilité",
        meta="Convertissez vos AVIF en JPG pour les logiciels ou plateformes qui ne lisent pas encore ce "
             "format récent. 100% dans le navigateur.",
        intro="Pour les logiciels ou usages qui ne prennent pas encore en charge l'AVIF.",
        paragraphs=[
            "L'AVIF est très efficace mais encore jeune : certains logiciels de retouche, imprimeurs en ligne "
            "ou plateformes ne le reconnaissent pas encore. Cette page reconvertit vos AVIF en JPG, universellement lisible.",
            "Le fichier obtenu sera plus lourd que l'AVIF d'origine : c'est le prix de la compatibilité maximale.",
        ],
        faq=[
            ("Pourquoi mon fichier AVIF ne s'ouvre-t-il pas partout ?", "L'AVIF est récent (2019) : sa prise en "
             "charge est excellente dans les navigateurs modernes mais encore incomplète dans certains logiciels "
             "de bureau ou anciens systèmes."),
            ("Puis-je reconvertir plus tard en AVIF ?", "Oui, votre fichier AVIF d'origine n'est jamais modifié, "
             "vous pouvez le reconvertir à tout moment."),
        ],
    ),
    ("png", "ico"): dict(
        title="Créer une favicon .ico à partir d'un PNG",
        meta="Transformez votre logo PNG en fichier favicon.ico prêt à l'emploi pour votre site web. 100% dans "
             "le navigateur, sans upload.",
        intro="Générez un favicon.ico prêt à déposer à la racine de votre site, à partir de votre logo PNG.",
        paragraphs=[
            "Un favicon.ico reste le format le plus universellement reconnu par les navigateurs pour l'icône "
            "d'un site, affichée dans l'onglet et les favoris. Cette page transforme votre logo PNG en ICO "
            "directement utilisable.",
            "Pour un résultat net, partez d'un PNG carré (par exemple 512×512) : l'image est automatiquement "
            "réduite à 256 px maximum, la taille standard des favicons.",
        ],
        faq=[
            ("Mon logo n'est pas carré, est-ce grave ?", "Non, mais le rendu sera plus propre avec un visuel "
             "carré : sur un format rectangulaire, le favicon peut paraître écrasé dans l'onglet du navigateur."),
            ("Où placer le fichier obtenu ?", "Déposez-le à la racine de votre site sous le nom favicon.ico, "
             "ou référencez-le via une balise « link rel=icon » placée dans l’en-tête (head) de vos pages."),
        ],
    ),
    ("png", "jpg"): dict(
        title="Convertir PNG en JPG",
        meta="Convertissez vos PNG en JPG, fond blanc automatique pour la transparence. 100% dans le navigateur, sans upload.",
        intro="Pour réduire le poids d'un PNG ou répondre à un usage qui exige explicitement du JPEG.",
        paragraphs=[
            "Un PNG contenant une photographie ou un dégradé complexe pèse souvent plus lourd qu'il ne devrait : "
            "le JPEG, conçu pour ce type de contenu, réduit nettement la taille du fichier.",
            "Le JPEG n'ayant pas de canal alpha, toute zone transparente de votre PNG est automatiquement "
            "remplie en blanc avant l'encodage.",
        ],
        faq=[
            ("Que devient la transparence ?", "Les zones transparentes sont remplies en blanc, le JPEG ne "
             "pouvant pas encoder de canal alpha."),
            ("Dans quel cas garder le PNG plutôt que convertir ?", "Si l'image est un logo en aplats de "
             "couleurs ou nécessite la transparence, gardez le PNG : le gain de poids en JPEG y est minime."),
        ],
    ),
    ("jpg", "png"): dict(
        title="Convertir JPG en PNG sans perte",
        meta="Convertissez vos JPG en PNG sans perte supplémentaire, pour la retouche ou l'ajout de transparence. 100% local.",
        intro="Pour retoucher une photo sans accumuler de nouvelles pertes de compression.",
        paragraphs=[
            "Convertir un JPG en PNG n'améliore pas la qualité d'origine (les artefacts JPEG déjà présents "
            "restent visibles), mais garantit qu'aucune perte supplémentaire ne sera ajoutée lors des "
            "prochaines étapes de retouche.",
            "C'est aussi le point de passage utile si vous devez ensuite détourer l'image et lui ajouter de "
            "la transparence dans un logiciel de retouche.",
        ],
        faq=[
            ("Le PNG obtenu sera-t-il de meilleure qualité que le JPG ?", "Non : la qualité déjà perdue par la "
             "compression JPEG d'origine ne peut pas être récupérée. Le PNG évite simplement toute perte future."),
            ("Le fichier sera-t-il plus lourd ?", "Oui, généralement : le PNG sans perte pèse presque toujours "
             "plus lourd qu'un JPEG équivalent, surtout sur une photographie."),
        ],
    ),
}

# ---------------------------------------------------------------------------
# Per-input-format hub page (/convertisseur-x/) intro copy. Falls back to a
# generic paragraph built from FORMATS facts when a format has no override.
# ---------------------------------------------------------------------------
HUB_OVERRIDES = {
    "heic": dict(
        title="Convertisseur HEIC en ligne (iPhone, iPad)",
        meta="Convertissez vos photos HEIC d'iPhone en JPG, PNG ou WebP en ligne, gratuitement et sans upload. "
             "Le décodage se fait entièrement dans votre navigateur.",
        intro="Rendez vos photos iPhone lisibles sur Windows, Android et le web.",
    ),
    "svg": dict(
        title="Convertisseur SVG en ligne",
        meta="Convertissez vos SVG en PNG, JPG ou WebP en ligne, gratuitement. Rasterisation 100% dans le "
             "navigateur, sans upload.",
        intro="Transformez vos logos et icônes vectoriels en images matricielles classiques.",
    ),
}


def get_pair_copy(input_id, output_id):
    return PAIR_OVERRIDES.get((input_id, output_id))


def get_hub_copy(format_id):
    return HUB_OVERRIDES.get(format_id)


# ---------------------------------------------------------------------------
# Compression to a target weight (/compresser-image/ and its sub-pages)
# ---------------------------------------------------------------------------
# 1 Ko = 1 000 octets and 1 Mo = 1 000 000 octets: a result under "1 Mo" in
# this sense is also under 1 048 576 octets, so it passes either convention
# a destination site might use.

# (slug, bytes, label) — one page per threshold: /compresser-image-{slug}/
TARGET_SIZES = [
    ("50-ko", 50_000, "50 Ko"),
    ("100-ko", 100_000, "100 Ko"),
    ("200-ko", 200_000, "200 Ko"),
    ("300-ko", 300_000, "300 Ko"),
    ("500-ko", 500_000, "500 Ko"),
    ("1-mo", 1_000_000, "1 Mo"),
    ("2-mo", 2_000_000, "2 Mo"),
    ("5-mo", 5_000_000, "5 Mo"),
]

TARGET_USES = {
    "50-ko": "les formulaires les plus stricts, les avatars et les signatures d'e-mail",
    "100-ko": "les photos de profil, les miniatures et certains formulaires en ligne",
    "200-ko": "les formulaires de candidature, les photos de CV et les images de blog",
    "300-ko": "les images de site web et les pièces jointes légères",
    "500-ko": "les illustrations de site web et les annonces en ligne",
    "1-mo": "la plupart des téléservices administratifs (dont l'ANTS) et les pièces jointes",
    "2-mo": "les dossiers en ligne, les formulaires de recrutement et les envois groupés",
    "5-mo": "les photos haute définition à envoyer par e-mail ou sur une plateforme",
}

# Démarches: pages /compresser-photo-{slug}/ that preset the right limit.
# Only limits confirmed by an official source are stated as facts; "check
# the limit shown on the form" stays in every page because they can change.
DEMARCHES = {
    "ants": dict(
        path="/compresser-photo-ants/",
        crumb="Pour l'ANTS",
        title="Compresser une photo ou un justificatif pour l'ANTS (moins de 1 Mo)",
        h1="Photo trop lourde pour l'ANTS ? Passez-la sous 1 Mo",
        meta=("Justificatif refusé car trop volumineux sur le site de l'ANTS ? Compressez vos photos et scans "
              "sous 1 Mo en JPG, directement dans votre navigateur, sans envoyer vos documents."),
        intro="Carte grise, carte d'identité, passeport : chaque pièce jointe doit peser moins de 1 Mo. Vos documents restent sur votre appareil.",
        target=1_000_000,
        output="jpg",
        paragraphs=[
            "Sur la plupart des démarches du site de l'ANTS (carte grise, pré-demande de carte d'identité ou de "
            "passeport), chaque document téléversé ne doit pas dépasser 1 Mo et doit être au format JPEG, PNG ou "
            "PDF. Une photo prise au smartphone pèse souvent 3 à 5 Mo : elle est refusée avec un message indiquant "
            "que le fichier est trop volumineux.",
            "Déposez ici vos photos ou scans : chacun est recompressé en JPG sous 1 Mo en gardant la meilleure "
            "qualité possible, pour que le texte du document reste lisible. Si la compression ne suffit pas, "
            "l'image est légèrement réduite en dimensions.",
            "Il s'agit de pièces d'identité et de justificatifs : ils ne sont jamais envoyés sur un serveur. Tout "
            "le traitement a lieu dans votre navigateur.",
        ],
        faq=[
            ("Quelle est la taille maximale d'un fichier sur le site de l'ANTS ?",
             "Pour la plupart des démarches, 1 Mo par document, aux formats JPEG, PNG ou PDF. Vérifiez toujours "
             "la limite affichée sur le formulaire de votre démarche : elle peut différer (les demandes de permis "
             "de conduire acceptent par exemple des fichiers plus lourds)."),
            ("Mon document restera-t-il lisible ?",
             "Oui dans la grande majorité des cas : l'outil cherche la meilleure qualité qui tient sous 1 Mo "
             "avant de réduire les dimensions. Vérifiez l'aperçu avant de l'envoyer."),
            ("Mes documents d'identité sont-ils envoyés quelque part ?",
             "Non. La compression est faite par votre navigateur : aucune image ne quitte votre appareil."),
        ],
    ),
    "caf": dict(
        path="/compresser-photo-caf/",
        crumb="Pour la CAF",
        title="Compresser un justificatif pour la CAF (envoi de 10 Mo maximum)",
        h1="Justificatif trop lourd pour la CAF ? Allégez vos photos",
        meta=("Vos justificatifs dépassent la limite d'envoi de la CAF ? Compressez vos photos de documents en JPG "
              "dans votre navigateur, sans les envoyer sur un serveur."),
        intro="Un envoi de documents à la CAF ne doit pas dépasser 10 Mo au total. Allégez vos photos de justificatifs sans les envoyer nulle part.",
        target=2_000_000,
        output="jpg",
        paragraphs=[
            "Depuis l'espace « Mon Compte » de la CAF, un envoi de justificatifs ne doit pas dépasser 10 Mo pour "
            "l'ensemble des documents, aux formats JPEG, PDF, PNG ou GIF. Trois ou quatre photos de smartphone "
            "suffisent à dépasser cette limite.",
            "Le réglage par défaut (2 Mo par photo) permet d'envoyer jusqu'à cinq documents en un seul envoi. "
            "Pour un envoi plus important, choisissez 1 Mo ou 500 Ko dans le menu « Poids maximum ».",
            "Bulletins de salaire, quittances, avis d'imposition : ces documents restent sur votre appareil, la "
            "compression a lieu dans votre navigateur.",
        ],
        faq=[
            ("Quelle est la limite d'envoi de documents à la CAF ?",
             "10 Mo pour l'ensemble des documents d'un même envoi. Un envoi ne regroupe qu'un seul type de "
             "document : par exemple plusieurs bulletins de salaire, mais pas un bulletin et une quittance."),
            ("Quel poids choisir pour chaque photo ?",
             "Divisez 10 Mo par le nombre de documents à envoyer : 2 Mo par photo pour cinq documents, 1 Mo pour "
             "dix. Le texte reste lisible dans la plupart des cas."),
            ("Mes justificatifs sont-ils envoyés sur un serveur ?",
             "Non. Tout le traitement a lieu dans votre navigateur, rien ne quitte votre appareil."),
        ],
    ),
    "mail": dict(
        path="/compresser-photo-pour-mail/",
        crumb="Pour un e-mail",
        title="Photo trop lourde pour un mail : compresser ses photos avant l'envoi",
        h1="Photo trop lourde pour un mail ? Compressez-la avant l'envoi",
        meta=("Photos trop lourdes pour une pièce jointe ? Compressez-les en quelques secondes pour les envoyer "
              "par mail, gratuitement et sans les téléverser sur un serveur."),
        intro="Les messageries limitent le poids des pièces jointes. Réduisez vos photos à 1 Mo chacune pour en envoyer plusieurs dans un seul mail.",
        target=1_000_000,
        output="jpg",
        paragraphs=[
            "Gmail accepte jusqu'à 25 Mo de pièces jointes par message et Outlook.com jusqu'à 20 Mo ; beaucoup de "
            "messageries professionnelles sont plus strictes. Une série de photos de smartphone dépasse vite ces "
            "limites, et le message est refusé ou transformé en lien de téléchargement.",
            "À 1 Mo par photo, une vingtaine d'images tiennent dans un seul mail, tout en restant nettes sur un "
            "écran d'ordinateur ou de téléphone. Choisissez 500 Ko pour en envoyer davantage, ou 2 Mo pour une "
            "qualité d'impression.",
            "Vos photos ne transitent par aucun serveur : elles sont compressées dans votre navigateur puis "
            "téléchargées une à une ou groupées dans un ZIP.",
        ],
        faq=[
            ("Quelle taille de pièce jointe accepte Gmail ?",
             "25 Mo par message, toutes pièces jointes comprises. Au-delà, Gmail propose de partager les fichiers "
             "via Google Drive."),
            ("Quelle taille choisir pour mes photos ?",
             "1 Mo par photo convient à un affichage sur écran. Pour une impression en grand format, gardez 2 à "
             "5 Mo."),
            ("Puis-je compresser plusieurs photos d'un coup ?",
             "Oui, déposez-les toutes en même temps puis téléchargez le ZIP."),
        ],
    ),
    "web": dict(
        path="/compresser-image-pour-site-web/",
        crumb="Pour un site web",
        title="Compresser une image pour un site web (moins de 200 Ko)",
        h1="Compresser une image pour un site web",
        meta=("Réduisez le poids de vos images de site web sous 200 Ko en WebP ou JPG, pour des pages plus "
              "rapides. Gratuit, par lot, sans envoi sur un serveur."),
        intro="Des images légères accélèrent l'affichage de vos pages. Passez-les sous 200 Ko en WebP, en gardant la meilleure qualité possible.",
        target=200_000,
        output="webp",
        paragraphs=[
            "Les images représentent souvent la plus grande partie du poids d'une page web. Viser moins de 200 Ko "
            "par image de contenu est un bon repère pour un affichage rapide, y compris sur mobile.",
            "Le WebP est sélectionné par défaut : à qualité égale, il est nettement plus léger que le JPG et il est "
            "lu par tous les navigateurs actuels. Pour une image d'en-tête plein écran, 300 à 500 Ko peuvent être "
            "justifiés ; pour une miniature, 50 à 100 Ko suffisent.",
            "Si une image dépasse la limite même compressée, l'outil réduit ses dimensions : une photo de 4000 px "
            "de large est de toute façon affichée bien plus petite sur un site.",
        ],
        faq=[
            ("Quel poids viser pour une image de site web ?",
             "Moins de 200 Ko pour une image de contenu, 50 à 100 Ko pour une miniature, jusqu'à 500 Ko pour un "
             "grand visuel d'en-tête."),
            ("Faut-il utiliser le WebP ou le JPG ?",
             "Le WebP, sauf contrainte particulière : il est plus léger à qualité égale et compatible avec tous "
             "les navigateurs modernes. L'AVIF est encore plus léger mais plus lent à encoder."),
            ("Mes images sont-elles envoyées sur un serveur ?",
             "Non, la compression a lieu dans votre navigateur."),
        ],
    ),
}
