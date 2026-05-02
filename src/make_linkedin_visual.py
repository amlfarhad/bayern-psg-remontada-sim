from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


W = 1600
H = 2000
SCALE = 2

CANVAS = "#0B0A08"
PAPER = "#F5EFE4"
MUTED = "#91887C"
SUBTLE = "#5F574F"
FAINT = "#2C261F"
RED = "#E3062C"
BLUE = "#3267B1"
GOLD = "#CBAA5E"


def f(size: int, face: str = "sans") -> ImageFont.FreeTypeFont:
    size *= SCALE
    if face == "serif":
        return ImageFont.truetype("/System/Library/Fonts/NewYork.ttf", size)
    if face == "mono":
        return ImageFont.truetype("/System/Library/Fonts/SFNSMono.ttf", size)
    return ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", size)


def pct(x: float) -> str:
    return f"{x * 100:.1f}%"


def sx(v: float) -> int:
    return int(v * SCALE)


def box(draw: ImageDraw.ImageDraw, xy: tuple[float, float, float, float], outline: str = FAINT, width: int = 1) -> None:
    draw.rounded_rectangle(tuple(sx(v) for v in xy), radius=sx(2), outline=outline, width=sx(width))


def line(draw: ImageDraw.ImageDraw, xy: tuple[float, float, float, float], fill: str = FAINT, width: float = 1) -> None:
    draw.line(tuple(sx(v) for v in xy), fill=fill, width=max(1, sx(width)))


def text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    value: str,
    fill: str = PAPER,
    size: int = 28,
    face: str = "sans",
    anchor: str | None = None,
    spacing: int = 4,
) -> None:
    draw.text((sx(xy[0]), sx(xy[1])), value, fill=fill, font=f(size, face), anchor=anchor, spacing=sx(spacing))


def right_text(draw: ImageDraw.ImageDraw, x: float, y: float, value: str, fill: str, size: int, face: str = "sans") -> None:
    text(draw, (x, y), value, fill=fill, size=size, face=face, anchor="ra")


def make_bg() -> Image.Image:
    img = Image.new("RGBA", (W * SCALE, H * SCALE), CANVAS)
    draw = ImageDraw.Draw(img)

    # Subtle floodlight glow. Built as blurred ellipses, not decorative blobs.
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((sx(-260), sx(-180), sx(760), sx(860)), fill=(120, 0, 8, 82))
    gd.ellipse((sx(1040), sx(-120), sx(1900), sx(780)), fill=(15, 60, 120, 68))
    gd.ellipse((sx(280), sx(1230), sx(1440), sx(2360)), fill=(115, 80, 25, 38))
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(sx(90))))

    # Pitch geometry as quiet structure.
    for y in range(300, 1800, 165):
        line(draw, (96, y, 1504, y), fill="#17130F", width=1)
    for x in range(160, 1500, 165):
        line(draw, (x, 250, x, 1810), fill="#15110E", width=1)
    line(draw, (800, 255, 800, 1810), fill="#251F19", width=1.2)
    draw.ellipse((sx(585), sx(785), sx(1015), sx(1215)), outline="#211B15", width=sx(2))
    draw.arc((sx(628), sx(828), sx(972), sx(1172)), 205, 335, fill="#332A20", width=sx(3))
    draw.arc((sx(628), sx(828), sx(972), sx(1172)), 25, 155, fill="#263852", width=sx(3))

    rng = random.Random(4)
    px = img.load()
    for _ in range(35000):
        x = rng.randrange(W * SCALE)
        y = rng.randrange(H * SCALE)
        r, g, b, a = px[x, y]
        n = rng.randrange(5, 17)
        px[x, y] = (min(255, r + n), min(255, g + n), min(255, b + n), min(255, a + rng.randrange(6, 13)))
    return img


def dot(draw: ImageDraw.ImageDraw, x: float, y: float, r: float, fill: str, outline: str | None = None) -> None:
    draw.ellipse((sx(x - r), sx(y - r), sx(x + r), sx(y + r)), fill=fill, outline=outline, width=sx(1) if outline else 1)


