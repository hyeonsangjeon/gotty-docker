#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SOCIAL = ASSETS / "social-preview.png"
DEMO = ASSETS / "demo.gif"

BG = (10, 14, 24)
PANEL = (20, 28, 45)
PANEL_2 = (27, 38, 59)
INK = (238, 245, 255)
MUTED = (145, 161, 181)
GREEN = (77, 224, 151)
CYAN = (85, 205, 252)
YELLOW = (255, 204, 102)
RED = (255, 94, 104)
BLUE = (118, 139, 255)
PURPLE = (203, 128, 255)


def font(size: int, bold: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont:
    candidates = []
    if mono:
        candidates.extend(
            [
                "/System/Library/Fonts/Menlo.ttc",
                "/System/Library/Fonts/Supplemental/Courier New.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
            ]
        )
    elif bold:
        candidates.extend(
            [
                "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                "/System/Library/Fonts/Supplemental/Helvetica Bold.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            ]
        )
    else:
        candidates.extend(
            [
                "/System/Library/Fonts/Supplemental/Arial.ttf",
                "/System/Library/Fonts/Supplemental/Helvetica.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            ]
        )

    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)

    return ImageFont.load_default()


def rounded(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill: tuple[int, int, int], radius: int = 18) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], value: str, fill: tuple[int, int, int], size: int, *, bold: bool = False, mono: bool = False) -> None:
    draw.text(xy, value, fill=fill, font=font(size, bold=bold, mono=mono))


def terminal_window(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], lines: Iterable[tuple[str, tuple[int, int, int]]]) -> None:
    x1, y1, x2, y2 = box
    rounded(draw, box, PANEL, 20)
    draw.rounded_rectangle((x1, y1, x2, y1 + 46), radius=20, fill=PANEL_2)
    draw.rectangle((x1, y1 + 26, x2, y1 + 46), fill=PANEL_2)

    for i, color in enumerate([RED, YELLOW, GREEN]):
        draw.ellipse((x1 + 20 + i * 24, y1 + 16, x1 + 32 + i * 24, y1 + 28), fill=color)

    text(draw, (x1 + 105, y1 + 12), "gotty-docker / authenticated shell", MUTED, 16, mono=True)

    y = y1 + 72
    for line, color in lines:
        text(draw, (x1 + 26, y), line, color, 21, mono=True)
        y += 32


def render_social() -> None:
    img = Image.new("RGB", (1280, 640), BG)
    draw = ImageDraw.Draw(img)

    for offset, color in [(0, BLUE), (24, CYAN), (48, GREEN)]:
        draw.line((0, 610 - offset, 1280, 510 - offset), fill=color, width=3)

    rounded(draw, (56, 56, 1224, 584), (14, 20, 34), 28)
    draw.rectangle((56, 56, 1224, 114), fill=(18, 26, 43))

    text(draw, (88, 88), "modenaf360/gotty-docker", CYAN, 28, bold=True)
    text(draw, (88, 164), "GoTTY Docker", INK, 86, bold=True)
    text(draw, (92, 270), "Share a real terminal in the browser.", MUTED, 34)
    text(draw, (92, 318), "Ubuntu 26.04 + GoTTY v1.8.0", GREEN, 30, bold=True)
    text(draw, (92, 356), "Basic Auth out of the box", CYAN, 27, bold=True)

    pills = [
        ("docker run", BLUE),
        ("compose ready", GREEN),
        ("tmux sharing", PURPLE),
        ("TLS samples", YELLOW),
    ]
    for idx, (label, color) in enumerate(pills):
        row = idx // 2
        col = idx % 2
        x = 92 + col * 230
        y = 420 + row * 58
        width = int(draw.textlength(label, font=font(22, bold=True))) + 34
        draw.rounded_rectangle((x, y, x + width, y + 46), radius=23, fill=(26, 37, 58), outline=color, width=2)
        text(draw, (x + 17, y + 10), label, color, 22, bold=True)

    terminal_lines = [
        ("$ docker run -p 8989:8080 \\", CYAN),
        ("  -e GOTTY_USER=gotty \\", INK),
        ("  -e GOTTY_PASSWORD='***' \\", INK),
        ("  modenaf360/gotty-docker", INK),
        ("GoTTY is serving a protected shell", GREEN),
    ]
    terminal_window(draw, (690, 158, 1168, 476), terminal_lines)

    text(draw, (92, 530), "github.com/hyeonsangjeon/gotty-docker", MUTED, 24, mono=True)
    img.save(SOCIAL)


def demo_frame(typed_lines: list[str], footer: str, cursor: bool) -> Image.Image:
    img = Image.new("RGB", (960, 540), BG)
    draw = ImageDraw.Draw(img)

    text(draw, (42, 34), "GoTTY Docker", INK, 38, bold=True)
    text(draw, (44, 82), "A browser terminal container with auth-first examples", MUTED, 20)
    terminal_window(draw, (44, 126, 916, 450), [])

    y = 198
    for i, line in enumerate(typed_lines):
        color = GREEN if line.startswith("OK") else CYAN if line.startswith("$") else INK
        text(draw, (78, y), line, color, 22, mono=True)
        y += 34

    if cursor:
        draw.rectangle((78 + int(draw.textlength(typed_lines[-1], font=font(22, mono=True))) + 3, y - 30, 92 + int(draw.textlength(typed_lines[-1], font=font(22, mono=True))) + 3, y - 7), fill=GREEN)

    draw.rounded_rectangle((44, 474, 916, 508), radius=17, fill=(21, 31, 49))
    text(draw, (66, 480), footer, MUTED, 17)
    return img


def render_demo() -> None:
    script = [
        "$ docker run -p 8989:8080 \\",
        "  -e GOTTY_USER=gotty \\",
        "  -e GOTTY_PASSWORD='strong-password' \\",
        "  modenaf360/gotty-docker",
        "OK  Open http://localhost:8989",
        "$ gotty@container:~$ tmux new -A -s gotty",
    ]
    frames: list[Image.Image] = []
    visible: list[str] = []

    for line in script:
        visible.append("")
        step = max(3, len(line) // 10)
        for idx in range(step, len(line) + step, step):
            visible[-1] = line[:idx]
            frames.append(demo_frame(visible.copy(), "Basic Auth, read-only views, tmux sharing, random URLs, and TLS samples included.", True))
        frames.extend([demo_frame(visible.copy(), "Basic Auth, read-only views, tmux sharing, random URLs, and TLS samples included.", False)] * 3)

    frames.extend([demo_frame(visible.copy(), "Star the repo if this saves you from wiring a web terminal again.", i % 2 == 0) for i in range(12)])
    frames[0].save(DEMO, save_all=True, append_images=frames[1:], duration=90, loop=0, optimize=True)


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    render_social()
    render_demo()
    print(SOCIAL)
    print(DEMO)


if __name__ == "__main__":
    main()
