# MD-1 Research Update

Checked on May 5, 2026 local time before Bayern vs PSG on Wednesday 6 May.

## High-Confidence Updates

- UEFA lists Bayern's possible XI as Neuer; Stanišić, Upamecano, Tah, Laimer; Kimmich, Pavlović; Olise, Musiala, Luis Díaz; Kane.
- UEFA lists PSG's possible XI as Safonov; Zaïre-Emery, Marquinhos, Pacho, Nuno Mendes; Vitinha; João Neves, Fabián Ruiz; Doué, Dembélé, Kvaratskhelia.
- UEFA lists Gnabry out for Bayern and Hakimi plus Chevalier out for PSG, with no doubts for either side.
- PSG's official squad includes Safonov, Zaïre-Emery, Fabián, Vitinha, João Neves, Nuno Mendes, Doué, Dembélé and Kvaratskhelia.
- Luis Enrique and Zaïre-Emery both framed PSG's approach as proactive. PSG are not publicly preparing the game as a survival low block.
- Opta's public supercomputer is materially more PSG-leaning than the previous project baseline: Bayern win the 90 minutes 52.7%, but PSG qualify 57.8%.
- German final-training reporting says Karl, Bischof and Guerreiro were on the pitch, increasing Bayern's late bench optionality.
- Referee reporting points to João Pinheiro with Marco Di Bello on VAR. I did not materially change the penalty model because public referee samples are mixed and low-volume.

## Model Changes

- PSG shape moved from uncertain to strongly weighted toward Zaïre-Emery at RB with Fabián Ruiz in midfield.
- Davies/recovery-pace availability moved down because UEFA's possible lineup uses Laimer and other reporting remains mixed.
- Karl and Bischof bench availability moved up after final-training reports.
- Base Bayern and PSG xG rates were recalibrated toward Opta's MD-1 benchmark to reduce Bayern-fan leakage in the headline probability.

## Updated Output

- Bayern qualify: 44.2%.
- PSG qualify: 55.8%.
- Bayern overturn in regulation by two or more: 32.5%.
- Bayern win by one and force extra time: 19.9%.
- PSG survive regulation: 47.6%.
- Most common regulation score: 3-2.
- Average total goals: 5.22.
- Both teams score: 84.7%.

## Interpretation

The biggest change is not that Bayern suddenly look bad. It is that the model was over-crediting the home comeback path relative to external MD-1 information. Bayern are still more likely than PSG to win the second leg in 90 minutes, but the exact required margin makes PSG the tie favorite.

The football read is still chaos-positive: PSG's Hakimi loss is real, Bayern's home pressure is real, and the first leg plus both camps' quotes point away from a cagey match. But after the MD-1 refresh, the honest headline is PSG slight-to-moderate tie favorite, Bayern live comeback threat.
