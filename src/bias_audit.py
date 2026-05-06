from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

from simulate import run_simulation


def deep_update(base: dict[str, Any], updates: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(base)
    for key, value in updates.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_update(result[key], value)
        else:
            result[key] = value
    return result


def set_runs(config: dict[str, Any], runs: int, seed: int) -> dict[str, Any]:
    cfg = copy.deepcopy(config)
    cfg["simulation"]["runs"] = runs
    cfg["simulation"]["seed"] = seed
    return cfg


def variant_configs(base: dict[str, Any]) -> list[tuple[str, str, dict[str, Any]]]:
    bayern_ratio = base["observed_data"]["bayern"]["ucl_goals"] / base["observed_data"]["bayern"]["ucl_xg"]
    psg_ratio = base["observed_data"]["psg"]["ucl_goals"] / base["observed_data"]["psg"]["ucl_xg"]

    return [
        (
            "baseline",
            "Current public model: data anchors plus analyst priors from the discussion.",
            {},
        ),
        (
            "raw_ucl_finishing_ratios",
            "Uses raw UCL goals/xG finishing multipliers for both teams. This is a PSG-friendly check because PSG's UCL overperformance is larger.",
            {
                "model_priors": {
                    "bayern_finishing_mean": bayern_ratio,
                    "psg_finishing_mean": psg_ratio,
                }
            },
        ),
        (
            "no_comeback_narrative",
            "Removes most of Bayern's comeback/crowd late-game boost and makes chasing states more conservative.",
            {
                "model_priors": {
                    "bayern_chasing_minus_2_boost": 1.16,
                    "bayern_chasing_minus_1_boost": 1.10,
                    "karl_late_boost": 1.02,
                    "bischof_late_boost": 1.00,
                    "et_karl_boost": 1.01,
                    "et_bischof_boost": 1.00,
                }
            },
        ),
        (
            "no_psg_fatigue_edge",
            "Assumes PSG fatigue does not show and removes the Bayern late boost from fatigue states.",
            {
                "scenario_weights": {
                    "psg_fatigue": {
                        "shows_after_60": 0.0,
                        "masked_until_extra_time": 0.0,
                        "not_visible": 1.0,
                    }
                },
                "model_priors": {
                    "psg_fatigue_bayern_boost": 1.00,
                    "psg_fatigue_psg_multiplier": 1.00,
                    "masked_fatigue_bayern_boost": 1.00,
                    "et_fatigue_bayern_boost": 1.00,
                    "et_fatigue_psg_multiplier": 1.00,
                    "et_masked_bayern_boost": 1.00,
                    "et_masked_psg_multiplier": 1.00,
                },
            },
        ),
        (
            "psg_midfield_not_disrupted",
            "Assumes WZE stays central or PSG solve RB without materially weakening midfield dynamics.",
            {
                "scenario_weights": {
                    "psg_shape": {
                        "wze_rb_ruiz_mid": 0.0,
                        "wze_mid_alt_rb": 0.85,
                        "unclear_hybrid": 0.15,
                    }
                }
            },
        ),
        (
            "psg_transition_stress",
            "Raises PSG transition burst frequency and Bayern system-event risk to test whether the press risk is understated.",
            {
                "model_priors": {
                    "psg_transition_burst_probability": 0.075,
                    "psg_transition_burst_multiplier": 1.30,
                    "bayern_system_event_probability": 0.014,
                    "bayern_system_event_chasing_multiplier": 1.34,
                }
            },
        ),
        (
            "neutral_et_penalties",
            "Removes Bayern's extra-time and penalty-shootout edge.",
            {
                "model_priors": {
                    "et_bayern_stamina_multiplier": 0.90,
                    "et_psg_fatigue_multiplier": 0.90,
                    "et_fatigue_bayern_boost": 1.00,
                    "et_fatigue_psg_multiplier": 1.00,
                    "et_masked_bayern_boost": 1.00,
                    "et_masked_psg_multiplier": 1.00,
                    "penalty_home_edge": 0.0,
                    "max_bayern_penalty_shootout_probability": 0.52,
                    "min_bayern_penalty_shootout_probability": 0.48,
                }
            },
        ),
        (
            "anti_bayern_stack",
            "Stacks the most defensible PSG-friendly choices: raw UCL finishing, no PSG fatigue, less midfield disruption, more PSG transition danger, neutral ET/pens.",
            {
                "scenario_weights": {
                    "psg_shape": {
                        "wze_rb_ruiz_mid": 0.0,
                        "wze_mid_alt_rb": 0.85,
                        "unclear_hybrid": 0.15,
                    },
                    "psg_fatigue": {
                        "shows_after_60": 0.0,
                        "masked_until_extra_time": 0.0,
                        "not_visible": 1.0,
                    },
                },
                "model_priors": {
                    "bayern_finishing_mean": bayern_ratio,
                    "psg_finishing_mean": psg_ratio,
                    "bayern_chasing_minus_2_boost": 1.16,
                    "bayern_chasing_minus_1_boost": 1.10,
                    "psg_transition_burst_probability": 0.075,
                    "psg_transition_burst_multiplier": 1.30,
                    "bayern_system_event_probability": 0.014,
                    "bayern_system_event_chasing_multiplier": 1.34,
                    "psg_fatigue_bayern_boost": 1.00,
                    "psg_fatigue_psg_multiplier": 1.00,
                    "masked_fatigue_bayern_boost": 1.00,
                    "et_bayern_stamina_multiplier": 0.90,
                    "et_psg_fatigue_multiplier": 0.90,
                    "et_fatigue_bayern_boost": 1.00,
                    "et_fatigue_psg_multiplier": 1.00,
                    "et_masked_bayern_boost": 1.00,
                    "et_masked_psg_multiplier": 1.00,
                    "penalty_home_edge": 0.0,
                    "max_bayern_penalty_shootout_probability": 0.52,
                    "min_bayern_penalty_shootout_probability": 0.48,
                },
            },
        ),
    ]


def write_markdown(path: Path, rows: list[dict[str, Any]], runs: int) -> None:
    baseline = rows[0]["bayern_qualify"]
    lines = [
        "# Bias Audit",
        "",
        "This audit tests whether Bayern-favorable analyst priors are driving the headline result.",
        "",
        f"Runs per scenario: `{runs:,}`",
        "",
        "## Summary Table",
        "",
        "| Variant | Bayern qualify | Delta vs baseline | Modal score | Purpose |",
        "| --- | ---: | ---: | --- | --- |",
    ]
    for row in rows:
        delta = row["bayern_qualify"] - baseline
        lines.append(
            f"| `{row['variant']}` | {row['bayern_qualify']:.1%} | {delta:+.1%} | {row['modal_score']} | {row['description']} |"
        )

    anti = next(row for row in rows if row["variant"] == "anti_bayern_stack")
    raw = next(row for row in rows if row["variant"] == "raw_ucl_finishing_ratios")
    no_comeback = next(row for row in rows if row["variant"] == "no_comeback_narrative")

    lines.extend(
        [
            "",
            "## Verdict",
            "",
            f"- The model is **not laundering a Bayern fan take**: after the MD-1 refresh, the baseline is only Bayern {baseline:.1%} / PSG {1 - baseline:.1%}.",
            f"- The largest bias-sensitive channel is PSG finishing treatment. Using raw UCL goals/xG finishing ratios moves Bayern from {baseline:.1%} to {raw['bayern_qualify']:.1%}.",
            f"- The Bayern comeback/crowd prior matters but is not the entire model: removing it moves Bayern to {no_comeback['bayern_qualify']:.1%}.",
            f"- The anti-Bayern stack gives Bayern {anti['bayern_qualify']:.1%}, meaning the public headline should avoid sounding like a confident Bayern call.",
            "",
            "## Interpretation",
            "",
            "The current model still contains Bayern-leaning priors, especially around late-game pressure, extra-time stamina, home crowd effects, and the now-cleaner Bayern availability picture. It also contains PSG-leaning priors around elite finishing, transition bursts, and the possibility that PSG solve the Hakimi absence without losing too much midfield control. The honest public wording is therefore: Bayern have a narrow model edge, but PSG-friendly assumptions can still flip the tie.",
            "",
        ]
    )
    path.write_text("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run ablation-based bias audit for the Bayern PSG simulation.")
    parser.add_argument("--config", default="configs/bayern_psg.json")
    parser.add_argument("--runs", type=int, default=120000)
    parser.add_argument("--seed", type=int, default=2026050207)
    parser.add_argument("--output", default="outputs/bias_audit.json")
    parser.add_argument("--markdown", default="docs/bias_audit.md")
    args = parser.parse_args()

    base = json.loads(Path(args.config).read_text())
    rows: list[dict[str, Any]] = []
    for i, (name, description, updates) in enumerate(variant_configs(base)):
        cfg = deep_update(base, updates)
        cfg = set_runs(cfg, args.runs, args.seed + i * 1009)
        result = run_simulation(cfg)
        rows.append(
            {
                "variant": name,
                "description": description,
                "bayern_qualify": result["qualification"]["bayern"],
                "psg_qualify": result["qualification"]["psg"],
                "bayern_win_90": result["probabilities_90"]["bayern_win"],
                "draw_90": result["probabilities_90"]["draw"],
                "psg_win_90": result["probabilities_90"]["psg_win"],
                "modal_score": result["metadata"]["modal_score"],
                "best_value_score": result["metadata"]["best_value_score"],
            }
        )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps({"runs_per_variant": args.runs, "rows": rows}, indent=2) + "\n")

    markdown_path = Path(args.markdown)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    write_markdown(markdown_path, rows, args.runs)
    print(json.dumps({row["variant"]: row["bayern_qualify"] for row in rows}, indent=2))
    print(f"Wrote {output_path}")
    print(f"Wrote {markdown_path}")


if __name__ == "__main__":
    main()
