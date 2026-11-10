"""Generate Rakib Download Manager's browser extension icons from its brand mark.

Requires Pillow (pip install Pillow). The source is vector-drawn at 4x resolution so the
small toolbar sizes remain crisp; no upstream artwork is reused.
"""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "extension" / "icons"
MASTER = 1024
SIZES = (16, 32, 48, 128)


def gradient(size, top, bottom):
    image = Image.new("RGBA", (size, size))
    px = image.load()
    for y in range(size):
        t = y / max(1, size - 1)
        color = tuple(round(top[i] * (1 - t) + bottom[i] * t) for i in range(3)) + (255,)
        for x in range(size):
            px[x, y] = color
    return image


def build():
    n = MASTER
    image = gradient(n, (17, 31, 56), (7, 17, 31))
    mask = Image.new("L", (n, n), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((24, 24, 1000, 1000), radius=226, fill=255)
    image.putalpha(mask)

    glow = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((180, 156, 844, 820), outline=(0, 201, 183, 34), width=54)
    image = Image.alpha_composite(image, glow)

    ring = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ring)
    rd.ellipse((220, 196, 804, 780), outline=(20, 190, 174, 255), width=34)
    image = Image.alpha_composite(image, ring)

    arrow = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    ad = ImageDraw.Draw(arrow)
    ad.rounded_rectangle((462, 260, 562, 566), radius=48, fill=(244, 251, 255, 255))
    ad.polygon([(292, 470), (360, 402), (512, 554), (664, 402), (732, 470),
                (546, 656), (478, 656)], fill=(244, 251, 255, 255))
    image = Image.alpha_composite(image, arrow)

    tray = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    td = ImageDraw.Draw(tray)
    td.polygon([(250, 730), (774, 730), (730, 846), (676, 884), (348, 884), (294, 846)],
               fill=(14, 184, 166, 255))
    td.line((372, 770, 652, 770), fill=(9, 35, 56, 140), width=22)
    image = Image.alpha_composite(image, tray)

    OUT.mkdir(parents=True, exist_ok=True)
    for size in SIZES:
        image.resize((size, size), Image.Resampling.LANCZOS).save(OUT / f"icon-{size}.png", optimize=True)
    print("Generated Rakib extension icons:", ", ".join(map(str, SIZES)))


if __name__ == "__main__":
    build()
