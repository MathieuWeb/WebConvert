# -*- coding: utf-8 -*-
"""Guide articles. Each entry renders as /guide/<slug>/. body_html uses the
same markup vocabulary as .article in css/styles.css (h2/h3, p, ul/ol,
table, .callout)."""

ARTICLES = [
    dict(
        slug="webp-avif-png-jpg-quel-format-choisir",
        tag="Comparatif",
        title="WebP, AVIF, PNG, JPG : quel format d'image choisir en 2026 ?",
        meta="Comparatif complet des formats d'image WebP, AVIF, PNG et JPG : poids, qualité, transparence, "
             "compatibilité. Le bon choix selon votre usage.",
        excerpt="Poids, qualité, transparence, compatibilité : le comparatif complet pour choisir sans se tromper.",
        published="2026-08-04",
        reading_time="7 min",
        lede="Il n'y a pas un seul « meilleur » format d'image : il y a le bon format pour chaque usage. "
             "Voici comment trancher en fonction de ce que vous publiez.",
        body_html="""
<h2>La question à se poser en premier</h2>
<p>Avant de comparer des chiffres de compression, une seule question compte vraiment : qu'est-ce que
contient l'image ? Une photographie et un logo n'ont pas les mêmes contraintes, et le format le plus adapté
change du tout au tout selon la réponse.</p>
<p>Une photographie tolère très bien la compression avec perte : l'œil ne distingue presque rien entre
l'original et une version compressée à 80%. Un logo en aplats de couleurs, à l'inverse, révèle immédiatement
le moindre artefact de compression sur ses bords nets.</p>

<h2>Le tableau comparatif</h2>
<table>
<tr><th>Format</th><th>Compression</th><th>Transparence</th><th>Poids typique</th><th>Compatibilité</th></tr>
<tr><td>JPG</td><td>Avec perte</td><td>Non</td><td>Référence</td><td>Universelle</td></tr>
<tr><td>PNG</td><td>Sans perte</td><td>Oui</td><td>Élevé sur photo, correct sur aplats</td><td>Universelle</td></tr>
<tr><td>WebP</td><td>Avec ou sans perte</td><td>Oui</td><td>-25 à -35% vs JPG</td><td>Très large depuis 2020</td></tr>
<tr><td>AVIF</td><td>Avec ou sans perte</td><td>Oui</td><td>-30 à -50% vs WebP</td><td>Bonne, navigateurs récents</td></tr>
</table>

<h2>JPG : le format qu'on ne peut pas se permettre d'abandonner</h2>
<p>Le JPEG a plus de trente ans et reste le plus universellement lu, y compris par des logiciels et appareils
très anciens. Pour une pièce jointe email, un visuel destiné à l'impression grand public ou tout contexte où
la compatibilité prime sur l'optimisation, c'est encore le choix le plus sûr.</p>

<h2>PNG : quand la netteté ne se négocie pas</h2>
<p>Un logo, une capture d'écran, une interface : dès qu'une image contient du texte ou des bords nets, le PNG
évite les halos et le flou que produirait une compression avec perte. Son défaut est le poids sur les photos,
là où il n'a simplement pas été conçu pour briller.</p>

<h2>WebP : le compromis raisonnable pour le web</h2>
<p>Pour un site web publié aujourd'hui, le WebP est presque toujours le bon choix par défaut : gain de poids
significatif, transparence gérée nativement, compatibilité large (Chrome, Firefox, Edge, Safari depuis la
version 14). C'est le format qui offre le meilleur rapport gain de performance / risque de compatibilité.</p>

<h2>AVIF : la pointe de la compression, avec des concessions</h2>
<p>L'AVIF va plus loin encore que le WebP en compression, au prix d'un encodage plus lent et d'une
compatibilité encore légèrement en retrait sur les logiciels desktop. Pour un site à fort trafic où chaque
kilo-octet économisé compte, c'est le format le plus rentable ; pour un usage plus occasionnel, le WebP reste
plus simple à généraliser sans arrière-pensée de compatibilité.</p>

<div class="callout">
<p>Règle simple : photo → JPG ou WebP ; logo/interface → PNG ou WebP ; site web où la performance est
critique → AVIF avec un repli WebP. Vous pouvez tester chaque conversion et comparer le poids obtenu avant
de choisir définitivement.</p>
</div>

<h2>Et les formats plus spécifiques ?</h2>
<p>Le GIF garde sa niche sur l'animation courte, malgré son poids et ses 256 couleurs. Le SVG s'impose dès
qu'une image est vectorielle par nature (logo, icône). Le TIFF reste l'outil des professionnels de l'image et
de l'impression. Le HEIC, enfin, n'a de sens qu'à l'intérieur de l'écosystème Apple : dès qu'il faut publier
ou partager ailleurs, une conversion en JPG ou PNG s'impose.</p>
""",
    ),
    dict(
        slug="confidentialite-conversion-image-navigateur",
        tag="Confidentialité",
        title="Pourquoi la confidentialité compte quand vous convertissez une image",
        seo_title="Conversion d'image et confidentialité : ce qu'il faut savoir",
        meta="Vos photos contiennent souvent plus qu'une image : position GPS, appareil, informations sensibles. "
             "Pourquoi la conversion locale change tout.",
        excerpt="Vos photos contiennent souvent plus d'informations que ce qu'elles montrent. Voici pourquoi "
                "l'endroit où elles sont converties n'est pas un détail.",
        published="2026-08-18",
        reading_time="6 min",
        lede="Convertir une image semble anodin. Mais selon l'endroit où cette conversion a lieu, vous "
             "envoyez peut-être bien plus qu'un simple fichier.",
        body_html="""
<h2>Ce qu'un fichier image contient vraiment</h2>
<p>Un fichier JPG ou HEIC issu d'un smartphone embarque presque toujours des métadonnées EXIF : modèle de
l'appareil, date et heure précises de la prise de vue, et très souvent des coordonnées GPS exactes du lieu où
la photo a été prise. Une capture d'écran peut, elle, révéler des informations affichées à l'écran au moment
où elle a été prise : un email, un numéro de commande, une conversation.</p>
<p>Rien de tout cela n'est visible en un coup d'œil sur la photo elle-même. C'est précisément ce qui rend le
sujet facile à négliger.</p>

<h2>Ce qui se passe avec un convertisseur classique « en ligne »</h2>
<p>La plupart des convertisseurs d'image en ligne fonctionnent de la même façon : votre fichier est envoyé
sur un serveur distant, converti là-bas, puis le résultat vous est renvoyé. Entre ces deux étapes, votre
image — et tout ce qu'elle contient — a transité par une infrastructure que vous ne contrôlez pas et dont
vous ne connaissez ni la politique de conservation, ni la durée réelle de suppression, ni les sous-traitants
éventuels.</p>
<p>Dans l'immense majorité des cas, ce n'est probablement pas un problème. Mais pour une pièce d'identité
scannée, un document professionnel confidentiel ou simplement une photo personnelle, ce « probablement »
ne devrait pas être la seule garantie disponible.</p>

<h2>La conversion locale change la nature de la question</h2>
<p>Quand la conversion a lieu directement dans votre navigateur — via l'API Canvas, comme c'est le cas sur ce
site — le fichier ne quitte jamais votre appareil. Il n'y a rien à envoyer, donc rien à intercepter, rien à
stocker par erreur, rien à sous-traiter. La question de la confidentialité ne se pose plus en ces termes,
elle disparaît structurellement plutôt que d'être promise par une politique de confidentialité qu'il faut
croire sur parole.</p>

<div class="callout">
<p>Vous pouvez vérifier ce point vous-même : ouvrez les outils de développement de votre navigateur, onglet
Réseau, avant de convertir une image sur ce site. Aucune requête contenant votre fichier ne part vers un
serveur — c'est vérifiable, pas seulement annoncé.</p>
</div>

<h2>Les bons réflexes, au-delà du choix de l'outil</h2>
<ul>
<li>Avant de partager une photo prise avec un smartphone, vérifiez si elle contient des données de
localisation que vous ne souhaitez pas diffuser.</li>
<li>Pour un document scanné ou une pièce sensible, privilégiez systématiquement un outil qui traite le
fichier localement plutôt qu'un service qui l'envoie sur un serveur.</li>
<li>Convertir un fichier change son format, mais ne supprime pas automatiquement ses métadonnées : gardez
cela en tête si l'objectif est justement de les retirer.</li>
</ul>
""",
    ),
    dict(
        slug="convertir-heic-iphone",
        tag="Guide pratique",
        title="Photos HEIC d'iPhone illisibles : le guide complet pour les convertir",
        seo_title="Photos HEIC d'iPhone : comment les convertir en JPG",
        meta="Pourquoi vos photos iPhone sont en .HEIC, pourquoi elles ne s'ouvrent pas sur Windows ou "
             "Android, et comment les convertir simplement en JPG ou PNG.",
        excerpt="Pourquoi vos photos iPhone sont illisibles ailleurs, et comment les rendre compatibles avec "
                "n'importe quel appareil en quelques secondes.",
        published="2026-08-27",
        reading_time="5 min",
        lede="Vous transférez une photo depuis votre iPhone et elle refuse de s'ouvrir sur votre PC ou de "
             "s'afficher sur un site web ? Voici pourquoi, et comment régler le problème.",
        body_html="""
<h2>Pourquoi l'iPhone enregistre en HEIC</h2>
<p>Depuis iOS 11 (2017), l'iPhone enregistre ses photos au format HEIC (High Efficiency Image Container) par
défaut plutôt qu'en JPEG. La raison est simple : à qualité visuelle équivalente, un fichier HEIC pèse environ
deux fois moins lourd qu'un JPEG. Sur un appareil au stockage limité, l'économie est significative sur
plusieurs milliers de photos.</p>

<h2>Pourquoi ça pose problème ailleurs</h2>
<p>Le HEIC s'appuie sur la même technologie de compression que le codec vidéo HEVC, plus récente et plus
complexe que celle du JPEG. Apple l'a largement adopté, mais son support reste inégal en dehors de son
écosystème : de nombreuses versions de Windows, une bonne partie des sites web, des outils professionnels et
des appareils Android ne savent tout simplement pas l'afficher nativement.</p>
<p>Résultat concret : une photo qui s'affiche normalement sur l'iPhone devient une icône de fichier vide une
fois transférée sur un PC Windows plus ancien, ou refuse d'être mise en ligne sur un site qui n'accepte que
le JPG et le PNG.</p>

<h2>Trois façons de régler le problème</h2>
<ol>
<li><strong>Convertir les photos existantes.</strong> Pour des photos déjà prises, la solution la plus rapide
est de les convertir en JPG (universel, léger) ou en PNG (sans perte, plus lourd) via un convertisseur qui
traite le fichier directement dans le navigateur, sans l'envoyer sur un serveur tiers.</li>
<li><strong>Changer le format de capture sur l'iPhone.</strong> Réglages → Appareil photo → Formats → choisir
« Le plus compatible » fait enregistrer les futures photos directement en JPEG, au prix d'un espace de
stockage légèrement supérieur.</li>
<li><strong>Activer la conversion automatique au transfert.</strong> Sur Mac et Windows (avec les bons
pilotes), l'option « Conserver le plus compatible » dans les réglages de transfert de photos convertit
automatiquement le HEIC en JPEG au moment de l'importation, sans toucher aux photos sur l'iPhone lui-même.</li>
</ol>

<h2>JPG ou PNG : lequel choisir pour vos photos HEIC ?</h2>
<p>Pour la très large majorité des photos (des prises de vue classiques), le JPG est le bon choix : format
universel, poids raisonnable, qualité largement suffisante pour le partage et la publication. Réservez le PNG
aux cas où vous avez besoin d'une fidélité sans aucune perte supplémentaire, par exemple avant une retouche
poussée.</p>

<div class="callout">
<p>La conversion HEIC de ce site s'appuie sur une librairie de décodage exécutée entièrement dans votre
navigateur : vos photos ne sont jamais envoyées à un serveur, y compris pendant l'étape de décodage HEIC.</p>
</div>
""",
    ),
    dict(
        slug="quest-ce-que-avif",
        tag="Format",
        title="Qu'est-ce que l'AVIF et pourquoi l'adopter",
        meta="AVIF : le format d'image le plus efficace du moment. Origine, avantages, compatibilité, et "
             "quand l'utiliser plutôt que le WebP.",
        excerpt="Le format le plus efficace du moment pour le web, expliqué simplement : origine, avantages, "
                "limites et cas d'usage.",
        published="2026-09-02",
        reading_time="5 min",
        lede="L'AVIF s'impose progressivement comme le format d'image le plus efficace disponible dans les "
             "navigateurs. Voici ce qu'il apporte concrètement.",
        body_html="""
<h2>D'où vient l'AVIF</h2>
<p>AVIF signifie AV1 Image File Format. Comme son nom l'indique, il dérive directement du codec vidéo AV1,
développé par l'Alliance for Open Media (un consortium réunissant Google, Mozilla, Netflix, Apple et
d'autres). Standardisé en 2019, il applique à une image fixe les mêmes techniques de compression très
avancées utilisées pour la vidéo.</p>

<h2>Ce que ça change concrètement</h2>
<p>Le résultat le plus visible est le poids du fichier : à qualité visuelle comparable, un AVIF pèse
généralement 30 à 50% de moins qu'un WebP, lui-même déjà 25 à 35% plus léger qu'un JPEG. Sur un site avec de
nombreuses images, l'effet cumulé sur le temps de chargement peut être important.</p>
<p>L'AVIF gère aussi nativement la transparence (comme le PNG et le WebP) et peut encoder aussi bien en mode
avec perte qu'en mode totalement sans perte, ce qui en fait un format polyvalent plutôt qu'un simple concurrent
du JPEG sur les photos.</p>

<h2>Les limites à connaître</h2>
<ul>
<li><strong>Encodage plus lent.</strong> Produire un fichier AVIF demande plus de calcul qu'un JPEG ou un
WebP. Pour une conversion ponctuelle, ce n'est pas gênant ; pour un traitement automatisé de très gros
volumes, c'est un facteur à anticiper.</li>
<li><strong>Compatibilité encore progressive.</strong> Les navigateurs récents (Chrome, Firefox, Safari 16+)
le décodent sans problème, mais certains logiciels de bureau, anciens systèmes ou outils professionnels ne
le prennent pas encore en charge.</li>
</ul>

<h2>WebP ou AVIF : comment choisir</h2>
<p>Si la compatibilité maximale avec des logiciels tiers ou des navigateurs plus anciens compte, le WebP
reste le choix le plus sûr. Si l'objectif est de minimiser le poids des images sur un site à fort trafic et
que votre audience utilise majoritairement des navigateurs récents, l'AVIF apporte un gain réel et mesurable.</p>
<p>En pratique, beaucoup de sites servent aujourd'hui de l'AVIF avec un repli automatique vers le WebP, puis
vers le JPEG, pour couvrir l'ensemble des cas sans sacrifier la performance pour la majorité des visiteurs.</p>
""",
    ),
    dict(
        slug="png-vs-jpg",
        tag="Comparatif",
        title="PNG vs JPG : bien choisir pour ne pas perdre en qualité",
        meta="PNG ou JPG ? Le guide pour choisir le bon format selon le contenu de votre image et éviter les "
             "pertes de qualité évitables.",
        excerpt="Le choix entre PNG et JPG semble anodin, mais il détermine directement la netteté et le "
                "poids final de votre image.",
        published="2026-09-10",
        reading_time="5 min",
        lede="PNG et JPG sont les deux formats les plus connus, et pourtant beaucoup d'images sont enregistrées "
             "dans le mauvais des deux.",
        body_html="""
<h2>La différence fondamentale</h2>
<p>Le JPG compresse avec perte : il supprime des détails que l'œil humain perçoit mal, ce qui réduit
fortement le poids du fichier au prix d'une fidélité légèrement dégradée. Le PNG compresse sans perte :
chaque pixel de l'image d'origine est restitué à l'identique, mais le fichier est plus lourd, en particulier
sur des images photographiques riches en détails.</p>

<h2>Pourquoi un logo en JPG a souvent l'air « sale »</h2>
<p>La compression JPEG fonctionne par blocs de pixels et lisse les transitions progressives d'une
photographie sans que l'œil le remarque. Mais sur un bord net — le contour d'un logo, une lettre de texte —
cette même technique produit un halo ou un flou visible, surtout autour des zones de fort contraste. C'est le
symptôme le plus courant d'un mauvais choix de format.</p>
<p>Le PNG, en conservant chaque pixel exactement, n'a pas ce défaut : les bords restent parfaitement nets,
quel que soit le niveau de zoom.</p>

<h2>Pourquoi une photo en PNG est presque toujours du gaspillage</h2>
<p>À l'inverse, une photographie enregistrée en PNG n'a généralement rien à gagner en netteté (l'œil ne
perçoit pas la différence avec un JPEG bien réglé) mais peut peser plusieurs fois plus lourd. Pour du contenu
photographique, le PNG n'apporte quasiment jamais d'avantage perceptible, seulement un poids de fichier plus
élevé.</p>

<h2>Le tableau de décision</h2>
<table>
<tr><th>Contenu de l'image</th><th>Format recommandé</th><th>Pourquoi</th></tr>
<tr><td>Photographie</td><td>JPG (ou WebP)</td><td>Compression efficace, perte imperceptible</td></tr>
<tr><td>Logo, texte, icône</td><td>PNG</td><td>Bords nets, aucune perte</td></tr>
<tr><td>Capture d'écran</td><td>PNG</td><td>Netteté du texte préservée</td></tr>
<tr><td>Image avec transparence</td><td>PNG (ou WebP)</td><td>Le JPG n'a pas de canal alpha</td></tr>
</table>

<div class="callout">
<p>Vous avez déjà un fichier dans le mauvais format ? La conversion ne « répare » pas une qualité déjà
perdue (un JPG resté flou ne redeviendra pas net en PNG), mais elle évite d'accumuler des pertes
supplémentaires lors des prochaines étapes de traitement.</p>
</div>
""",
    ),
    dict(
        slug="reduire-poids-images-site-web",
        tag="Performance web",
        title="Réduire le poids de ses images sans perdre en qualité : le guide complet",
        seo_title="Réduire le poids de ses images sans perte de qualité",
        meta="Les images représentent souvent la majorité du poids d'une page web. Voici comment les alléger "
             "sans sacrifice visuel perceptible.",
        excerpt="Les images pèsent souvent plus de la moitié du poids total d'une page web. Voici comment les "
                "alléger sans sacrifice visuel perceptible.",
        published="2026-09-16",
        reading_time="6 min",
        lede="Sur la plupart des sites, les images représentent la plus grande part du poids total d'une "
             "page — et la marge de progression la plus facile à obtenir.",
        body_html="""
<h2>Pourquoi ça compte</h2>
<p>Le poids des images influence directement la vitesse de chargement perçue, les métriques Core Web Vitals
utilisées par Google (en particulier le LCP, Largest Contentful Paint) et, in fine, le taux de rebond des
visiteurs sur mobile en connexion limitée. Alléger ses images est souvent le levier de performance le plus
simple à activer, sans toucher au code du site.</p>

<h2>1. Choisir le bon format avant tout</h2>
<p>Avant même de régler un curseur de qualité, le choix du format détermine l'essentiel du gain possible.
Une photographie en WebP pèsera 25 à 35% de moins que le même contenu en JPEG, et jusqu'à 50% de moins encore
en AVIF, sans perte visuelle perceptible dans la majorité des cas.</p>

<h2>2. Ne pas confondre dimensions et poids</h2>
<p>Redimensionner une image à sa taille d'affichage réelle avant de la convertir change beaucoup plus le
poids final que le seul réglage de qualité. Une image de 4000 pixels de large affichée dans un espace de 800
pixels gaspille l'essentiel de son poids en détails invisibles à l'écran.</p>

<h2>3. Régler la qualité en fonction du contenu, pas d'une valeur unique</h2>
<p>Un réglage de qualité entre 70 et 85 (sur une échelle 0-100) est généralement suffisant pour une
photographie, avec un gain de poids important et une perte invisible à l'œil nu. Sur un visuel contenant du
texte ou des aplats nets, privilégiez un réglage plus élevé, proche de 95-100, pour éviter tout artefact
visible sur les bords.</p>

<h2>4. Ne pas oublier la transparence</h2>
<p>Si une image n'a pas besoin de transparence, ne la conservez pas en PNG « par habitude » : convertir
en JPG ou en WebP avec fond opaque réduit souvent le poids de manière significative, sans aucune perte
d'information utile.</p>

<h2>5. Automatiser plutôt que traiter au cas par cas</h2>
<p>Pour un site avec de nombreuses images, convertissez vos visuels par lot plutôt qu'un par un : cela
garantit un format et un réglage cohérents sur l'ensemble du site, et fait gagner un temps considérable par
rapport à un traitement image par image.</p>

<div class="callout">
<p>Ce site convertit vos images par lot, directement dans le navigateur : déposez plusieurs fichiers à la
fois sur n'importe quelle page de conversion, ajustez le curseur de qualité, et téléchargez le résultat en
une seule archive ZIP.</p>
</div>
""",
    ),
    dict(
        slug="creer-favicon-ico",
        tag="Guide pratique",
        title="Créer une favicon .ico à partir de votre logo : le guide complet",
        seo_title="Créer une favicon .ico à partir de son logo",
        meta="Comment transformer votre logo en favicon.ico prête à l'emploi pour votre site web, avec les "
             "bonnes dimensions et les bons réglages.",
        excerpt="La petite icône affichée dans l'onglet du navigateur mérite un peu plus d'attention qu'on ne "
                "le pense. Voici comment la préparer correctement.",
        published="2026-09-20",
        reading_time="4 min",
        lede="La favicon est la première chose qu'un visiteur voit avant même d'ouvrir votre page. Voici "
             "comment en préparer une correctement à partir de votre logo.",
        body_html="""
<h2>Pourquoi le format .ico reste incontournable</h2>
<p>Malgré l'existence de formats plus modernes pour les icônes de site (PNG, SVG), le fichier favicon.ico
reste la référence historique reconnue sans exception par tous les navigateurs, y compris les plus anciens.
C'est la valeur de repli la plus sûre, même si vous ajoutez également des variantes PNG ou SVG pour les
usages plus récents (icônes d'accueil mobile, PWA).</p>

<h2>Partir d'un bon visuel source</h2>
<p>Une favicon s'affiche à une taille minuscule (souvent 16 à 32 pixels dans l'onglet du navigateur). Un
logo trop détaillé ou trop chargé devient illisible à cette échelle. Les meilleurs résultats viennent en
général d'un visuel simple, carré, à fort contraste :</p>
<ul>
<li>Partez d'une image carrée, idéalement 512×512 pixels ou plus, pour garder de la marge à la réduction.</li>
<li>Simplifiez si besoin : un monogramme ou un symbole isolé fonctionne mieux qu'un logo complet avec texte
à cette taille d'affichage.</li>
<li>Un fond transparent (PNG) laisse la favicon s'adapter aux thèmes clair et sombre du navigateur.</li>
</ul>

<h2>La conversion</h2>
<p>Déposez votre logo au format PNG (ou JPG) sur le convertisseur PNG vers ICO de ce site : l'image est
automatiquement réduite à 256 pixels maximum, la taille standard utilisée pour les favicons et icônes
d'application, en conservant la transparence si votre PNG en contient une.</p>

<h2>Installer le fichier obtenu</h2>
<p>Deux options, à combiner idéalement :</p>
<ol>
<li>Déposez le fichier à la racine de votre site sous le nom <code>favicon.ico</code> : la plupart des
navigateurs le détectent automatiquement à cet emplacement, sans configuration supplémentaire.</li>
<li>Référencez-le explicitement dans le <code>&lt;head&gt;</code> de vos pages avec
<code>&lt;link rel="icon" href="/favicon.ico"&gt;</code>, pour un contrôle plus fiable sur tous les
navigateurs.</li>
</ol>

<div class="callout">
<p>Pour une compatibilité optimale avec les appareils Apple et Android, complétez votre favicon.ico par des
variantes PNG dédiées (apple-touch-icon, icônes Android Chrome) : la favicon .ico couvre l'essentiel, ces
variantes couvrent les cas particuliers.</p>
</div>
""",
    ),
]
