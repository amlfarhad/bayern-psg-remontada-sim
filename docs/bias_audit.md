# Bias Audit

This audit tests whether Bayern-favorable analyst priors are driving the headline result.

Runs per scenario: `120,000`

## Summary Table

| Variant | Bayern qualify | Delta vs baseline | Modal score | Purpose |
| --- | ---: | ---: | --- | --- |
| `baseline` | 52.1% | +0.0% | 3-2 | Current public model: data anchors plus analyst priors from the discussion. |
| `raw_ucl_finishing_ratios` | 47.7% | -4.4% | 3-2 | Uses raw UCL goals/xG finishing multipliers for both teams. This is a PSG-friendly check because PSG's UCL overperformance is larger. |
| `no_comeback_narrative` | 50.1% | -2.0% | 3-2 | Removes most of Bayern's comeback/crowd late-game boost and makes chasing states more conservative. |
| `no_psg_fatigue_edge` | 50.6% | -1.5% | 3-2 | Assumes PSG fatigue does not show and removes the Bayern late boost from fatigue states. |
| `psg_midfield_not_disrupted` | 51.3% | -0.9% | 3-2 | Assumes WZE stays central or PSG solve RB without materially weakening midfield dynamics. |
| `psg_transition_stress` | 51.5% | -0.6% | 3-2 | Raises PSG transition burst frequency and Bayern system-event risk to test whether the press risk is understated. |
| `neutral_et_penalties` | 51.1% | -1.1% | 3-2 | Removes Bayern's extra-time and penalty-shootout edge. |
| `anti_bayern_stack` | 43.0% | -9.2% | 3-2 | Stacks the most defensible PSG-friendly choices: raw UCL finishing, no PSG fatigue, less midfield disruption, more PSG transition danger, neutral ET/pens. |

## Verdict

- The model is **not purely laundering a Bayern fan take**: the baseline is narrow, and PSG-friendly stress tests can flip the tie.
- The largest bias-sensitive channel is PSG finishing treatment. Using raw UCL goals/xG finishing ratios moves Bayern from 52.1% to 47.7%.
- The Bayern comeback/crowd prior matters but is not the entire model: removing it moves Bayern to 50.1%.
- The anti-Bayern stack gives Bayern 43.0%, meaning the public headline should avoid sounding like a confident Bayern call.

## Interpretation

The current model contains Bayern-leaning priors, especially around late-game pressure, extra-time stamina, and the PSG midfield reshuffle. It also contains PSG-leaning priors, especially around elite finishing and repeatable transition bursts. The honest public wording is therefore: Bayern have a narrow model edge under the chosen assumptions, but the result is assumption-sensitive and PSG-friendly assumptions can flip it.
