"""One-off asset generator: favicons, OG image, logo-square, in the "Pierre"
palette (see css/styles.css). The mark is the one drawn in CSS in the site
header (.brand__mark): a dark rounded square with a stone-coloured square
outline inside. Run once when the brand changes, not part of the shipped site.
"""
from PIL import Image, ImageDraw, ImageFont
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS = os.path.join(ROOT, "assets")
ICONS = os.path.join(ASSETS, "icons")
os.makedirs(ICONS, exist_ok=True)

INK = (35, 34, 31, 255)        # --ink   #23221f
STONE = (231, 228, 221, 255)   # --bg    #e7e4dd
WIN = (251, 250, 248, 255)     # --win   #fbfaf8
LINE = (220, 216, 207, 255)    # --line  #dcd8cf
MUTED = (93, 90, 83, 255)      # --muted #5d5a53
OK = (47, 107, 59, 255)        # --ok    #2f6b3b

ARIAL_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
ARIAL = "/System/Library/Fonts/Supplemental/Arial.ttf"


def draw_mark(size, bg=None, pad_ratio=0.0):
    """Same proportions as .brand__mark (26px box, 8px radius, inner square
    inset 7px with a 2px outline and 3px radius)."""
    S = size * 4
    pad = int(S * pad_ratio)
    box = S - pad * 2
    img = Image.new("RGBA", (S, S), bg if bg else (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    REF = 26.0
    u = box / REF
    x0, y0, x1, y1 = pad, pad, pad + box, pad + box
    d.rounded_rectangle([x0, y0, x1, y1], radius=round(8 * u), fill=INK)
    inset = 7 * u
    d.rounded_rectangle([x0 + inset, y0 + inset, x1 - inset, y1 - inset], radius=round(3 * u),
                        outline=STONE, width=max(2, round(2 * u)))
    return img.resize((size, size), Image.LANCZOS)


def save_png(img, path):
    img.save(path)
    print("wrote", path, img.size)


def make_ico(sizes, path):
    imgs = [draw_mark(s) for s in sizes]
    imgs[0].save(path, format="ICO", sizes=[(s, s) for s in sizes])
    print("wrote", path, sizes)


def make_og_image(path):
    W, H = 1200, 630
    img = Image.new("RGBA", (W, H), STONE)
    d = ImageDraw.Draw(img)

    try:
        f_word = ImageFont.truetype(ARIAL_BOLD, 84)
        f_tag = ImageFont.truetype(ARIAL, 36)
        f_chip = ImageFont.truetype(ARIAL_BOLD, 23)
    except Exception:
        f_word = f_tag = f_chip = ImageFont.load_default()

    x = 120
    mark = draw_mark(96)
    img.alpha_composite(mark, (x, 150))
    d.text((x + 124, 150 + 4), "Webconvert", font=f_word, fill=INK)

    d.text((x, 300), "Convertisseur d'images gratuit,", font=f_tag, fill=MUTED)
    d.text((x, 348), "100 % dans votre navigateur", font=f_tag, fill=MUTED)

    cx, cy = x, 440
    for name in ["JPG", "PNG", "WebP", "AVIF", "GIF", "BMP", "ICO", "SVG", "TIFF", "HEIC"]:
        tw = d.textlength(name, font=f_chip)
        w = int(tw + 34)
        d.rounded_rectangle([cx, cy, cx + w, cy + 48], radius=24, fill=WIN, outline=LINE, width=2)
        d.text((cx + 17, cy + 11), name, font=f_chip, fill=INK)
        cx += w + 10

    img.convert("RGB").save(path, quality=90)
    print("wrote", path, img.size)


if __name__ == "__main__":
    save_png(draw_mark(512, pad_ratio=0.06), os.path.join(ASSETS, "logo-square.png"))
    save_png(draw_mark(180, bg=STONE, pad_ratio=0.16), os.path.join(ICONS, "apple-touch-icon.png"))
    save_png(draw_mark(192, pad_ratio=0.06), os.path.join(ICONS, "android-chrome-192x192.png"))
    save_png(draw_mark(512, pad_ratio=0.06), os.path.join(ICONS, "android-chrome-512x512.png"))
    save_png(draw_mark(32), os.path.join(ICONS, "favicon-32x32.png"))
    save_png(draw_mark(16), os.path.join(ICONS, "favicon-16x16.png"))
    make_ico([16, 32, 48], os.path.join(ICONS, "favicon.ico"))
    make_og_image(os.path.join(ASSETS, "og-image.jpg"))
