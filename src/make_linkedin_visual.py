from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


WIDTH = 1600
HEIGHT = 1600

INK = "#F6F1E8"
MUTED = "#9D968B"
SUBTLE = "#5B554E"
PANEL = "#12100E"
PANEL_2 = "#181512"
BAYERN = "#E3062C"
PSG = "#2D5CA8"
GOLD = "#D3AE5F"
LINE = "#332C25"


def typeface(size: int, kind: str = "body") -> ImageFont.FreeTypeFont:
    if kind == "serif":
        return ImageFont.truetype("/System/Library/Fonts/NewYork.ttf", size)
    if kind == "mono":
        return ImageFont.truetype("/System/Library/Fonts/SFNSMono.ttf", size)
    return ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", size)


def pct(value: float, digits: int = 1) -> str:
    return f"{value * 100:.{digits}f}%"


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def blend(a: str, b: str, t: float) -> tuple[int, int, int]:
    ar, ag, ab = hex_to_rgb(a)
    br, bg, bb = hex_to_rgb(b)
    return (
        int(ar + (br - ar) * t),
        int(ag + (bg - ag) * t),
        int(ab + (bb - ab) * t),
    )


def background() -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), "#080706")
    px = img.load()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            nx = x / WIDTH
            ny = y / HEIGHT
            radial_red = math.exp(-((nx - 0.18) ** 2 + (ny - 0.22) ** 2) / 0.035)
            radial_blue = math.exp(-((nx - 0.86) ** 2 + (ny - 0.18) ** 2) / 0.045)
            warmth = math.exp(-((nx - 0.50) ** 2 + (ny - 0.90) ** 2) / 0.10)
            r = 8 + int(34 * radial_red + 10 * warmth)
            g = 7 + int(6 * radial_red + 8 * radial_blue + 8 * warmth)
            b = 6 + int(12 * radial_blue + 3 * warmth)
            px[x, y] = (r, g, b)

    rng = random.Random(42)
    noise = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    npx = noise.load()
    for _ in range(45000):
        x = rng.randrange(WIDTH)
        y = rng.randrange(HEIGHT)
        alpha = rng.randrange(5, 14)
        npx[x, y] = (255, 244, 220, alpha)
    return Image.alpha_composite(img.convert("RGBA"), noise)


def panel(draw: ImageDraw.ImageDraw, canvas: Image.Image, box: tuple[int, int, int, int], radius: int = 34) -> None:
    x1, y1, x2, y2 = box
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((x1 + 10, y1 + 18, x2 + 10, y2 + 18), radius=radius, fill=(0, 0, 0, 95))
    shadow = shadow.filter(ImageFilter.GaussianBlur(22))
    canvas.alpha_composite(shadow)
    draw.rounded_rectangle(box, radius=radius, fill=PANEL, outline="#2A231C", width=2)
    draw.rounded_rectangle((x1 + 8, y1 + 8, x2 - 8, y2 - 8), radius=radius - 8, outline="#221D17", width=1)


def text_right(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fill: str, font: ImageFont.FreeTypeFont) -> None:
    bbox = draw.textbbox((0, 0), text, font=font)
    draw.text((xy[0] - (bbox[2] - bbox[0]), xy[1]), text, fill=fill, font=font)


