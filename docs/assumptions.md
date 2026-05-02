# Assumptions

This file records the current football assumptions behind the model.

## User Priors

These are subjective football priors supplied by the analyst/user.

1. The model should blend matchup/recent evidence with season xG.
2. PSG's xG overperformance should be treated mostly as elite quality, not pure variance.
3. Bayern should not be heavily penalized for intricate attack patterns.
4. The first leg reflected the quality of both teams, not a one-off fluke.
5. Neuer's extreme performances are difficult to predict reliably.
6. PSG fatigue is plausible, especially after the first leg, but high stakes could mask it.
7. Bayern should press full throttle from minute 1.
8. PSG are unlikely to low block; they are more likely to counter through broken phases.
9. Zaire-Emery at RB may be defensively fine, but it costs PSG midfield dynamism and right-side pace.
10. Fabian Ruiz looked off rhythm in the first leg and may slow PSG's counter-launch sequences.
11. Karl is hard to project post-injury but has enough talent to matter late.
12. Bayern's defensive risk is system-based, not because the center-backs are poor.
13. Bayern's attack is fluid and positionless: Kane drops, Olise and Diaz rotate, and overloads shift.
14. Kvaratskhelia, Dembele, Doue, and Barcola are all capable of deciding the tie.
15. Kimmich had the upper hand in the first leg.
16. Bayern have a stronger anti-collapse mentality, but PSG are not fragile.
17. Set pieces are roughly even.
18. Davies matters mainly as recovery-pace insurance.
19. Stanisic may not match the required athletic level for this specific game.
20. Bayern's comeback pattern is primarily mentality and crowd momentum.
21. Hakimi's absence is mainly an attacking-pace loss, with midfield domino effects.
22. Market odds should matter somewhat, but football-specific priors should override when justified.
23. Safonov is fine but ordinary; PSG structure protects him, but he is not treated as an elite tie-stealer.
24. Bayern conversion should remain high because Kane, Olise, and Diaz are elite.
25. PSG conversion should remain high because their forward quality is elite.
26. Bayern have the extra-time edge because of stamina and Allianz pressure.
27. Bayern's bench is not deep, but Karl and possibly Bischof are real late options.
28. Referee assumptions should be facts-only, with no unsourced bias adjustment.
29. Bayern's best XI is strong enough despite injuries.
30. PSG's counters are repeatable, but Hakimi's absence lowers certainty.
31. The final prediction should prioritize football-informed value, not only the modal score.

## Current Scenario Weights

These weights are initial assumptions and should be exposed as configuration.

| Scenario | Weight |
| --- | ---: |
| PSG shape: WZE at RB, Ruiz midfield | 0.60 |
| PSG shape: WZE midfield, alternate RB | 0.25 |
| PSG shape: unclear hybrid | 0.15 |
| Davies/recovery pace present | 0.60 |
| PSG fatigue visible after 60 | 0.36 |
| PSG fatigue masked until extra time | 0.40 |
| PSG fatigue not visible | 0.24 |
| Neuer strong state | 0.24 |
| Neuer normal state | 0.54 |
| Neuer bad-tail state | 0.22 |
| Karl available as late option | 0.55 |
| Bischof available as small energy option | 0.35 |

## Current Prediction Snapshot

Latest documented simulation run:

- Simulations: 300,000
- Bayern win in 90: 59.7%
- Draw in 90: 16.5%
- PSG win in 90: 23.9%
- Bayern advance in 90: 39.7%
- Extra time: 20.0%
- PSG advance in 90: 40.3%
- Bayern qualify overall: 51.9%
- PSG qualify overall: 48.1%

Most likely 90-minute scorelines:

1. Bayern 3-2 PSG
2. Bayern 3-1 PSG
3. Bayern 2-1 PSG
4. Bayern 2-2 PSG
5. Bayern 4-2 PSG

Football-informed value score:

```text
Bayern 3-1 PSG
```

