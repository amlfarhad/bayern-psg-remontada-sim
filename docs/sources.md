# Sources

This file lists public sources used to anchor the model. Exact values should be periodically refreshed before publishing or rerunning the final model.

## Statistical Sources

### StatMuse Champions League Team xG

URL: https://www.statmuse.com/fc/ask/teams-with-most-expected-goals?l=ucl

Used for:

- Team xG
- Goals
- Goals conceded
- xGA
- Shots
- Shots on target
- Possession
- Fouls
- Yellow/red cards

Current extracted values:

| Team | Matches | Goals | xG | Goals Against | xGA | Shots | SOT |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Bayern | 12 | 38 | 33.54 | 14 | 17.20 | 230 | 99 |
| PSG | 14 | 38 | 28.82 | 17 | 17.59 | 270 | 102 |

### Opta Analyst First-Leg Report

URL: https://theanalyst.com/articles/psg-vs-bayern-munich-stats-opta-champions-league-semi-final-first-leg-04-2026

Used for:

- First-leg xG
- First-leg score context
- Finishing quality interpretation
- Bayern front-three goal contribution context

Current extracted values:

- PSG 5-4 Bayern
- PSG xG: 1.91
- Bayern xG: 2.51
- 22 total shots
- Bayern front three Kane, Olise, and Diaz reported at 100 combined goals this season

### FBref Bayern Munich

URL: https://fbref.com/en/squads/054efa67/2025-2026/Bayern-Munich-Stats

Used for:

- Domestic team strength cross-check
- Bayern goals, goals against, xG, xGA
- Overall Kompany-era performance profile

### UEFA PSG Squad Page

URL: https://www.uefa.com/uefachampionsleague/clubs/52747--paris//squad/

Used for:

- PSG squad registration
- Goalkeeper context
- Player availability cross-check

### Transfer/Goalkeeper Context

URLs:

- https://www.culturepsg.com/news/mercato/le-psg-et-city-officialisent-le-transfert-de-donnarumma/56856
- https://www.goal.com/en-us/lists/gianluigi-donnarumma-completes-transfer-man-city-psg-long-term-contract-replacement-ederson/bltbe0da667e679a454

Used for:

- Correcting PSG goalkeeper assumption: Donnarumma is no longer at PSG.
- PSG goalkeeper should be modeled as Safonov/Chevalier context, not Donnarumma.

## Reporting Sources To Refresh

Before final publication, refresh:

- Hakimi injury status
- Chevalier/Safonov expected starter status
- Ruiz fitness status
- Zaire-Emery expected role
- Davies availability
- Karl availability
- Bischof availability
- Confirmed referee and referee card/penalty history
- Market odds close to kickoff

