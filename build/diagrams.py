# -*- coding: utf-8 -*-
"""Inline SVG diagrams for the platform pages (zones and layout examples).
Same visual vocabulary as the LinkedIn guide's diagrams (build/articles.py):
banner in a warm grey, profile photo as a white disc, hatched orange for what
gets hidden, green for the safe area. Text is real sample copy, sized to stay
readable once a figure shrinks to a phone's width. Every SVG id is prefixed so
that several figures can share a page."""

FONT = 'font-family="Figtree, system-ui, sans-serif"'
INK, MUTED, BANNER = "#23221f", "#5d5a53", "#d8d3c9"
ORANGE, GREEN, BLUE = "#c9521c", "#2f6b3b", "#1f6fb2"


def svg(vw, vh, inner, label, defs=""):
    return (f'<svg viewBox="0 0 {vw} {vh}" role="img" aria-label="{label}" xmlns="http://www.w3.org/2000/svg">'
            f'{defs}{inner}</svg>')


def text(x, y, txt, size, color=INK, weight=400, anchor="start"):
    return (f'<text x="{x}" y="{y}" {FONT} font-size="{size}" font-weight="{weight}" '
            f'fill="{color}" text-anchor="{anchor}">{txt}</text>')


def rect(x, y, w, h, fill="none", stroke=None, sw=2, rx=0, dash=None, opacity=None):
    attrs = f'x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"'
    if rx:
        attrs += f' rx="{rx}"'
    if stroke:
        attrs += f' stroke="{stroke}" stroke-width="{sw}"'
    if dash:
        attrs += f' stroke-dasharray="{dash}"'
    if opacity is not None:
        attrs += f' fill-opacity="{opacity}"'
    return f"<rect {attrs}/>"


def avatar(cx, cy, r):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fbfaf8" stroke="{INK}" stroke-width="2"/>'
            f'<circle cx="{cx}" cy="{cy - r * 0.24}" r="{r * 0.32}" fill="#bdb8ad"/>'
            f'<path d="M{cx - r * 0.65} {cy + r * 0.66}a{r * 0.65} {r * 0.53} 0 0 1 {r * 1.3} 0z" fill="#bdb8ad"/>')


def hatch(pid):
    return (f'<pattern id="{pid}" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<rect width="6" height="6" fill="{ORANGE}" fill-opacity="0.12"/>'
            f'<line x1="0" y1="0" x2="0" y2="6" stroke="{ORANGE}" stroke-opacity="0.5" stroke-width="2"/></pattern>')


def gradient(gid, c1, c2):
    return (f'<linearGradient id="{gid}" x1="0" x2="1"><stop offset="0" stop-color="{c1}"/>'
            f'<stop offset="1" stop-color="{c2}"/></linearGradient>')


def figure(svg_html, caption):
    return f'<figure class="diagram">\n{svg_html}\n<figcaption>{caption}</figcaption>\n</figure>'


# --------------------------------------------------------------------------
# YouTube channel banner: 2560 × 1440 drawn at 400 × 225.
# --------------------------------------------------------------------------
_YT_W, _YT_H = 400, 225
_YT_BAND_Y, _YT_BAND_H = (1440 - 423) / 2 / 1440 * _YT_H, 423 / 1440 * _YT_H
_YT_TAB_W, _YT_MOB_W = 1855 / 2560 * _YT_W, 1546 / 2560 * _YT_W


