# Feature Dictionary

This file defines the features used or planned for the simulation.

## Observed Data Features

| Feature | Type | Description | Current Use |
| --- | --- | --- | --- |
| `team_xg_ucl` | numeric | Champions League expected goals | Base attacking rate |
| `team_xga_ucl` | numeric | Champions League expected goals against | Defensive strength prior |
| `team_goals_ucl` | numeric | Champions League goals scored | Finishing prior |
| `team_goals_against_ucl` | numeric | Champions League goals conceded | Defensive outcome prior |
| `team_shots_ucl` | numeric | Champions League shots | Shot-volume projection |
| `team_sot_ucl` | numeric | Champions League shots on target | Shot-on-target projection |
| `first_leg_xg` | numeric | First-leg expected goals | Matchup calibration |
| `first_leg_score` | categorical | PSG 5-4 Bayern | Aggregate state and context |
| `first_leg_shots` | numeric | First-leg shot count | Tempo and shot-quality calibration |
| `market_1x2` | numeric | Betting-market win/draw/loss probabilities | Moderate prior |
| `market_total` | numeric | Betting-market total-goals expectation | Calibration guardrail |

## Analyst Prior Features

| Feature | Type | Description | Directional Effect |
| --- | --- | --- | --- |
| `bayern_full_throttle_press` | boolean/probability | Bayern press aggressively from the start | Raises Bayern xG and PSG transition xG |
| `bayern_system_risk` | numeric | Risk created by high press and rest-defense exposure | Raises PSG transition event chance |
| `bayern_fluid_attack` | numeric | Kane, Olise, Diaz, Musiala rotations and role fluidity | Raises Bayern chance quality |
| `bayern_intricacy_penalty` | numeric | Risk of overplaying instead of shooting | Currently low or zero |
| `bayern_comeback_momentum` | numeric | Bayern emotional/crowd response when behind | Raises late Bayern xG |
| `psg_transition_repeatability` | numeric | Ability of PSG forwards to generate repeatable counters | Raises PSG xG in open game states |
| `psg_elite_finishing` | numeric | Kvaratskhelia, Dembele, Doue, Barcola finishing/carrying quality | Keeps PSG finishing above average |
| `hakimi_attacking_loss` | numeric | Lost right-side pace and outlet quality | Lowers PSG transition rate |
| `wze_midfield_loss` | numeric | Cost of moving Zaire-Emery from midfield to RB | Lowers PSG progression and counter-launch quality |
| `ruiz_rhythm_risk` | numeric | Ruiz being technically good but potentially off pace | Lowers PSG counter-launch speed |
| `davies_recovery_pace` | boolean/probability | Recovery pace behind Bayern's press | Lowers PSG transition conversion |
| `stanisic_level_risk` | numeric | Concern that Stanisic profile may not match this game's athletic level | Raises PSG wide transition danger |
| `safonov_keeper_level` | numeric | Safonov as fine but not elite | Slightly raises Bayern conversion/rebound potential |
| `neuer_state` | categorical | Strong, normal, bad-tail | Changes PSG conversion and penalty edge |
| `karl_late_option` | boolean/probability | Direct late runner/shooter option | Raises Bayern late xG when chasing |
| `bischof_energy_option` | boolean/probability | Small late midfield-energy option | Slight Bayern late boost |
| `psg_fatigue_state` | categorical | Visible after 60, masked until ET, not visible | Changes late Bayern/PSG rates |

## Game-State Features

| Feature | Type | Description |
| --- | --- | --- |
| `minute_block` | categorical | 15-minute block of match |
| `second_leg_score` | tuple | Current second-leg score |
| `aggregate_diff_bayern` | integer | Bayern aggregate goals minus PSG aggregate goals |
| `bayern_need_goals` | integer | Goals Bayern need to qualify or force ET |
| `psg_can_counter_space` | numeric | Counter space available based on Bayern pressure/game state |
| `late_chase_state` | boolean | Bayern are behind after 60 minutes |
| `et_required` | boolean | Bayern win by exactly one after 90 |

## Event Features

| Feature | Type | Description |
| --- | --- | --- |
| `penalty_event` | stochastic | Penalty awarded and conversion sampled |
| `red_card_event` | stochastic | Card/shock event that changes block rates |
| `system_transition_event` | stochastic | PSG chance created by Bayern rest-defense exposure |
| `set_piece_event` | stochastic | Goal from set-piece chance |

