#!/usr/bin/env python3
"""Build deterministic Crux brand assets from the Arena-generated source image."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "crux-arena-original.jpg"
ASSETS = ROOT / "assets"
SKILL_ASSETS = ROOT / "skills" / "crux" / "assets"

BACKGROUND = (247, 248, 244)
INK = (23, 33, 38)
TEAL = (15, 118, 110)
CORAL = (228, 87, 61)
MUTED = (82, 96, 97)
WHITE = (255, 255, 255)

FONT_CANDIDATES = (
    Path("/System/Library/Fonts/SFNS.ttf"),
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
)


def font(size: int) -> ImageFont.FreeTypeFont:
    for candidate in FONT_CANDIDATES:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default(size=size)


def clean_mark() -> Image.Image:
    source = Image.open(SOURCE).convert("RGB")
    crop = source.crop((250, 248, 775, 730)).resize((840, 772), Image.Resampling.LANCZOS)

    pixels = crop.load()
    for y in range(crop.height):
        for x in range(crop.width):
            red, green, blue = pixels[x, y]
            if red > 226 and green > 226 and blue > 220:
                pixels[x, y] = WHITE
            elif red > green * 1.18 and red > blue * 1.18:
                pixels[x, y] = CORAL
            elif blue > red * 1.05 or green > red * 1.05:
                pixels[x, y] = TEAL

    crop = ImageEnhance.Contrast(crop).enhance(1.05)
    canvas = Image.new("RGB", (1024, 1024), WHITE)
    canvas.paste(crop, ((1024 - crop.width) // 2, (1024 - crop.height) // 2))
    return canvas


def make_banner(mark: Image.Image) -> Image.Image:
    width, height = 1600, 640
    banner = Image.new("RGB", (width, height), BACKGROUND)
    draw = ImageDraw.Draw(banner)

    draw.rectangle((0, 0, 18, height), fill=TEAL)
    draw.rectangle((18, 0, 24, height), fill=CORAL)

    mark_card = Image.new("RGB", (430, 430), WHITE)
    mark_card.paste(mark.resize((360, 360), Image.Resampling.LANCZOS), (35, 35))
    banner.paste(mark_card, (1100, 105))

    title_font = font(144)
    kicker_font = font(28)
    subtitle_font = font(42)
    label_font = font(24)

    draw.text((112, 100), "OPEN-SOURCE AGENT SKILL + POLICY CORE", font=kicker_font, fill=TEAL)
    draw.text((105, 154), "Crux", font=title_font, fill=INK)
    draw.rectangle((112, 326, 228, 338), fill=CORAL)
    draw.text((112, 372), "Evidence-governed thinking", font=subtitle_font, fill=INK)
    draw.text((112, 430), "for papers, research, and decisions", font=subtitle_font, fill=INK)

    labels = ("FIND THE CRUX", "TEST THE EVIDENCE", "CHOOSE THE NEXT MOVE")
    x = 112
    for label in labels:
        box = draw.textbbox((0, 0), label, font=label_font)
        label_width = box[2] - box[0]
        draw.rounded_rectangle((x, 530, x + label_width + 36, 574), radius=5, fill=WHITE, outline=(217, 223, 218), width=2)
        draw.text((x + 18, 538), label, font=label_font, fill=MUTED)
        x += label_width + 50

    return banner


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    SKILL_ASSETS.mkdir(parents=True, exist_ok=True)

    mark = clean_mark()
    mark.save(ASSETS / "crux-logo-1024.png", optimize=True)
    mark.resize((400, 400), Image.Resampling.LANCZOS).save(
        SKILL_ASSETS / "crux-icon-400.png", optimize=True
    )
    mark.save(SKILL_ASSETS / "crux-logo-1024.png", optimize=True)

    banner = make_banner(mark)
    banner.save(ASSETS / "readme-banner.png", optimize=True)
    ImageOps.fit(banner, (1280, 640), method=Image.Resampling.LANCZOS).save(
        ASSETS / "social-preview.png", optimize=True
    )


if __name__ == "__main__":
    main()