def youtube_zones():
    by, bh = round(_YT_BAND_Y, 1), round(_YT_BAND_H, 1)
    tx, mx = round((_YT_W - _YT_TAB_W) / 2, 1), round((_YT_W - _YT_MOB_W) / 2, 1)
    inner = (
        rect(0, 0, _YT_W, _YT_H, BANNER, rx=6)
        + text(12, 24, "TV : image entière", 14, INK, 700)
        + rect(0, by, _YT_W, bh, "#fbfaf8", opacity=0.35)
        + rect(1, by, _YT_W - 2, bh, stroke=ORANGE)
        + rect(tx, by, round(_YT_TAB_W, 1), bh, stroke=BLUE, dash="5 4")
        + rect(mx, by + 6, round(_YT_MOB_W, 1), bh - 12, "#fbfaf8", stroke=GREEN, sw=2.5, rx=3, opacity=0.75)
        + text(200, by + bh / 2 + 1, "Mobile : zone sûre", 15, GREEN, 700, "middle")
        + text(200, by + bh / 2 + 19, "texte et logo ici", 13, INK, 400, "middle")
        + text(8, by - 8, "Ordinateur", 13, ORANGE, 700)
        + text(tx + 4, by + bh + 17, "Tablette", 13, BLUE, 700)
    )
    return svg(_YT_W, _YT_H, inner,
               "Schéma : l'image entière n'est visible que sur TV ; ordinateur et tablette montrent une bande "
               "centrale ; la zone sûre au centre est visible partout")


def youtube_example(gid, c1, c2, title, sub, dark=False, deco=""):
    """Banner example: decorative background (seen in full on TV only) and
    the text kept inside the mobile safe zone, shown dashed."""
    by, bh = _YT_BAND_Y, _YT_BAND_H
    col, subcol = ("#fbfaf8", "#fbfaf8") if dark else (INK, MUTED)
    inner = (
        f'<rect x="0" y="0" width="{_YT_W}" height="{_YT_H}" rx="6" fill="url(#{gid})"/>' + deco
        + rect(round((_YT_W - _YT_MOB_W) / 2, 1), round(by + 3, 1), round(_YT_MOB_W, 1), round(bh - 6, 1),
               stroke=col, sw=1, dash="3 4", rx=3)
        + text(200, round(by + bh / 2 + 3, 1), title, 26, col, 800, "middle")
        + text(200, round(by + bh / 2 + 22, 1), sub, 14, subcol, 500, "middle")
    )
    return svg(_YT_W, _YT_H, inner, f"Exemple de bannière YouTube : « {title} », {sub}",
               defs="<defs>" + gradient(gid, c1, c2) + "</defs>")


def deco_plates():
    return ('<circle cx="30" cy="40" r="44" fill="#fbfaf8" fill-opacity="0.35"/>'
            '<circle cx="30" cy="40" r="28" fill="none" stroke="#fbfaf8" stroke-opacity="0.6" stroke-width="3"/>'
            '<circle cx="372" cy="190" r="52" fill="#fbfaf8" fill-opacity="0.3"/>'
            '<circle cx="372" cy="190" r="34" fill="none" stroke="#fbfaf8" stroke-opacity="0.55" stroke-width="3"/>')


def deco_stripes():
    return "".join(f'<path d="M{x} 225 L{x + 120} 0" stroke="#b48cff" stroke-opacity="0.18" stroke-width="10"/>'
                   for x in (-60, -20, 300, 340, 380))


def deco_grid():
    lines = "".join(f'<path d="M{x} 0 V225" stroke="{GREEN}" stroke-opacity="0.13"/>' for x in range(0, 401, 40))
    lines += "".join(f'<path d="M0 {y} H400" stroke="{GREEN}" stroke-opacity="0.13"/>' for y in range(0, 226, 25))
    return lines + f'<rect x="40" y="25" width="40" height="25" fill="{GREEN}" fill-opacity="0.18"/>' \
                   f'<rect x="320" y="175" width="40" height="25" fill="{GREEN}" fill-opacity="0.18"/>'


def deco_landscape():
    return ('<circle cx="320" cy="58" r="26" fill="#ffe6b3" fill-opacity="0.9"/>'
            '<path d="M0 170 L90 120 L170 155 L260 105 L340 140 L400 118 V225 H0Z" fill="#2c3e50" fill-opacity="0.35"/>'
            '<path d="M0 200 L110 160 L210 190 L300 150 L400 180 V225 H0Z" fill="#1d2a36" fill-opacity="0.55"/>')


