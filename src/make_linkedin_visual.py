from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH = 1600
HEIGHT = 1600
BG = "#F7F4EF"
TEXT = "#191919"
MUTED = "#6E6A63"
BAYERN = "#DC052D"
PSG = "#21468B"
GOLD = "#C8A45D"
DARK = "#262626"
GRID = "#D9D3C7"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf"
    return ImageFont.truetype(path, size)


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def bar(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, value: float, color: str, label: str) -> None:
    draw.rounded_rectangle((x, y, x + w, y + h), radius=8, fill="#E7E0D3")
    draw.rounded_rectangle((x, y, x + int(w * value), y + h), radius=8, fill=color)
    draw.text((x, y - 42), label, fill=MUTED, font=font(28, True))
    draw.text((x + w + 24, y + h / 2 - 22), pct(value), fill=TEXT, font=font(34, True))


def small_bar(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    w: int,
    h: int,
    value: float,
    max_value: float,
    color: str,
    label: str,
) -> None:
    draw.rounded_rectangle((x, y, x + w, y + h), radius=6, fill="#E7E0D3")
    fill_w = int(w * (value / max_value))
    draw.rounded_rectangle((x, y, x + fill_w, y + h), radius=6, fill=color)
    draw.text((x, y - 5), label, fill=TEXT, font=font(30, True), anchor="ls")
    draw.text((x + fill_w + 14, y + h / 2), pct(value), fill=TEXT, font=font(28, True), anchor="lm")


def make_visual(results_path: Path, output_path: Path) -> None:
    results = json.loads(results_path.read_text())
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)

    title = "Bayern vs PSG second-leg simulation"
    subtitle = "Scenario-weighted Monte Carlo | 300,000 simulated matches | data + analyst priors"
    draw.text((80, 72), title, fill=TEXT, font=font(52, True))
    draw.text((80, 138), subtitle, fill=MUTED, font=font(25))

    q = results["qualification"]
    draw.text((80, 235), "Qualification probability", fill=TEXT, font=font(34, True))
    bar(draw, 80, 330, 520, 58, q["bayern"], BAYERN, "Bayern")
    bar(draw, 80, 455, 520, 58, q["psg"], PSG, "PSG")

    draw.text((820, 235), "Most common 90-minute scores", fill=TEXT, font=font(34, True))
    scores = results["scorelines"][:5]
    max_score = max(item["probability"] for item in scores)
    for i, item in enumerate(scores):
        small_bar(
            draw,
            820,
            330 + i * 95,
            430,
            42,
            item["probability"],
            max_score,
            DARK,
            item["score"],
        )

    draw.text((80, 665), "Tie path after 90 minutes", fill=TEXT, font=font(34, True))
    buckets = results["score_buckets"]
    path_items = [
        ("Bayern in 90", buckets["bayern_by_2_plus"], BAYERN),
        ("Extra time", buckets["bayern_by_1_extra_time"], GOLD),
        ("PSG in 90", buckets["psg_advance_in_90"], PSG),
    ]
    for i, (label, value, color) in enumerate(path_items):
        small_bar(draw, 80, 760 + i * 95, 520, 42, value, 0.45, color, label)

    draw.text((820, 835), "Bayern qualification by scenario", fill=TEXT, font=font(34, True))
    conditional = results["conditional_bayern_qualification"]
    scenario_items = [
        ("Davies present", conditional["davies"]["Davies"]),
        ("No Davies", conditional["davies"]["No_Davies"]),
        ("Fatigue shows", conditional["fatigue"]["shows_after_60"]),
        ("Fatigue masked", conditional["fatigue"]["masked_until_ET"]),
    ]
    draw.line((820, 915, 1250, 915), fill=GRID, width=3)
    draw.text((1035, 882), "50%", fill=MUTED, font=font(22), anchor="mm")
    for i, (label, value) in enumerate(scenario_items):
        y = 965 + i * 85
        draw.text((820, y), label, fill=TEXT, font=font(27, True), anchor="ls")
        start = 1035
        delta = int((value - 0.5) / 0.1 * 210)
        color = BAYERN if value >= 0.5 else PSG
        if delta >= 0:
            draw.rounded_rectangle((start, y - 31, start + delta, y - 1), radius=5, fill=color)
        else:
            draw.rounded_rectangle((start + delta, y - 31, start, y - 1), radius=5, fill=color)
        draw.text((1270, y - 16), pct(value), fill=TEXT, font=font(25, True), anchor="lm")

    projections = results["projections"]
    cards = [
        ("Modal score", results["metadata"]["modal_score"]),
        ("Value pick", results["metadata"]["best_value_score"]),
        ("Average goals", f"{projections['average_goals']:.2f}"),
        ("BTTS", pct(projections["both_teams_score"])),
    ]
    card_w = 330
    for i, (label, value) in enumerate(cards):
        x = 80 + i * 370
        y = 1260
        draw.rounded_rectangle((x, y, x + card_w, y + 155), radius=10, outline="#D6CEC0", width=2, fill="#FBF8F1")
        draw.text((x + 24, y + 28), label.upper(), fill=MUTED, font=font(19, True))
        draw.text((x + 24, y + 78), value, fill=TEXT, font=font(35, True))

    footer = "Code-generated visualization. Source anchors: UCL xG/shots, first-leg xG, lineup/fatigue scenarios, tactical priors."
    draw.text((80, 1510), footer, fill=MUTED, font=font(22))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a LinkedIn-ready simulation result visual.")
    parser.add_argument("--results", default="outputs/results.json")
    parser.add_argument("--output", default="outputs/linkedin_results.png")
    args = parser.parse_args()
    make_visual(Path(args.results), Path(args.output))
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()

