# Bias Audit

This audit tests whether Bayern-favorable analyst priors are driving the headline result.

Runs per scenario: `120,000`

## Summary Table

| Variant | Bayern qualify | Delta vs baseline | Modal score | Purpose |
| --- | ---: | ---: | --- | --- |
| `baseline` | 52.0% | +0.0% | 3-2 | Current public model: data anchors plus analyst priors from the discussion. |
| `raw_ucl_finishing_ratios` | 47.7% | -4.3% | 3-2 | Uses raw UCL goals/xG finishing multipliers for both teams. This is a PSG-friendly check because PSG's UCL overperformance is larger. |
| `no_comeback_narrative` | 49.9% | -2.1% | 3-2 | Removes most of Bayern's comeback/crowd late-game boost and makes chasing states more conservative. |
| `no_psg_fatigue_edge` | 50.4% | -1.6% | 3-2 | Assumes PSG fatigue does not show and removes the Bayern late boost from fatigue states. |
| `psg_midfield_not_disrupted` | 51.2% | -0.9% | 3-2 | Assumes WZE stays central or PSG solve RB without materially weakening midfield dynamics. |
| `psg_transition_stress` | 51.0% | -1.0% | 3-2 | Raises PSG transition burst frequency and Bayern system-event risk to test whether the press risk is understated. |
| `neutral_et_penalties` | 50.9% | -1.1% | 3-2 | Removes Bayern's extra-time and penalty-shootout edge. |
| `anti_bayern_stack` | 42.8% | -9.2% | 3-2 | Stacks the most defensible PSG-friendly choices: raw UCL finishing, no PSG fatigue, less midfield disruption, more PSG transition danger, neutral ET/pens. |

## Verdict

- The model is **not laundering a Bayern fan take**: after the MD-1 refresh, the baseline is only Bayern 52.0% / PSG 48.0%.
- The largest bias-sensitive channel is PSG finishing treatment. Using raw UCL goals/xG finishing ratios moves Bayern from 52.0% to 47.7%.
- The Bayern comeback/crowd prior matters but is not the entire model: removing it moves Bayern to 49.9%.
- The anti-Bayern stack gives Bayern 42.8%, meaning the public headline should avoid sounding like a confident Bayern call.

## Interpretation

The current model still contains Bayern-leaning priors, especially around late-game pressure, extra-time stamina, home crowd effects, and the now-cleaner Bayern availability picture. It also contains PSG-leaning priors around elite finishing, transition bursts, and the possibility that PSG solve the Hakimi absence without losing too much midfield control. The honest public wording is therefore: Bayern have a narrow model edge, but PSG-friendly assumptions can still flip the tie.