# --------------------------------------------------------------------------
# Facebook cover: 851 × 315 drawn at 400 × 148 (+ room under it).
# --------------------------------------------------------------------------
_FB_W, _FB_H = 400, 148
_FB_MOBILE_W = 315 * 2.4 / 851 * _FB_W


def facebook_zones():
    mw = round(_FB_MOBILE_W, 1)
    inner = (
        rect(0, 0, _FB_W, _FB_H, BANNER, rx=6)
        + f'<rect x="{mw}" y="0" width="{round(_FB_W - mw, 1)}" height="{_FB_H}" fill="url(#fbz-h)"/>'
        + f'<line x1="{mw}" y1="0" x2="{mw}" y2="{_FB_H}" stroke="{BLUE}" stroke-width="2" stroke-dasharray="5 4"/>'
        + f'<rect x="8" y="80" width="96" height="68" fill="url(#fbz-h)"/>'
        + avatar(52, 116, 38)
        + rect(132, 30, 210, 62, "#fbfaf8", stroke=GREEN, sw=2.5, rx=4, opacity=0.65)
        + text(146, 56, "Zone la plus sûre", 16, GREEN, 700)
        + text(146, 77, "texte, logo, sujet", 14)
        + text(100, 176, "← masqué par la photo", 13, ORANGE, 600)
        + text(398, 176, "coupé sur mobile ↑", 13, BLUE, 600, "end")
    )
    return svg(_FB_W, 186, inner,
               "Schéma : la photo de profil masque le bas à gauche, la droite peut être coupée sur mobile, "
               "la zone la plus sûre est au centre",
               defs="<defs>" + hatch("fbz-h") + "</defs>")


def facebook_example(gid, c1, c2, title, sub, dark=False, photo=False, pill=None, deco=""):
    col, subcol = ("#fbfaf8", "#fbfaf8") if dark else (INK, MUTED)
    hills = ('<circle cx="300" cy="46" r="20" fill="#fff1d6" fill-opacity="0.9"/>'
             f'<path d="M0 104 L70 74 L150 98 L240 52 L320 86 L400 62 L400 {_FB_H} L0 {_FB_H}Z" fill="{INK}" fill-opacity="0.22"/>'
             f'<path d="M0 128 L90 104 L190 124 L280 98 L400 118 L400 {_FB_H} L0 {_FB_H}Z" fill="{INK}" fill-opacity="0.35"/>'
             ) if photo else ""
    pill_html = ""
    if pill:
        pw = len(pill) * 7 + 20
        pill_html = (rect(round(236 - pw / 2), 84, pw, 22, "#fbfaf8" if dark else INK, rx=11,
                          opacity=0.18 if dark else 0.88)
                     + text(236, 99, pill, 12.5, "#fbfaf8", 700, "middle"))
    inner = (
        f'<rect x="0" y="0" width="{_FB_W}" height="{_FB_H}" rx="6" fill="url(#{gid})"/>' + deco + hills
        + (text(236, 60, title, 23, col, 800, "middle") if title else "")
        + (text(236, 82, sub, 13, subcol, 500, "middle") if sub and not pill else "")
        + pill_html
        + avatar(52, 116, 38)
    )
    return svg(_FB_W, 160, inner, f"Exemple de couverture Facebook : {title or 'photo seule'}"
               + (f", {pill or sub}" if (pill or sub) else ""), defs="<defs>" + gradient(gid, c1, c2) + "</defs>")


def deco_bakery():
    return ('<circle cx="392" cy="10" r="46" fill="#fbfaf8" fill-opacity="0.35"/>'
            '<circle cx="380" cy="132" r="30" fill="#c98a3f" fill-opacity="0.18"/>'
            '<path d="M120 22 q10 -12 20 0 q10 -12 20 0" stroke="#c98a3f" stroke-opacity="0.45" stroke-width="3" fill="none"/>')


