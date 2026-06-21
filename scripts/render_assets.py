#!/usr/bin/env python3
"""Generate the README demo GIF and the GitHub social preview image.

Both assets are rendered programmatically so they stay reproducible and easy to
tweak. Run with::

    python3 scripts/render_assets.py
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SOCIAL = ASSETS / "social-preview.png"
DEMO = ASSETS / "demo.gif"

# Palette -------------------------------------------------------------------
BG_TOP = (9, 12, 22)
BG_BOTTOM = (16, 22, 40)
PANEL = (17, 24, 40)
PANEL_2 = (24, 33, 53)
CHROME = (30, 41, 64)
BORDER = (46, 61, 92)
INK = (236, 243, 255)
MUTED = (150, 166, 188)
FAINT = (104, 120, 144)
GREEN = (87, 226, 158)
CYAN = (96, 209, 252)
YELLOW = (255, 207, 112)
RED = (255, 105, 114)
BLUE = (123, 145, 255)
PURPLE = (199, 134, 255)


def font(size: int, *, bold: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont:
    if mono:
        candidates = [
            "/System/Library/Fonts/Menlo.ttc",
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
            if bold
            else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        ]
    elif bold:
        candidates = [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]
    else:
        candidates = [
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]

    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def lerp(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))  # type: ignore[return-value]


def vertical_gradient(size: tuple[int, int], top: tuple[int, int, int], bottom: tuple[int, int, int]) -> Image.Image:
    width, height = size
    base = Image.new("RGB", size, top)
    draw = ImageDraw.Draw(base)
    for y in range(height):
        draw.line((0, y, width, y), fill=lerp(top, bottom, y / max(1, height - 1)))
    return base


def glow(img: Image.Image, center: tuple[int, int], radius: int, color: tuple[int, int, int], strength: float = 0.35) -> None:
    """Additively blend a soft radial glow onto ``img`` (screen-like)."""
    from PIL import ImageChops, ImageFilter

    cx, cy = center
    overlay = Image.new("RGB", img.size, (0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    tint = tuple(int(c * strength) for c in color)
    odraw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=tint)
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius // 3))
    img.paste(ImageChops.add(img, overlay), (0, 0))


def text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], value: str, fill: tuple[int, int, int], size: int, *, bold: bool = False, mono: bool = False) -> None:
    draw.text(xy, value, fill=fill, font=font(size, bold=bold, mono=mono))


def traffic_lights(draw: ImageDraw.ImageDraw, x: int, y: int, r: int = 7, gap: int = 22) -> None:
    for i, color in enumerate((RED, YELLOW, GREEN)):
        cx = x + i * gap
        draw.ellipse((cx, y, cx + 2 * r, y + 2 * r), fill=color)


def address_bar(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], url: str, *, secure: bool = True) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=(y2 - y1) // 2, fill=(13, 19, 33), outline=BORDER, width=1)
    pad = (y2 - y1) // 2
    lock_color = GREEN if secure else FAINT
    # tiny padlock glyph
    lx, ly = x1 + pad, (y1 + y2) // 2
    draw.rounded_rectangle((lx, ly - 1, lx + 9, ly + 7), radius=2, fill=lock_color)
    draw.arc((lx + 1, ly - 7, lx + 8, ly + 2), start=180, end=360, fill=lock_color, width=2)
    text(draw, (lx + 22, y1 + (y2 - y1 - 18) // 2), url, INK, 17, mono=True)


def chrome_window(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], *, title_url: str, radius: int = 18) -> tuple[int, int, int, int]:
    """Draw a browser-style window and return the inner content box."""
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=radius, fill=PANEL, outline=BORDER, width=1)
    bar_h = 50
    draw.rounded_rectangle((x1, y1, x2, y1 + bar_h + radius), radius=radius, fill=CHROME)
    draw.rectangle((x1, y1 + radius, x2, y1 + bar_h), fill=CHROME)
    traffic_lights(draw, x1 + 20, y1 + 18)
    address_bar(draw, (x1 + 96, y1 + 12, x2 - 24, y1 + bar_h - 12), title_url)
    draw.line((x1, y1 + bar_h, x2, y1 + bar_h), fill=(12, 17, 29), width=1)
    return (x1, y1 + bar_h, x2, y2)


def render_terminal_line(draw: ImageDraw.ImageDraw, pos: tuple[int, int], line: str, size: int) -> int:
    """Render one terminal line with light syntax accents. Returns x-end."""
    x, y = pos
    f = font(size, mono=True)
    fb = font(size, mono=True, bold=True)

    if line.startswith("$ "):
        draw.text((x, y), "$", font=fb, fill=GREEN)
        x += draw.textlength("$ ", font=fb)
        rest = line[2:]
        # highlight the leading command word
        head, _, tail = rest.partition(" ")
        draw.text((x, y), head, font=fb, fill=CYAN)
        x += draw.textlength(head, font=fb)
        if tail:
            draw.text((x, y), " " + tail, font=f, fill=INK)
            x += draw.textlength(" " + tail, font=f)
        return int(x)

    if line.startswith("OK"):
        draw.text((x, y), "OK", font=fb, fill=GREEN)
        x += draw.textlength("OK", font=fb)
        draw.text((x, y), line[2:], font=f, fill=INK)
        return int(x + draw.textlength(line[2:], font=f))

    color = MUTED if line.startswith("#") else INK
    draw.text((x, y), line, font=f, fill=color)
    return int(x + draw.textlength(line, font=f))


# ---------------------------------------------------------------------------
# Social preview
# ---------------------------------------------------------------------------
def render_social() -> None:
    img = vertical_gradient((1280, 640), BG_TOP, BG_BOTTOM)
    glow(img, (250, 140), 360, BLUE, 0.20)
    glow(img, (1080, 540), 380, GREEN, 0.16)
    draw = ImageDraw.Draw(img)

    # outer card
    draw.rounded_rectangle((48, 48, 1232, 592), radius=30, fill=(13, 19, 33), outline=BORDER, width=1)

    # left column ------------------------------------------------------------
    text(draw, (88, 92), "modenaf360/gotty-docker", CYAN, 26, bold=True)
    text(draw, (84, 150), "GoTTY Docker", INK, 72, bold=True)
    text(draw, (90, 256), "Run a real terminal in your browser.", MUTED, 32)
    text(draw, (90, 308), "Ubuntu 26.04  ·  GoTTY v1.8.0", GREEN, 28, bold=True)
    text(draw, (90, 348), "Basic Auth, secured by default", CYAN, 26, bold=True)

    pills = [
        ("docker run", BLUE),
        ("compose ready", GREEN),
        ("tmux sharing", PURPLE),
        ("TLS samples", YELLOW),
        ("amd64 · arm64", CYAN),
    ]
    x = 90
    y = 412
    for label, color in pills:
        pad = 15
        w = int(draw.textlength(label, font=font(20, bold=True))) + pad * 2
        if x + w > 660:
            x = 90
            y += 56
        draw.rounded_rectangle((x, y, x + w, y + 44), radius=22, fill=(24, 34, 55), outline=color, width=2)
        text(draw, (x + pad, y + 11), label, color, 20, bold=True)
        x += w + 16

    text(draw, (90, 556), "github.com/hyeonsangjeon/gotty-docker", FAINT, 22, mono=True)

    # right column: browser window ------------------------------------------
    inner = chrome_window(draw, (688, 150, 1184, 506), title_url="localhost:8989", radius=20)
    ix1, iy1, ix2, iy2 = inner
    lines = [
        "$ docker run -p 8989:8080 \\",
        "    -e GOTTY_USER=gotty \\",
        "    -e GOTTY_PASSWORD=*** \\",
        "    modenaf360/gotty-docker",
        "",
        "OK  serving on http://localhost:8989",
        "$ tmux new -A -s gotty",
    ]
    ty = iy1 + 26
    for line in lines:
        render_terminal_line(draw, (ix1 + 26, ty), line, 19)
        ty += 30
    # blinking cursor block on last line
    cursor_x = ix1 + 26 + int(draw.textlength("$ tmux new -A -s gotty ", font=font(19, mono=True)))
    draw.rectangle((cursor_x, ty - 30, cursor_x + 12, ty - 8), fill=GREEN)

    img.save(SOCIAL)


# ---------------------------------------------------------------------------
# Demo GIF
# ---------------------------------------------------------------------------
DEMO_SIZE = (1000, 600)
BADGES = [("Basic Auth", GREEN), ("tmux sharing", PURPLE), ("TLS samples", YELLOW)]

# GIF palette tuning. Seeding the adaptive palette with full brand swatches
# guarantees small accents (e.g. the red/yellow traffic lights) are preserved.
GIF_COLORS = 128
SWATCH_W, SWATCH_H = 70, 60
PALETTE_SWATCHES = [RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, INK, MUTED, FAINT, BG_TOP, BG_BOTTOM, PANEL, CHROME, BORDER]


def demo_base() -> tuple[Image.Image, tuple[int, int, int, int]]:
    img = vertical_gradient(DEMO_SIZE, BG_TOP, BG_BOTTOM)
    glow(img, (200, 120), 300, BLUE, 0.16)
    glow(img, (840, 540), 320, GREEN, 0.12)
    draw = ImageDraw.Draw(img)

    text(draw, (44, 30), "GoTTY Docker", INK, 34, bold=True)
    text(draw, (46, 76), "A real Linux terminal in your browser — auth-first.", MUTED, 19)

    inner = chrome_window(draw, (44, 120, 956, 506), title_url="localhost:8989", radius=18)

    # footer badges
    bx = 44
    by = 524
    for label, color in BADGES:
        pad = 14
        w = int(draw.textlength(label, font=font(17, bold=True))) + pad * 2
        draw.rounded_rectangle((bx, by, bx + w, by + 38), radius=19, fill=(22, 31, 50), outline=color, width=2)
        text(draw, (bx + pad, by + 9), label, color, 17, bold=True)
        bx += w + 14
    return img, inner


# Build the static background once; every frame is a cheap copy of it.
_DEMO_BASE: Image.Image | None = None
_DEMO_INNER: tuple[int, int, int, int] | None = None


def _demo_canvas() -> tuple[Image.Image, tuple[int, int, int, int]]:
    global _DEMO_BASE, _DEMO_INNER
    if _DEMO_BASE is None:
        _DEMO_BASE, _DEMO_INNER = demo_base()
    assert _DEMO_INNER is not None
    return _DEMO_BASE.copy(), _DEMO_INNER


def demo_frame(visible: list[str], cursor: bool, *, browser_ready: bool = False) -> Image.Image:
    img, inner = _demo_canvas()
    draw = ImageDraw.Draw(img)
    ix1, iy1, ix2, iy2 = inner

    y = iy1 + 28
    for line in visible:
        render_terminal_line(draw, (ix1 + 26, y), line, 20)
        y += 34

    if browser_ready:
        # success banner inside the terminal
        draw.rounded_rectangle((ix1 + 24, y + 6, ix2 - 24, y + 52), radius=12, fill=(18, 40, 32), outline=GREEN, width=1)
        text(draw, (ix1 + 40, y + 17), "✓  Protected shell is live — open the URL and log in.", GREEN, 19, mono=True)

    if cursor and visible:
        cf = font(20, mono=True)
        cx = ix1 + 26 + int(draw.textlength(visible[-1], font=cf)) + 4
        draw.rectangle((cx, y - 34 + 2, cx + 11, y - 34 + 24), fill=GREEN)
    return img


def render_demo() -> None:
    script = [
        "$ docker run -p 8989:8080 \\",
        "    -e GOTTY_USER=gotty \\",
        "    -e GOTTY_PASSWORD='strong-password' \\",
        "    modenaf360/gotty-docker",
        "OK  GoTTY serving on http://localhost:8989",
        "$ tmux new -A -s gotty",
    ]

    frames: list[Image.Image] = []
    durations: list[int] = []

    def push(img: Image.Image, ms: int) -> None:
        frames.append(img)
        durations.append(ms)

    visible: list[str] = []
    for line in script:
        visible.append("")
        step = max(2, len(line) // 14)
        for idx in range(step, len(line) + step, step):
            visible[-1] = line[:idx]
            push(demo_frame(visible.copy(), True), 45)
        # brief pause with a blink at end of the line
        push(demo_frame(visible.copy(), True), 220)
        push(demo_frame(visible.copy(), False), 160)

    # success scene with a couple of cursor blinks
    for i in range(6):
        push(demo_frame(visible.copy(), i % 2 == 0, browser_ready=True), 360)

    # Quantize every frame against one shared palette so the GIF stays small
    # and free of per-frame palette flicker. Seed the palette with the brand
    # swatches so small but important accents (red/yellow traffic lights,
    # cursor) survive quantization.
    seed = frames[-1].copy()
    sdraw = ImageDraw.Draw(seed)
    for i, color in enumerate(PALETTE_SWATCHES):
        sdraw.rectangle((i * SWATCH_W, 0, i * SWATCH_W + SWATCH_W - 1, SWATCH_H - 1), fill=color)
    palette_src = seed.convert("P", palette=Image.Palette.ADAPTIVE, colors=GIF_COLORS)
    quantized = [f.quantize(palette=palette_src, dither=Image.Dither.NONE) for f in frames]

    quantized[0].save(
        DEMO,
        save_all=True,
        append_images=quantized[1:],
        duration=durations,
        loop=0,
        optimize=True,
        disposal=1,
    )


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    render_social()
    render_demo()
    print(SOCIAL)
    print(DEMO)


if __name__ == "__main__":
    main()