def make_visual(results_path: Path, output_path: Path) -> None:
    results = json.loads(results_path.read_text())
    img = make_bg()
    draw = ImageDraw.Draw(img)

    bq = results["qualification"]["bayern"]
    pq = results["qualification"]["psg"]
    buckets = results["score_buckets"]
    projections = results["projections"]
    scores = results["scorelines"][:6]
    conditional = results["conditional_bayern_qualification"]

    # Header.
    text(draw, (96, 82), "SIMULATION DOSSIER", fill=GOLD, size=18, face="mono")
    text(draw, (96, 122), "BAYERN / PSG · SECOND LEG", fill=MUTED, size=18, face="mono")
    right_text(draw, 1504, 82, "300,000 MONTE CARLO RUNS", fill=GOLD, size=18, face="mono")
    right_text(draw, 1504, 122, "SCENARIO-WEIGHTED · GAME-STATE DEPENDENT", fill=MUTED, size=18, face="mono")
    line(draw, (96, 178, 1504, 178), fill="#322920", width=1)

    # Main headline.
    text(draw, (96, 252), "Remontada", fill=PAPER, size=132, face="serif")
    text(draw, (104, 402), "with receipts.", fill=PAPER, size=86, face="serif")
    text(
        draw,
        (104, 532),
        "A football-biased model, now forced to show its workings:\nUCL xG, first-leg context, fatigue branches, lineup uncertainty,\nand tactical priors audited against PSG-friendly assumptions.",
        fill=MUTED,
        size=25,
        spacing=10,
    )

    # Qualification axis, no dashboard card.
    line(draw, (900, 300, 1504, 300), fill="#3B3026", width=2)
    mid = 900 + 604 * bq
    line(draw, (900, 300, mid, 300), fill=RED, width=8)
    line(draw, (mid, 300, 1504, 300), fill=BLUE, width=8)
    dot(draw, mid, 300, 11, PAPER)
    text(draw, (900, 204), "QUALIFICATION EDGE", fill=MUTED, size=20, face="mono")
    text(draw, (900, 232), pct(bq), fill=PAPER, size=70)
    text(draw, (1190, 258), "Bayern", fill=RED, size=31)
    text(draw, (900, 350), pct(pq), fill=PAPER, size=42)
    text(draw, (1068, 365), "PSG", fill=BLUE, size=25)
    right_text(draw, 1504, 350, f"Bayern +{(bq - pq) * 100:.1f}pp", fill=GOLD, size=22, face="mono")

    # 90 minute route map.
    text(draw, (96, 775), "The 90-minute fork", fill=PAPER, size=50, face="serif")
    line(draw, (96, 858, 1504, 858), fill="#302820", width=1)
    routes = [
        ("Bayern\nin 90", buckets["bayern_by_2_plus"], RED),
        ("Extra\ntime", buckets["bayern_by_1_extra_time"], GOLD),
        ("PSG\nin 90", buckets["psg_advance_in_90"], BLUE),
    ]
    route_x = [260, 800, 1340]
    for x, (label, value, color) in zip(route_x, routes):
        dot(draw, x, 858, 12, color)
        line(draw, (x, 858, x, 1024), fill=color, width=2)
        text(draw, (x, 1060), pct(value), fill=PAPER, size=58, anchor="ma")
        text(draw, (x, 1142), label, fill=MUTED, size=24, anchor="ma", spacing=5)

    # Scoreline distribution: row plot, not a dashboard bar chart.
    text(draw, (96, 1270), "Scoreline cloud", fill=PAPER, size=46, face="serif")
    text(draw, (96, 1326), "Most common regulation outcomes", fill=MUTED, size=21, face="mono")
    x0, x1 = 250, 760
    y_axis = 1730
    line(draw, (x0, y_axis, x1, y_axis), fill="#352C23", width=1)
    for tick, label in [(0.04, "4%"), (0.05, "5%"), (0.06, "6%")]:
        tx = x0 + (tick - 0.035) / 0.035 * (x1 - x0)
        line(draw, (tx, y_axis - 12, tx, y_axis + 12), fill="#352C23", width=1)
        text(draw, (tx, y_axis + 30), label, fill=SUBTLE, size=15, face="mono", anchor="ma")
    for idx, item in enumerate(scores):
        prob = item["probability"]
        x = x0 + (prob - 0.035) / 0.035 * (x1 - x0)
        y = 1398 + idx * 54
        line(draw, (x0, y, x1, y), fill="#17120E", width=1)
        color = RED if idx < 3 else BLUE if item["score"].endswith("-3") else GOLD
        text(draw, (96, y - 22), item["score"], fill=PAPER, size=28, face="mono")
        dot(draw, x, y, 14 if idx == 0 else 10, color, outline="#1B1510")
        text(draw, (x + 26, y - 16), pct(prob), fill=MUTED, size=18, face="mono")

    # Assumption sensitivity.
    text(draw, (900, 1270), "Bias audit snapshot", fill=PAPER, size=46, face="serif")
    text(draw, (900, 1326), "Bayern qualify under selected ablations", fill=MUTED, size=21, face="mono")
    audit_path = results_path.parent / "bias_audit.json"
    audit_values: list[tuple[str, float]] = []
    if audit_path.exists():
        audit = json.loads(audit_path.read_text())
        keep = ["baseline", "raw_ucl_finishing_ratios", "no_comeback_narrative", "anti_bayern_stack"]
        names = {
            "baseline": "baseline",
            "raw_ucl_finishing_ratios": "raw UCL finishing",
            "no_comeback_narrative": "no comeback prior",
            "anti_bayern_stack": "PSG-friendly stack",
        }
        for row in audit["rows"]:
            if row["variant"] in keep:
                audit_values.append((names[row["variant"]], row["bayern_qualify"]))
    else:
        audit_values = [
            ("baseline", bq),
            ("Davies present", conditional["davies"]["Davies"]),
            ("No Davies", conditional["davies"]["No_Davies"]),
            ("fatigue shows", conditional["fatigue"]["shows_after_60"]),
        ]
    ax0, ax1 = 900, 1504
    ay0 = 1730
    line(draw, (ax0, ay0, ax1, ay0), fill="#352C23", width=1)
    for value, label in [(0.4, "40"), (0.5, "50"), (0.6, "60")]:
        tx = ax0 + (value - 0.4) / 0.2 * (ax1 - ax0)
        line(draw, (tx, ay0 - 18, tx, ay0 + 18), fill="#352C23", width=1)
        text(draw, (tx, ay0 + 32), label, fill=SUBTLE, size=15, face="mono", anchor="ma")
    for idx, (label, value) in enumerate(audit_values):
        y = 1405 + idx * 74
        x = ax0 + (value - 0.4) / 0.2 * (ax1 - ax0)
        line(draw, (ax0, y, ax1, y), fill="#19130F", width=1)
        dot(draw, x, y, 12, RED if value >= 0.5 else BLUE)
        text(draw, (ax0, y - 32), label.upper(), fill=MUTED, size=15, face="mono")
        text(draw, (x + 28, y - 18), pct(value), fill=PAPER, size=22, face="mono")

    # Footer metrics.
    line(draw, (96, 1840, 1504, 1840), fill="#302820", width=1)
    footer = [
        ("modal", results["metadata"]["modal_score"]),
        ("value pick", results["metadata"]["best_value_score"]),
        ("avg goals", f"{projections['average_goals']:.2f}"),
        ("BTTS", pct(projections["both_teams_score"])),
    ]
    for i, (label, value) in enumerate(footer):
        x = 96 + i * 360
        text(draw, (x, 1886), label.upper(), fill=MUTED, size=17, face="mono")
        text(draw, (x, 1930), value, fill=PAPER, size=31)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img = img.resize((W, H), Image.Resampling.LANCZOS).convert("RGB")
    img.save(output_path, quality=96)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a premium LinkedIn-ready simulation poster.")
    parser.add_argument("--results", default="outputs/results.json")
    parser.add_argument("--output", default="outputs/linkedin_results_premium.png")
    args = parser.parse_args()
    make_visual(Path(args.results), Path(args.output))
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