def deco_confetti():
    dots = ((120, 24, "#f4b860"), (150, 128, "#fbfaf8"), (330, 26, "#fbfaf8"), (372, 110, "#f4b860"),
            (300, 132, "#9fd1ff"), (186, 18, "#9fd1ff"), (392, 58, "#fbfaf8"), (110, 70, "#f4b860"))
    return "".join(f'<rect x="{x}" y="{y}" width="8" height="8" rx="2" fill="{c}" fill-opacity="0.7" '
                   f'transform="rotate(25 {x + 4} {y + 4})"/>' for x, y, c in dots)


# --------------------------------------------------------------------------
# Twitch profile banner: 1200 × 480 drawn at 400 × 160.
# --------------------------------------------------------------------------
def twitch_zones():
    inner = (
        rect(0, 0, 400, 160, BANNER, rx=6)
        + rect(12, 14, 188, 132, "#fbfaf8", stroke=GREEN, sw=2.5, rx=4, opacity=0.65)
        + text(26, 44, "Éléments graphiques", 15, GREEN, 700)
        + text(26, 64, "pseudo, logo, planning", 13)
        + f'<path d="M232 80 H372" stroke="{ORANGE}" stroke-width="2" stroke-dasharray="5 4"/>'
        + f'<path d="M364 72 L376 80 L364 88" fill="none" stroke="{ORANGE}" stroke-width="2"/>'
        + text(302, 66, "s'étire selon", 13, ORANGE, 600, "middle")
        + text(302, 106, "la fenêtre", 13, ORANGE, 600, "middle")
    )
    return svg(400, 160, inner,
               "Schéma : Twitch conseille de concentrer les éléments graphiques à gauche, la bannière s'étirant "
               "selon la largeur de la fenêtre")


def twitch_example(gid, c1, c2, title, sub):
    inner = (
        f'<rect x="0" y="0" width="400" height="160" rx="6" fill="url(#{gid})"/>'
        + f'<circle cx="330" cy="80" r="46" fill="#fbfaf8" fill-opacity="0.12"/>'
        + f'<circle cx="352" cy="58" r="22" fill="#fbfaf8" fill-opacity="0.1"/>'
        + text(26, 76, title, 26, "#fbfaf8", 800)
        + text(26, 100, sub, 13, "#fbfaf8", 500)
    )
    return svg(400, 160, inner, f"Exemple de bannière Twitch : « {title} », {sub}",
               defs="<defs>" + gradient(gid, c1, c2) + "</defs>")


# --------------------------------------------------------------------------
# YouTube thumbnail: 16:9 drawn at 400 × 225.
# --------------------------------------------------------------------------
def thumbnail_example():
    inner = (
        '<rect x="0" y="0" width="400" height="225" rx="6" fill="url(#ytt-g)"/>'
        + avatar(108, 130, 70)
        + text(206, 92, "3 ASTUCES", 34, "#fbfaf8", 800)
        + text(206, 130, "que personne", 22, "#fbfaf8", 700)
        + text(206, 156, "ne connaît", 22, "#fbfaf8", 700)
        + '<rect x="326" y="186" width="64" height="30" rx="4" fill="url(#ytt-h)"/>'
        + rect(334, 192, 48, 18, INK, rx=3, opacity=0.85)
        + text(358, 206, "12:34", 12, "#fbfaf8", 700, "middle")
        + rect(324, 184, 68, 34, stroke=ORANGE, sw=2, rx=5, dash="4 3")
    )
    return svg(400, 225, inner,
               "Exemple de miniature YouTube : un visage à gauche, trois mots en gros à droite, rien sous le "
               "badge de durée en bas à droite",
               defs="<defs>" + gradient("ytt-g", "#3a3833", "#c9521c") + hatch("ytt-h") + "</defs>")
