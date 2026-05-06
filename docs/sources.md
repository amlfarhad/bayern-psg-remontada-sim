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

## MD-1 Research Refresh

Refresh completed on May 5, 2026 local time, ahead of the Wednesday 6 May second leg.

### UEFA Team News And Match Preview

URLs:

- https://www.uefa.com/uefachampionsleague/news/02a5-208b14a03cf8-b4d8a8bcc76b-1000--champions-league-semi-final-second-legs-starting-and-possib/
- https://www.uefa.com/uefachampionsleague/news/02a5-2087ecd92e89-edd633c22f65-1000--bayern-vs-paris-champions-league-preview-where-to-watch-/

Used for:

- Match timing and venue.
- Latest possible lineups.
- Confirmed listed absences: Gnabry for Bayern; Hakimi and Chevalier for PSG.
- No official doubts listed by UEFA.
- Competition goal context: PSG 43, Bayern 42.
- Coach/player comments pointing toward both sides maintaining aggressive styles.

### PSG Official MD-1 Sources

URLs:

- https://www.psg.fr/en/content/the-squad-for-fc-bayern-munich-paris-saint-germain-uefa-champions-league-20252026
- https://www.psg.fr/en/content/luis-enrique-no-player-will-stop-playing-no-supporter-will-stop-singing-press-conferencefc-bayern-munich-paris-saint-germain-uefa-champions-league-2025-2026
- https://www.psg.fr/en/content/warren-zaire-emery-do-all-we-can-to-win-this-match-and-qualify-for-the-final-again-press-conference-fc-bayern-munich-paris-saint-germain-uefa-champions-league-2025-2026

Used for:

- PSG travelling squad confirmation.
- Safonov, Zaïre-Emery, Fabián, Vitinha, João Neves, Nuno Mendes and the front three all included.
- Luis Enrique framing the one-goal lead as insufficient.
- Zaïre-Emery stating PSG intend to press, win the ball high, and attack rather than low-block.

### Opta Analyst MD-1 Preview

URL: https://theanalyst.com/articles/bayern-munich-vs-psg-predictions-champions-league-semi-final-second-leg-05-2026

Used for:

- External calibration check.
- Opta supercomputer: Bayern 90-minute win 52.7%, draw 20.1%, PSG 90-minute win 27.2%.
- Opta supercomputer: PSG qualify 57.8%, Bayern qualify 42.2%.
- PSG opponent-box-touch concession trend and both teams' knockout scoring context.
- Player production context for Kvaratskhelia, Doué and Kane.

### German Final-Training Reporting

URLs:

- https://sport.sky.de/fussball/artikel/karl-bischof-und-guerreiro-beim-training-des-fc-bayern-vor-psg/13540391/34130
- https://web.de/magazine/sport/fussball/champions-league/fc-bayern-psg-live-blog-aufatmen-fc-bayern-42227912

Used for:

- Karl, Bischof and Guerreiro appearing in final training.
- Gnabry remaining Bayern's main confirmed attacking absence.
- Hakimi, Chevalier and Ndjantou listed as PSG absences.

### Match Officials

URLs:

- https://bulinews.com/portuguese-referee-appointed-for-bayern-psg-champions-league-semi-final-second-leg
- https://www.aia-figc.it/news/champions-league-marco-di-bello-designato-come-var-per-la-partita-bayern-monaco-psg-27358/

Used for:

- João Pinheiro referee appointment.
- Bruno Jesus and Luciano Maia as assistants.
- Espen Eskås fourth official.
- Marco Di Bello VAR and Tiago Martins AVAR.
- No material model adjustment because available referee-card and penalty samples are too small to justify a strong prior shift.

Before kickoff, still refresh:

- Hakimi injury status
- Chevalier/Safonov expected starter status
- Ruiz fitness status
- Zaire-Emery expected role
- Davies availability
- Karl availability
- Bischof availability
- Confirmed referee and referee card/penalty history
- Market odds close to kickoff
