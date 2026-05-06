# Methodology

This project uses a scenario-weighted Monte Carlo simulation to estimate how Bayern vs PSG second leg could play out.

The model is intentionally transparent. It does not try to learn from a massive private event dataset. Instead, it combines public statistical inputs, tactical priors, lineup uncertainty, and game-state logic into repeated simulated match paths.

## 1. Data Anchors

The base rates should be anchored to public statistical sources:

- Champions League team xG, xGA, goals, shots, shots on target, possession, fouls, and cards.
- First-leg xG, scoreline, shot count, and tactical observations.
- Player availability and expected lineup news.
- Market odds as a moderate prior, not the only source of truth.

Current key anchors:

- Bayern: 38 Champions League goals from 33.54 xG, 230 shots, 99 shots on target.
- PSG: 38 Champions League goals from 28.82 xG, 270 shots, 102 shots on target.
- First leg: PSG 5-4 Bayern.
- First-leg Opta xG: PSG 1.91, Bayern 2.51.
- UEFA's match preview has PSG on 43 Champions League goals and Bayern on 42 before the second leg.
- Opta's MD-1 supercomputer has Bayern winning the 90 minutes in 52.7% of simulations but Bayern qualifying in only 42.2%.
- Bayern front-line production and PSG knockout production remain treated as elite enough that finishing is not regressed all the way to raw xG.

## 2. Priors And Analyst Inputs

The model separates observed data from analyst priors. Analyst priors are football-specific assumptions that cannot be fully captured by public xG tables.

Current analyst priors:

- Bayern should press full throttle from minute 1.
- Bayern's risk is mainly structural, not caused by poor center-back quality.
- Upamecano and Tah should be treated as high-level defenders defending difficult spaces.
- PSG will not simply low block; they are likely to counter and attack through broken phases.
- PSG's finishing overperformance should not be regressed hard because Kvaratskhelia, Dembele, Doue, and Barcola provide elite shot quality and execution.
- Bayern's attacking intricacy should not be penalized strongly because their fluid front line creates high-value looks.
- Hakimi's biggest loss is attacking pace and right-side transition outlet quality.
- If Zaire-Emery moves to right-back, PSG may defend that zone well but lose midfield athleticism and dynamism.
- Fabian Ruiz may be technically useful but could slow counter-launch speed if off rhythm.
- Bayern have the extra-time stamina edge.
- Bayern's bench is weaker than ideal, but Karl and possibly Bischof provide late energy.

MD-1 update:

- UEFA, Opta and PSG reporting converged on Zaïre-Emery at right-back with Fabián Ruiz in midfield, so that scenario is now the dominant PSG shape.
- UEFA's possible Bayern lineup listed Laimer rather than Davies at left-back, while other previews still had Davies starting. The Davies/recovery-pace scenario was therefore reduced from likely to close-to-even.
- German reporting from final training indicated Karl, Bischof and Guerreiro were back on the pitch, increasing late-bench availability.
- The base xG rates were recalibrated toward Opta's public MD-1 simulation because the previous baseline was too Bayern-friendly relative to a credible external benchmark.

## 3. Feature Engineering

The model creates match-level and block-level features.

Match-level features are sampled once per simulation:

- PSG lineup structure
- Davies/recovery-pace availability
- PSG fatigue state
- Neuer performance state
- PSG front-line finishing state
- Bayern finishing state
- Karl availability
- Bischof availability
- Bayern press risk profile

Block-level features are updated every 15 minutes:

- Current aggregate score
- Whether Bayern need one goal, two goals, or are ahead
- Whether PSG can counter into space
- Whether PSG fatigue begins to show
- Whether Bayern use late direct attacking options
- Penalty and card volatility
- System-transition concession risk

## 4. Simulation Mechanics

Each match is simulated in time blocks:

```text
0-15, 15-30, 30-45, 45-60, 60-75, 75-90, 90-96
```

For each block:

1. Start with base Bayern and PSG xG rates.
2. Apply scenario modifiers.
3. Apply game-state modifiers.
4. Generate open-play goals using Poisson sampling.
5. Generate penalty and transition-event goals as separate stochastic events.
6. Update the match and aggregate score.

If Bayern win the second leg by exactly one goal, the tie goes to extra time.

Extra time is modeled separately with:

- Lower per-minute scoring rate
- Bayern stamina/home edge
- PSG transition danger against tired legs
- Karl/Bischof availability if applicable
- Penalty shootout if aggregate remains level

## 5. Qualification Logic

PSG enter the second leg leading 5-4.

After 90 minutes:

- Bayern win by 2 or more: Bayern qualify in 90.
- Bayern win by 1: extra time.
- Draw or PSG win: PSG qualify in 90.

After extra time:

- Bayern score more in extra time: Bayern qualify.
- PSG score more in extra time: PSG qualify.
- Extra time draw: penalty shootout.

## 6. Calibration

The model should be calibrated against:

- Market 1X2 probabilities
- Market totals
- First-leg statistical profile
- UCL team xG and xGA
- Sensible scoreline distributions

Calibration is not allowed to erase tactical priors. The market is treated as one input among several.

## 7. Validation And Stress Tests

Required stress tests:

- PSG finishing regressed hard vs treated as elite skill
- Davies present vs absent
- WZE at RB with Ruiz midfield vs alternative PSG shape
- PSG fatigue visible after 60 vs masked by adrenaline
- Neuer strong vs normal vs bad-tail
- Karl available vs unavailable
- Bayern full-throttle press vs controlled press

The output should include conditional qualification probabilities for each major scenario.

## 8. Known Limitations

- Public xG data is not event-level enough to fully model shot location and pressure.
- Injury and fatigue reporting may be incomplete.
- Some tactical priors are subjective and should be labelled as such.
- Player chemistry and in-game coaching changes are hard to quantify.
- Penalty and red-card events are inherently noisy.
