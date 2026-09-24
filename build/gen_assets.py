"""One-off asset generator: favicons, OG image, logo-square. Reuses the exact
brand mark from webpconvert.fr (abstract tab + bars, not tied to one format)
with the Webconvert.fr wordmark. Run once, not part of the shipped site.
"""
from PIL import Image, ImageDraw, ImageFont
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS = os.path.join(ROOT, "assets")
ICONS = os.path.join(ASSETS, "icons")
os.makedirs(ICONS, exist_ok=True)

INK = (26, 23, 20, 255)
CREAM = (244, 239, 233, 255)
CARD = (255, 253, 251, 255)
ORANGE = (255, 107, 43, 255)
RUST = (196, 69, 26, 255)

ARIAL_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
ARIAL = "/System/Library/Fonts/Supplemental/Arial.ttf"


def draw_mark(size, bg=None, pad_ratio=0.0):
    S = size * 4
    pad = int(S * pad_ratio)
    box = S - pad * 2
    img = Image.new("RGBA", (S, S), bg if bg else (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    REF = 30.0
    radius = round(box * (7 / REF))
    border_w = max(2, round(box * (1.5 / REF)))
    x0, y0 = pad, pad
    x1, y1 = pad + box, pad + box

    d.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=CARD, outline=INK, width=border_w)

    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=255)
    tab_w = round(box * (12 / REF))
    tab_layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(tab_layer).rectangle([x0, y0, x0 + tab_w, y1], fill=ORANGE)
    tab_layer.putalpha(Image.composite(tab_layer.split()[3], Image.new("L", (S, S), 0), mask))
    img = Image.alpha_composite(img, tab_layer)
    d = ImageDraw.Draw(img)

    col_x0 = x0 + tab_w + round(box * (2 / REF))
    col_x1 = (x1 - border_w) - round(box * (3 / REF))
    col_y0 = (y0 + border_w) + round(box * (3 / REF))
    col_y1 = (y1 - border_w) - round(box * (3 / REF))
    bar_h = max(1, round(box * (2 / REF)))
    widths = [1.0, 0.7, 0.4]
    gap = (col_y1 - col_y0 - bar_h) / (len(widths) - 1)
    for i, w in enumerate(widths):
        by0 = round(col_y0 + i * gap)
        by1 = by0 + bar_h
        bx1 = col_x0 + round((col_x1 - col_x0) * w)
        d.rectangle([col_x0, by0, bx1, by1], fill=INK)

    img = img.resize((size, size), Image.LANCZOS)
    return img


def save_png(img, path):
    img.save(path)
    print("wrote", path, img.size)


def make_ico(sizes, path):
    imgs = [draw_mark(s) for s in sizes]
    imgs[0].save(path, format="ICO", sizes=[(s, s) for s in sizes])
    print("wrote", path, sizes)


def make_og_image(path):
    W, H = 1200, 630
    img = Image.new("RGBA", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    mark = draw_mark(120)
    mark_x = 140
    mark_y = 140
    img.alpha_composite(mark, (mark_x, mark_y))

    try:
        f_word = ImageFont.truetype(ARIAL_BOLD, 92)
        f_tld = ImageFont.truetype(ARIAL, 72)
        f_tag = ImageFont.truetype(ARIAL, 36)
    except Exception:
        f_word = f_tld = f_tag = ImageFont.load_default()

    word = "Webconvert"
    d.text((mark_x, mark_y + 150), word, font=f_word, fill=INK)
    bbox = d.textbbox((mark_x, mark_y + 150), word, font=f_word)
    d.text((bbox[2] + 6, mark_y + 150 + 18), ".fr", font=f_tld, fill=(122, 113, 105, 255))

    tagline = "Convertisseur d'images gratuit, 100% dans votre navigateur"
    d.text((mark_x, mark_y + 260), tagline, font=f_tag, fill=(61, 56, 51, 255))

    line1 = "JPG · PNG · WebP · AVIF · GIF"
    line2 = "BMP · ICO · SVG · TIFF · HEIC"
    d.text((mark_x, mark_y + 330), line1, font=f_tag, fill=RUST)
    d.text((mark_x, mark_y + 330 + 52), line2, font=f_tag, fill=RUST)

    img.convert("RGB").save(path, quality=90)
    print("wrote", path, img.size)


if __name__ == "__main__":
    save_png(draw_mark(512, pad_ratio=0.06), os.path.join(ASSETS, "logo-square.png"))
    save_png(draw_mark(180, pad_ratio=0.08), os.path.join(ICONS, "apple-touch-icon.png"))
    save_png(draw_mark(192, pad_ratio=0.06), os.path.join(ICONS, "android-chrome-192x192.png"))
    save_png(draw_mark(512, pad_ratio=0.06), os.path.join(ICONS, "android-chrome-512x512.png"))
    save_png(draw_mark(32), os.path.join(ICONS, "favicon-32x32.png"))
    save_png(draw_mark(16), os.path.join(ICONS, "favicon-16x16.png"))
    make_ico([16, 32, 48], os.path.join(ICONS, "favicon.ico"))
    make_og_image(os.path.join(ASSETS, "og-image.jpg"))
