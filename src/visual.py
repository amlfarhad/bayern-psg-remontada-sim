from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/bayern_psg_mpl")
os.environ.setdefault("XDG_CACHE_HOME", "/tmp/bayern_psg_xdg")

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import FuncFormatter


BG = "#F7F4EE"
INK = "#1F1D1B"
MUTED = "#6F6860"
GRID = "#DDD5C9"
BAYERN = "#D90429"
PSG = "#2451A6"
GOLD = "#B88A2A"


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def pct_axis(x: float, _pos: int) -> str:
    return f"{x * 100:.0f}%"


def remove_spines(ax) -> None:
    for spine in ax.spines.values():
        spine.set_visible(False)


def style_axis(ax) -> None:
    ax.set_facecolor(BG)
    ax.tick_params(colors=MUTED, labelsize=9, length=0)
    remove_spines(ax)


def add_panel_label(ax, label: str, title: str) -> None:
    ax.text(0, 1.12, title, transform=ax.transAxes, ha="left", va="bottom", fontsize=13, color=INK, fontweight="bold")


def load_audit(results_path: Path) -> list[tuple[str, float]]:
    audit_path = results_path.parent / "bias_audit.json"
    if not audit_path.exists():
        return []
    audit = json.loads(audit_path.read_text())
    labels = {
        "baseline": "Baseline",
        "raw_ucl_finishing_ratios": "PSG finishing heater holds",
        "no_comeback_narrative": "Remove Bayern comeback bump",
        "anti_bayern_stack": "PSG-friendly stack",
    }
    order = list(labels)
    values = {row["variant"]: row["bayern_qualify"] for row in audit["rows"]}
    return [(labels[key], values[key]) for key in order if key in values]


