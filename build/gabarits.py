# -*- coding: utf-8 -*-
"""Downloadable templates: one transparent PNG per platform page that has
risk zones, drawn from the same zone definitions as the crop preview
(data.PLATFORM_PAGES[*]["zones"]), at the page's exact output size.

Meant to be placed as the top layer in Canva, Photoshop, Figma… then hidden
before export. Requires Pillow; run by hand when zones change:
    cd build && python3 gabarits.py
Output: assets/gabarits/<slug>.png (committed, served as static files).
"""
import os
from PIL import Image, ImageDraw, ImageFont

from data import PLATFORM_PAGES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "gabarits")
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"
ORANGE = (201, 82, 28)


def rgb(hex_color):
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def shape_mask(size, z, W, H):
    m = Image.new("L", size, 0)
    d = ImageDraw.Draw(m)
    box = (z["x"] * W, z["y"] * H, (z["x"] + z["w"]) * W, (z["y"] + z["h"]) * H)
    (d.ellipse if z.get("shape") == "circle" else d.rectangle)(box, fill=255)
    return m, box


def hatch_layer(size, step):
    layer = Image.new("RGBA", size, (*ORANGE, 46))
    d = ImageDraw.Draw(layer)
    W, H = size
    for x in range(-H, W, step):
        d.line([(x, H), (x + H, 0)], fill=(*ORANGE, 150), width=max(2, step // 5))
    return layer


def label(d, xy, text, fs, color, anchor="la"):
    font = ImageFont.truetype(FONT_BOLD, fs)
    x0, y0, x1, y1 = d.textbbox(xy, text, font=font, anchor=anchor)
    pad = fs * 0.45
    d.rounded_rectangle((x0 - pad, y0 - pad * 0.7, x1 + pad, y1 + pad * 0.7), radius=fs * 0.3, fill=(*color, 235))
    d.text(xy, text, font=font, fill=(255, 255, 255, 255), anchor=anchor)


def draw(page):
    W, H = page["width"], page["height"]
    size = (W, H)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    fs = max(16, round(min(W, H * 4) * 0.014))
    lw = max(3, round(fs * 0.18))
    gap = fs * 0.8
    # Shading first, outlines and labels on top.
    for z in page["zones"]:
        if z["type"] == "frame" and z.get("shade") == "outside":
            m, _ = shape_mask(size, z, W, H)
            dark = Image.new("RGBA", size, (20, 18, 16, 120))
            dark.putalpha(Image.eval(m, lambda v: 0 if v else 120))
            img = Image.alpha_composite(img, dark)
        elif z["type"] == "cover":
            m, _ = shape_mask(size, z, W, H)
            h = hatch_layer(size, max(10, fs))
            h.putalpha(Image.composite(h.getchannel("A"), Image.new("L", size, 0), m))
            img = Image.alpha_composite(img, h)
    d = ImageDraw.Draw(img)
    for z in page["zones"]:
        color = rgb(z.get("color", "#c9521c"))
        if z["type"] == "label":
            label(d, (z["x"] * W + gap, z["y"] * H + gap), z["label"], fs, color)
            continue
        _, box = shape_mask(size, z, W, H)
        if z.get("shape") == "circle":
            d.ellipse(box, outline=(*color, 255), width=lw)
        else:
            d.rectangle(box, outline=(*color, 255), width=lw)
        text = z["label"] + (" · indicatif" if z["type"] == "cover" and not z.get("official") else "")
        x, y = box[0] + gap, box[1] + gap
        if z.get("label_pos") == "above":
            y = box[1] - gap - fs
        elif z.get("label_pos") == "below":
            y = box[3] + gap
        x = min(max(x, gap), W - gap)
        y = min(max(y, gap), H - gap - fs)
        label(d, (x, y), text, fs, color)
    # Footer: size and reminder, bottom right.
    small = ImageFont.truetype(FONT, max(12, round(fs * 0.7)))
    note = (f"Gabarit {W} × {H} px · webconvert.fr · masquez ce calque avant d'exporter" if W >= 800
            else f"{W} × {H} px · webconvert.fr")
    d.text((W - gap, H - gap), note, font=small, fill=(255, 255, 255, 230), anchor="rd",
           stroke_width=max(1, lw // 2), stroke_fill=(20, 18, 16, 200))
    return img


def main():
    os.makedirs(OUT, exist_ok=True)
    for page in PLATFORM_PAGES:
        if not page.get("zones") or page["width"] == page["height"]:
            continue
        slug = page["path"].strip("/")
        path = os.path.join(OUT, f"gabarit-{slug}.png")
        draw(page).save(path, optimize=True)
        print(f"{path}  {os.path.getsize(path) // 1024} Ko")


if __name__ == "__main__":
    main()
