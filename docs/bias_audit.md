# Bias Audit

This audit tests whether Bayern-favorable analyst priors are driving the headline result.

Runs per scenario: `120,000`

## Summary Table

| Variant | Bayern qualify | Delta vs baseline | Modal score | Purpose |
| --- | ---: | ---: | --- | --- |
| `baseline` | 44.0% | +0.0% | 3-2 | Current public model: data anchors plus analyst priors from the discussion. |
| `raw_ucl_finishing_ratios` | 39.9% | -4.1% | 3-2 | Uses raw UCL goals/xG finishing multipliers for both teams. This is a PSG-friendly check because PSG's UCL overperformance is larger. |
| `no_comeback_narrative` | 42.2% | -1.8% | 2-2 | Removes most of Bayern's comeback/crowd late-game boost and makes chasing states more conservative. |
| `no_psg_fatigue_edge` | 43.2% | -0.8% | 2-1 | Assumes PSG fatigue does not show and removes the Bayern late boost from fatigue states. |
| `psg_midfield_not_disrupted` | 43.5% | -0.6% | 3-2 | Assumes WZE stays central or PSG solve RB without materially weakening midfield dynamics. |
| `psg_transition_stress` | 43.4% | -0.7% | 3-2 | Raises PSG transition burst frequency and Bayern system-event risk to test whether the press risk is understated. |
| `neutral_et_penalties` | 43.4% | -0.6% | 3-2 | Removes Bayern's extra-time and penalty-shootout edge. |
| `anti_bayern_stack` | 35.0% | -9.0% | 3-2 | Stacks the most defensible PSG-friendly choices: raw UCL finishing, no PSG fatigue, less midfield disruption, more PSG transition danger, neutral ET/pens. |

## Verdict

- The model is **not laundering a Bayern fan take**: after the MD-1 refresh, the baseline gives PSG 56.0% to qualify.
- The largest bias-sensitive channel is PSG finishing treatment. Using raw UCL goals/xG finishing ratios moves Bayern from 44.0% to 39.9%.
- The Bayern comeback/crowd prior matters but is not the entire model: removing it moves Bayern to 42.2%.
- The anti-Bayern stack gives Bayern 35.0%, meaning the public headline should avoid sounding like a confident Bayern call.

## Interpretation

The current model still contains Bayern-leaning priors, especially around late-game pressure, extra-time stamina, and home crowd effects. The MD-1 research refresh pulls the headline toward PSG because Zaïre-Emery at right-back with Fabián Ruiz in midfield is now the dominant expected PSG structure, Davies is less certain, and the Opta supercomputer is a credible external benchmark. The honest public wording is therefore: PSG are tie favorites, while Bayern remain a live comeback threat because they are still very capable of winning the 90 minutes.
