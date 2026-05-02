from __future__ import annotations

import argparse
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median
from typing import Any


BLOCKS = [(0, 15), (15, 30), (30, 45), (45, 60), (60, 75), (75, 90), (90, 96)]


def poisson_sample(rng: random.Random, lam: float) -> int:
    if lam <= 0:
        return 0
    limit = math.exp(-lam)
    k = 0
    p = 1.0
    while p > limit:
        k += 1
        p *= rng.random()
    return k - 1


def weighted_choice(rng: random.Random, weighted: list[tuple[str, float]]) -> str:
    roll = rng.random()
    acc = 0.0
    for name, weight in weighted:
        acc += weight
        if roll <= acc:
            return name
    return weighted[-1][0]


def pct(counter: Counter[str], key: str, runs: int) -> float:
    return counter[key] / runs


def prior(priors: dict[str, Any], key: str, default: float) -> float:
    return float(priors.get(key, default))


def run_simulation(config: dict[str, Any]) -> dict[str, Any]:
    runs = int(config["simulation"]["runs"])
    rng = random.Random(int(config["simulation"]["seed"]))
    first_leg = config["observed_data"]["first_leg"]
    weights = config["scenario_weights"]
    priors = config["model_priors"]

    base_bayern_xg = float(priors["base_bayern_xg"])
    base_psg_xg = float(priors["base_psg_xg"])

    scorelines: Counter[tuple[int, int]] = Counter()
    qualification: Counter[str] = Counter()
    paths: Counter[str] = Counter()
    tags: Counter[str] = Counter()
    first_goal: Counter[str] = Counter()
    scenario_qual: defaultdict[tuple[str, str, str, str], Counter[str]] = defaultdict(Counter)
    total_goals: list[int] = []
    shots: list[tuple[int, int]] = []
    shots_on_target: list[tuple[int, int]] = []

    psg_shape_weights = [
        ("WZE_RB_Ruiz_mid", weights["psg_shape"]["wze_rb_ruiz_mid"]),
        ("WZE_mid_alt_RB", weights["psg_shape"]["wze_mid_alt_rb"]),
        ("unclear_hybrid", weights["psg_shape"]["unclear_hybrid"]),
    ]
    fatigue_weights = [
        ("shows_after_60", weights["psg_fatigue"]["shows_after_60"]),
        ("masked_until_ET", weights["psg_fatigue"]["masked_until_extra_time"]),
        ("not_visible", weights["psg_fatigue"]["not_visible"]),
    ]
    neuer_weights = [
        ("strong", weights["neuer_state"]["strong"]),
        ("normal", weights["neuer_state"]["normal"]),
        ("bad_tail", weights["neuer_state"]["bad_tail"]),
    ]

    for _ in range(runs):
        psg_shape = weighted_choice(rng, psg_shape_weights)
        davies = rng.random() < float(weights["davies_present"])
        fatigue = weighted_choice(rng, fatigue_weights)
        neuer = weighted_choice(rng, neuer_weights)

        tempo = rng.lognormvariate(math.log(1.04), 0.11)
        bayern_finishing = rng.lognormvariate(math.log(float(priors["bayern_finishing_mean"])), 0.10)
        psg_finishing = rng.lognormvariate(math.log(float(priors["psg_finishing_mean"])), 0.12)

        psg_star_tail = weighted_choice(rng, [("hot", 0.34), ("normal", 0.50), ("quiet", 0.16)])
        star_mult = {"hot": 1.16, "normal": 1.00, "quiet": 0.90}[psg_star_tail]

        neuer_mult = {"strong": 0.90, "normal": 1.00, "bad_tail": 1.13}[neuer]
        penalty_neuer = {"strong": 0.545, "normal": 0.525, "bad_tail": 0.495}[neuer]

        if psg_shape == "WZE_RB_Ruiz_mid":
            psg_mid_control = 0.94
            psg_rb_defense = 0.98
            psg_right_pace = 0.88
        elif psg_shape == "WZE_mid_alt_RB":
            psg_mid_control = 1.00
            psg_rb_defense = 1.045
            psg_right_pace = 0.91
        else:
            psg_mid_control = 0.97
            psg_rb_defense = 1.02
            psg_right_pace = 0.90

        bayern_recovery_risk = 0.94 if davies else 1.08
        stanisic_risk = 1.00 if davies else 1.06
        safonov_shotstop = 1.015
        karl_available = rng.random() < float(weights["karl_available"])
        bischof_available = rng.random() < float(weights["bischof_available"])

        bayern_goals = 0
        psg_goals = 0
        bayern_shots = 0
        psg_shots = 0
        bayern_sot = 0
        psg_sot = 0
        first = None

        for start, end in BLOCKS:
            mins = end - start
            mid = (start + end) / 2
            aggregate_diff = (first_leg["bayern_goals"] + bayern_goals) - (
                first_leg["psg_goals"] + psg_goals
            )

            b_rate = (
                base_bayern_xg
                * mins
                / 96
                * tempo
                * bayern_finishing
                * psg_rb_defense
                * safonov_shotstop
            )
            p_rate = (
                base_psg_xg
                * mins
                / 96
                * tempo
                * psg_finishing
                * star_mult
                * neuer_mult
                * psg_right_pace
                * bayern_recovery_risk
                * stanisic_risk
            )

            if mid < 30:
                b_rate *= prior(priors, "bayern_full_press_early_boost", 1.085)
                p_rate *= prior(priors, "psg_transition_early_boost", 1.065)
            elif mid < 60:
                b_rate *= prior(priors, "bayern_mid_press_boost", 1.045)
                p_rate *= prior(priors, "psg_mid_transition_boost", 1.035)

            b_rate *= 1.025 if psg_mid_control < 0.98 else 1.005
            p_rate *= psg_mid_control

            if mid >= 55:
                if aggregate_diff <= -2:
                    b_rate *= prior(priors, "bayern_chasing_minus_2_boost", 1.32)
                    p_rate *= prior(priors, "psg_counter_when_bayern_minus_2", 1.10)
                    tags["Bayern comeback pressure -2"] += 1
                elif aggregate_diff == -1:
                    b_rate *= prior(priors, "bayern_chasing_minus_1_boost", 1.23)
                    p_rate *= prior(priors, "psg_counter_when_bayern_minus_1", 1.065)
                    tags["Bayern comeback pressure -1"] += 1
                elif aggregate_diff == 0:
                    b_rate *= prior(priors, "bayern_level_attack_multiplier", 0.95)
                    p_rate *= prior(priors, "psg_counter_when_level", 1.03)
                else:
                    b_rate *= prior(priors, "bayern_leading_attack_multiplier", 0.86)
                    p_rate *= prior(priors, "psg_counter_when_bayern_lead", 1.08)

            if mid >= 65:
                if fatigue == "shows_after_60":
                    b_rate *= prior(priors, "psg_fatigue_bayern_boost", 1.09)
                    p_rate *= prior(priors, "psg_fatigue_psg_multiplier", 0.96)
                elif fatigue == "masked_until_ET":
                    b_rate *= prior(priors, "masked_fatigue_bayern_boost", 1.02)

            if mid >= 72 and aggregate_diff < 0:
                if karl_available:
                    b_rate *= prior(priors, "karl_late_boost", 1.055)
                    tags["Karl late direct option active"] += 1
                if bischof_available:
                    b_rate *= prior(priors, "bischof_late_boost", 1.018)
                    tags["Bischof small energy option active"] += 1

            if rng.random() < prior(priors, "psg_transition_burst_probability", 0.055) * mins / 15 and aggregate_diff < 1:
                p_rate *= prior(priors, "psg_transition_burst_multiplier", 1.24)
                tags["PSG repeatable transition burst"] += 1

            system_event_prob = (
                prior(priors, "bayern_system_event_probability", 0.0105)
                * mins
                / 15
                * (prior(priors, "bayern_system_event_chasing_multiplier", 1.25) if aggregate_diff < 0 and mid >= 45 else 1.0)
                * bayern_recovery_risk
                * stanisic_risk
            )
            if rng.random() < system_event_prob:
                psg_goals += 1
                psg_shots += 1
                psg_sot += 1
                tags["Bayern system transition concession"] += 1
                if first is None:
                    first = "PSG"

            ref = rng.lognormvariate(0, 0.17)
            if rng.random() < prior(priors, "bayern_penalty_probability", 0.020) * mins / 15 * ref * (1.08 if aggregate_diff < 0 else 1.0):
                bayern_shots += 1
                bayern_sot += 1
                if rng.random() < 0.80:
                    bayern_goals += 1
                    tags["Bayern penalty goal"] += 1
                    if first is None:
                        first = "Bayern"

            if rng.random() < prior(priors, "psg_penalty_probability", 0.015) * mins / 15 * ref * (1.03 if mid > 55 and aggregate_diff < 0 else 1.0):
                psg_shots += 1
                psg_sot += 1
                if rng.random() < 0.79:
                    psg_goals += 1
                    tags["PSG penalty goal"] += 1
                    if first is None:
                        first = "PSG"

            b_open = poisson_sample(rng, b_rate)
            p_open = poisson_sample(rng, p_rate)
            b_block_shots = max(b_open, poisson_sample(rng, b_rate / 0.145))
            p_block_shots = max(p_open, poisson_sample(rng, p_rate / 0.115))
            bayern_shots += b_block_shots
            psg_shots += p_block_shots
            bayern_sot += min(b_block_shots, poisson_sample(rng, b_block_shots * 0.43) + b_open)
            psg_sot += min(p_block_shots, poisson_sample(rng, p_block_shots * 0.38) + p_open)

            if first is None and b_open + p_open > 0:
                first = "Bayern" if rng.random() < b_open / (b_open + p_open) else "PSG"

            bayern_goals += b_open
            psg_goals += p_open

        scorelines[(bayern_goals, psg_goals)] += 1
        total_goals.append(bayern_goals + psg_goals)
        shots.append((bayern_shots, psg_shots))
        shots_on_target.append((bayern_sot, psg_sot))
        first_goal[first or "No goal"] += 1
        scenario_key = (psg_shape, "Davies" if davies else "No_Davies", fatigue, neuer)

        if bayern_goals - psg_goals >= 2:
            qualification["Bayern"] += 1
            paths["Bayern in 90"] += 1
            scenario_qual[scenario_key]["Bayern"] += 1
        elif bayern_goals - psg_goals <= 0:
            qualification["PSG"] += 1
            paths["PSG in 90"] += 1
            scenario_qual[scenario_key]["PSG"] += 1
        else:
            et_tempo = rng.lognormvariate(0, 0.10)
            et_b_rate = base_bayern_xg * 30 / 96 * prior(priors, "et_bayern_stamina_multiplier", 0.93) * et_tempo * bayern_finishing
            et_p_rate = (
                base_psg_xg
                * 30
                / 96
                * prior(priors, "et_psg_fatigue_multiplier", 0.88)
                * et_tempo
                * psg_finishing
                * star_mult
                * neuer_mult
                * psg_right_pace
                * bayern_recovery_risk
            )
            if fatigue == "shows_after_60":
                et_b_rate *= prior(priors, "et_fatigue_bayern_boost", 1.10)
                et_p_rate *= prior(priors, "et_fatigue_psg_multiplier", 0.94)
            elif fatigue == "masked_until_ET":
                et_b_rate *= prior(priors, "et_masked_bayern_boost", 1.06)
                et_p_rate *= prior(priors, "et_masked_psg_multiplier", 0.96)
            if karl_available:
                et_b_rate *= prior(priors, "et_karl_boost", 1.04)
            if bischof_available:
                et_b_rate *= prior(priors, "et_bischof_boost", 1.015)

            et_bayern = poisson_sample(rng, et_b_rate)
            et_psg = poisson_sample(rng, et_p_rate)
            if et_bayern > et_psg:
                qualification["Bayern"] += 1
                paths["Bayern in ET"] += 1
                scenario_qual[scenario_key]["Bayern"] += 1
            elif et_psg > et_bayern:
                qualification["PSG"] += 1
                paths["PSG in ET"] += 1
                scenario_qual[scenario_key]["PSG"] += 1
            else:
                bayern_pens = min(
                    prior(priors, "max_bayern_penalty_shootout_probability", 0.56),
                    max(
                        prior(priors, "min_bayern_penalty_shootout_probability", 0.50),
                        penalty_neuer + prior(priors, "penalty_home_edge", 0.018),
                    ),
                )
                if rng.random() < bayern_pens:
                    qualification["Bayern"] += 1
                    paths["Bayern on pens"] += 1
                    scenario_qual[scenario_key]["Bayern"] += 1
                else:
                    qualification["PSG"] += 1
                    paths["PSG on pens"] += 1
                    scenario_qual[scenario_key]["PSG"] += 1

    conditional: dict[str, dict[str, float]] = {}
    for selector, values in {
        "psg_shape": ["WZE_RB_Ruiz_mid", "WZE_mid_alt_RB", "unclear_hybrid"],
        "davies": ["Davies", "No_Davies"],
        "fatigue": ["shows_after_60", "masked_until_ET", "not_visible"],
        "neuer": ["strong", "normal", "bad_tail"],
    }.items():
        conditional[selector] = {}
        idx = {"psg_shape": 0, "davies": 1, "fatigue": 2, "neuer": 3}[selector]
        for value in values:
            total = 0
            bayern = 0
            for key, counter in scenario_qual.items():
                if key[idx] == value:
                    total += counter["Bayern"] + counter["PSG"]
                    bayern += counter["Bayern"]
            conditional[selector][value] = bayern / total if total else 0.0

    top_scores = [
        {"score": f"{b}-{p}", "probability": count / runs}
        for (b, p), count in scorelines.most_common(20)
    ]

    return {
        "runs": runs,
        "probabilities_90": {
            "bayern_win": sum(c for (b, p), c in scorelines.items() if b > p) / runs,
            "draw": sum(c for (b, p), c in scorelines.items() if b == p) / runs,
            "psg_win": sum(c for (b, p), c in scorelines.items() if b < p) / runs,
        },
        "qualification": {"bayern": pct(qualification, "Bayern", runs), "psg": pct(qualification, "PSG", runs)},
        "paths": {key.lower().replace(" ", "_"): value / runs for key, value in paths.items()},
        "score_buckets": {
            "bayern_by_2_plus": sum(c for (b, p), c in scorelines.items() if b - p >= 2) / runs,
            "bayern_by_1_extra_time": sum(c for (b, p), c in scorelines.items() if b - p == 1) / runs,
            "psg_advance_in_90": sum(c for (b, p), c in scorelines.items() if b - p <= 0) / runs,
        },
        "scorelines": top_scores,
        "projections": {
            "average_goals": mean(total_goals),
            "median_goals": median(total_goals),
            "over_4_5": sum(g >= 5 for g in total_goals) / runs,
            "both_teams_score": sum(c for (b, p), c in scorelines.items() if b > 0 and p > 0) / runs,
            "bayern_shots": mean(b for b, _ in shots),
            "psg_shots": mean(p for _, p in shots),
            "bayern_sot": mean(b for b, _ in shots_on_target),
            "psg_sot": mean(p for _, p in shots_on_target),
        },
        "first_goal": {key: value / runs for key, value in first_goal.items()},
        "conditional_bayern_qualification": conditional,
        "event_tags_per_match": {key: value / runs for key, value in tags.most_common(20)},
        "metadata": {
            "model_type": "scenario-weighted, game-state-dependent Monte Carlo with Poisson goal generation",
            "best_value_score": "Bayern 3-1 PSG",
            "modal_score": top_scores[0]["score"],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Bayern vs PSG second-leg simulation.")
    parser.add_argument("--config", default="configs/bayern_psg.json")
    parser.add_argument("--output", default="outputs/results.json")
    parser.add_argument("--runs", type=int)
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()

    config_path = Path(args.config)
    config = json.loads(config_path.read_text())
    if args.runs is not None:
        config["simulation"]["runs"] = args.runs
    if args.seed is not None:
        config["simulation"]["seed"] = args.seed

    result = run_simulation(config)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result["qualification"], indent=2))
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