def progress_split(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], left: float) -> None:
    x1, y1, x2, y2 = box
    w = x2 - x1
    h = y2 - y1
    draw.rounded_rectangle(box, radius=h // 2, fill="#252019")
    mid = x1 + int(w * left)
    draw.rounded_rectangle((x1, y1, mid, y2), radius=h // 2, fill=BAYERN)
    draw.rounded_rectangle((mid - h // 2, y1, x2, y2), radius=h // 2, fill=PSG)
    draw.line((mid, y1 - 10, mid, y2 + 10), fill=INK, width=2)


def make_visual(results_path: Path, output_path: Path) -> None:
    results = json.loads(results_path.read_text())
    img = background()
    draw = ImageDraw.Draw(img)

    # top system marks
    draw.text((74, 68), "MONTE CARLO / SECOND LEG", fill=GOLD, font=typeface(22, "mono"))
    text_right(draw, (1526, 68), "BAYERN vs PSG", INK, typeface(22, "mono"))
    draw.line((74, 116, 1526, 116), fill=LINE, width=2)

    # Hero title
    draw.text((74, 160), "Remontada,", fill=INK, font=typeface(104, "serif"))
    draw.text((74, 270), "with receipts.", fill=INK, font=typeface(104, "serif"))
    draw.text(
        (82, 400),
        "Scenario-weighted Monte Carlo built from UCL xG,\nfirst-leg context, lineups, fatigue states\nand tactical priors.",
        fill=MUTED,
        font=typeface(27),
        spacing=8,
    )

    q = results["qualification"]
    bq = q["bayern"]
    pq = q["psg"]

    # Qualification hero panel
    panel(draw, img, (850, 162, 1526, 535), 38)
    draw.text((900, 215), "Qualification edge", fill=MUTED, font=typeface(24, "mono"))
    draw.text((900, 270), pct(bq), fill=INK, font=typeface(76))
    draw.text((1168, 305), "Bayern", fill=BAYERN, font=typeface(36))
    draw.text((900, 398), pct(pq), fill=INK, font=typeface(46))
    draw.text((1082, 425), "PSG", fill=PSG, font=typeface(29))
    progress_split(draw, (900, 475, 1476, 506), bq)

    # Path panel
    panel(draw, img, (74, 610, 723, 1030), 34)
    draw.text((122, 660), "Tie path after 90", fill=INK, font=typeface(38, "serif"))
    path_items = [
        ("Bayern qualify", results["score_buckets"]["bayern_by_2_plus"], BAYERN),
        ("Extra time", results["score_buckets"]["bayern_by_1_extra_time"], GOLD),
        ("PSG survive", results["score_buckets"]["psg_advance_in_90"], PSG),
    ]
    max_path = max(v for _, v, _ in path_items)
    for idx, (label, value, color) in enumerate(path_items):
        y = 745 + idx * 90
        draw.text((122, y), label, fill=MUTED, font=typeface(24))
        draw.rounded_rectangle((318, y + 2, 600, y + 28), radius=13, fill="#2A241D")
        draw.rounded_rectangle((318, y + 2, 318 + int(282 * value / max_path), y + 28), radius=13, fill=color)
        text_right(draw, (658, y - 6), pct(value), INK, typeface(28, "mono"))

    # Scores panel
    panel(draw, img, (790, 610, 1526, 1030), 34)
    draw.text((840, 660), "Most common scorelines", fill=INK, font=typeface(38, "serif"))
    scores = results["scorelines"][:5]
    max_score = max(item["probability"] for item in scores)
    for idx, item in enumerate(scores):
        y = 742 + idx * 58
        draw.text((842, y - 10), item["score"], fill=INK, font=typeface(33, "mono"))
        draw.rounded_rectangle((946, y, 1334, y + 24), radius=12, fill="#2A241D")
        draw.rounded_rectangle((946, y, 946 + int(388 * item["probability"] / max_score), y + 24), radius=12, fill=blend(BAYERN, PSG, idx / 5))
        draw.text((1360, y - 8), pct(item["probability"]), fill=MUTED, font=typeface(25, "mono"))

    # Scenario strip
    draw.text((74, 1102), "Assumption pressure points", fill=INK, font=typeface(40, "serif"))
    conditional = results["conditional_bayern_qualification"]
    scenario_items = [
        ("Davies present", conditional["davies"]["Davies"], "recovery pace"),
        ("No Davies", conditional["davies"]["No_Davies"], "transition risk"),
        ("Fatigue shows", conditional["fatigue"]["shows_after_60"], "late PSG legs"),
        ("Fatigue masked", conditional["fatigue"]["masked_until_ET"], "adrenaline branch"),
    ]
    for idx, (label, value, sub) in enumerate(scenario_items):
        x = 74 + idx * 370
        panel(draw, img, (x, 1170, x + 326, 1380), 28)
        draw.text((x + 28, 1204), label, fill=INK, font=typeface(28))
        draw.text((x + 28, 1240), sub.upper(), fill=MUTED, font=typeface(16, "mono"))
        draw.text((x + 28, 1292), pct(value), fill=BAYERN if value >= 0.5 else PSG, font=typeface(48, "serif"))
        draw.line((x + 28, 1346, x + 298, 1346), fill=LINE, width=2)
        marker = x + 28 + int(270 * value)
        draw.ellipse((marker - 7, 1339, marker + 7, 1353), fill=BAYERN if value >= 0.5 else PSG)
        draw.text((x + 28, 1358), "0", fill=SUBTLE, font=typeface(13, "mono"))
        text_right(draw, (x + 298, 1358), "100", SUBTLE, typeface(13, "mono"))

    # Footer metrics
    projections = results["projections"]
    draw.line((74, 1448, 1526, 1448), fill=LINE, width=2)
    metrics = [
        ("modal", results["metadata"]["modal_score"]),
        ("value pick", results["metadata"]["best_value_score"]),
        ("avg goals", f"{projections['average_goals']:.2f}"),
        ("BTTS", pct(projections["both_teams_score"])),
    ]
    for idx, (label, value) in enumerate(metrics):
        x = 78 + idx * 360
        draw.text((x, 1480), label.upper(), fill=MUTED, font=typeface(16, "mono"))
        draw.text((x, 1510), value, fill=INK, font=typeface(31 if idx != 1 else 28))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(output_path, quality=96)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a LinkedIn-ready premium simulation visual.")
    parser.add_argument("--results", default="outputs/results.json")
    parser.add_argument("--output", default="outputs/linkedin_results.png")
    args = parser.parse_args()
    make_visual(Path(args.results), Path(args.output))
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