def make_visual(results_path: Path, output_path: Path) -> None:
    results = json.loads(results_path.read_text())
    q = results["qualification"]
    buckets = results["score_buckets"]
    projections = results["projections"]
    scores = results["scorelines"][:7]
    audit_rows = load_audit(results_path)

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "figure.facecolor": BG,
            "axes.facecolor": BG,
            "savefig.facecolor": BG,
            "text.color": INK,
            "axes.labelcolor": MUTED,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "axes.titleweight": "bold",
        }
    )

    fig = plt.figure(figsize=(13.5, 10.5), dpi=180)
    gs = GridSpec(
        4,
        2,
        figure=fig,
        height_ratios=[0.85, 1.2, 1.35, 0.55],
        hspace=0.88,
        wspace=0.50,
        left=0.075,
        right=0.965,
        top=0.88,
        bottom=0.10,
    )

    fig.text(0.075, 0.955, "Bayern vs PSG second leg: model output", fontsize=22, fontweight="bold", color=INK)
    fig.text(
        0.075,
        0.925,
        "Scenario-weighted Monte Carlo · 300,000 runs",
        fontsize=10.5,
        color=MUTED,
    )

    # Panel A: qualification probability.
    ax0 = fig.add_subplot(gs[0, :])
    style_axis(ax0)
    add_panel_label(ax0, "A", "Qualification probability")
    ax0.set_xlim(0, 1)
    ax0.set_ylim(-0.55, 0.55)
    ax0.axvline(0.5, color=INK, lw=1.1, alpha=0.75)
    ax0.barh([0.16], [q["bayern"]], height=0.20, color=BAYERN, left=0)
    ax0.barh([-0.16], [q["psg"]], height=0.20, color=PSG, left=0)
    ax0.text(q["bayern"] + 0.012, 0.16, f"Bayern {pct(q['bayern'])}", va="center", ha="left", fontsize=14, fontweight="bold", color=INK)
    ax0.text(q["psg"] + 0.012, -0.16, f"PSG {pct(q['psg'])}", va="center", ha="left", fontsize=14, fontweight="bold", color=INK)
    ax0.text(0.5, -0.46, "50/50", va="center", ha="center", fontsize=9, color=MUTED)
    ax0.set_yticks([])
    ax0.xaxis.set_major_formatter(FuncFormatter(pct_axis))
    ax0.set_xticks([0, 0.25, 0.5, 0.75, 1])
    ax0.grid(axis="x", color=GRID, lw=0.8)

    # Panel B: 90-minute tie path.
    ax1 = fig.add_subplot(gs[1, 0])
    style_axis(ax1)
    add_panel_label(ax1, "B", "Tie state after regulation")
    path_labels = ["Bayern overturn it in 90", "Bayern win by one: ET", "PSG survive regulation"]
    path_values = [buckets["bayern_by_2_plus"], buckets["bayern_by_1_extra_time"], buckets["psg_advance_in_90"]]
    path_colors = [BAYERN, GOLD, PSG]
    y_pos = list(range(len(path_labels)))[::-1]
    ax1.barh(y_pos, path_values, color=path_colors, height=0.42)
    for y, value in zip(y_pos, path_values):
        ax1.text(value + 0.012, y, pct(value), va="center", ha="left", fontsize=11, fontweight="bold")
    ax1.set_yticks(y_pos, path_labels)
    ax1.set_xlim(0, 0.46)
    ax1.xaxis.set_major_formatter(FuncFormatter(pct_axis))
    ax1.set_xticks([0, 0.1, 0.2, 0.3, 0.4])
    ax1.grid(axis="x", color=GRID, lw=0.8)

    # Panel C: scoreline distribution.
    ax2 = fig.add_subplot(gs[1, 1])
    style_axis(ax2)
    add_panel_label(ax2, "C", "Most common regulation scorelines")
    score_labels = [s["score"] for s in scores][::-1]
    score_values = [s["probability"] for s in scores][::-1]
    score_colors = [BAYERN if label in {"3-2", "3-1", "2-1"} else GOLD if label in {"2-2", "4-2"} else PSG for label in score_labels]
    ax2.scatter(score_values, range(len(score_labels)), s=110, c=score_colors, zorder=3)
    for i, (label, value) in enumerate(zip(score_labels, score_values)):
        ax2.plot([0.035, value], [i, i], color=GRID, lw=1.0, zorder=1)
        ax2.text(value + 0.0015, i, pct(value), va="center", ha="left", fontsize=9.5, color=MUTED)
    ax2.set_yticks(range(len(score_labels)), score_labels)
    ax2.set_xlim(0.035, 0.068)
    ax2.xaxis.set_major_formatter(FuncFormatter(pct_axis))
    ax2.set_xticks([0.04, 0.05, 0.06])
    ax2.grid(axis="x", color=GRID, lw=0.8)

    # Panel D: bias audit.
    ax3 = fig.add_subplot(gs[2, 0])
    style_axis(ax3)
    add_panel_label(ax3, "D", "Bias audit")
    if audit_rows:
        labels = [row[0] for row in audit_rows][::-1]
        values = [row[1] for row in audit_rows][::-1]
        colors = [BAYERN if value >= 0.5 else PSG for value in values]
        ax3.axvline(0.5, color=INK, lw=1.1, alpha=0.75)
        ax3.scatter(values, range(len(labels)), s=120, c=colors, zorder=3)
        for i, value in enumerate(values):
            ax3.plot([0.4, value], [i, i], color=GRID, lw=1.0, zorder=1)
            ax3.text(value + 0.004, i, pct(value), va="center", ha="left", fontsize=9.5)
        ax3.set_yticks(range(len(labels)), labels)
    ax3.set_xlim(0.4, 0.6)
    ax3.xaxis.set_major_formatter(FuncFormatter(pct_axis))
    ax3.set_xticks([0.4, 0.45, 0.5, 0.55, 0.6])
    ax3.grid(axis="x", color=GRID, lw=0.8)

    # Panel E: scenario sensitivities.
    ax4 = fig.add_subplot(gs[2, 1])
    style_axis(ax4)
    add_panel_label(ax4, "E", "Key football scenarios")
    cond = results["conditional_bayern_qualification"]
    scenario_rows = [
        ("Davies recovery pace holds", cond["davies"]["Davies"]),
        ("No Davies recovery outlet", cond["davies"]["No_Davies"]),
        ("PSG fade late like first leg", cond["fatigue"]["shows_after_60"]),
        ("PSG adrenaline masks fatigue", cond["fatigue"]["masked_until_ET"]),
    ]
    scen_labels = [row[0] for row in scenario_rows][::-1]
    scen_values = [row[1] for row in scenario_rows][::-1]
    scen_colors = [BAYERN if value >= 0.5 else PSG for value in scen_values]
    ax4.axvline(0.5, color=INK, lw=1.1, alpha=0.75)
    ax4.scatter(scen_values, range(len(scen_labels)), s=120, c=scen_colors, zorder=3)
    for i, value in enumerate(scen_values):
        ax4.plot([0.4, value], [i, i], color=GRID, lw=1.0, zorder=1)
        ax4.text(value + 0.004, i, pct(value), va="center", ha="left", fontsize=9.5)
    ax4.set_yticks(range(len(scen_labels)), scen_labels)
    ax4.set_xlim(0.4, 0.6)
    ax4.xaxis.set_major_formatter(FuncFormatter(pct_axis))
    ax4.set_xticks([0.4, 0.45, 0.5, 0.55])
    ax4.grid(axis="x", color=GRID, lw=0.8)

    # Footer outputs.
    ax5 = fig.add_subplot(gs[3, :])
    ax5.set_facecolor(BG)
    ax5.axis("off")
    summary = [
        ("Most common score", results["metadata"]["modal_score"]),
        ("Football value pick", results["metadata"]["best_value_score"]),
        ("Average goals", f"{projections['average_goals']:.2f}"),
        ("Both teams score", pct(projections["both_teams_score"])),
    ]
    for i, (label, value) in enumerate(summary):
        x = 0.02 + i * 0.245
        ax5.text(x, 0.66, label.upper(), transform=ax5.transAxes, fontsize=8.5, color=MUTED, fontfamily="DejaVu Sans Mono")
        ax5.text(x, 0.22, value, transform=ax5.transAxes, fontsize=17, color=INK, fontweight="bold")
    ax5.axhline(0.95, color=INK, lw=1.1)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180, bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a polished analyst-style simulation visual.")
    parser.add_argument("--results", default="outputs/results.json")
    parser.add_argument("--output", default="outputs/model_results.png")
    args = parser.parse_args()
    make_visual(Path(args.results), Path(args.output))
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
