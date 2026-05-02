# Model Contract

This file defines what the executable simulation should accept and return.

## Inputs

The model should accept a configuration object with these sections:

```yaml
observed_data:
  bayern:
    ucl_goals: 38
    ucl_xg: 33.54
    ucl_goals_against: 14
    ucl_xga: 17.20
    ucl_shots: 230
    ucl_sot: 99
  psg:
    ucl_goals: 38
    ucl_xg: 28.82
    ucl_goals_against: 17
    ucl_xga: 17.59
    ucl_shots: 270
    ucl_sot: 102
  first_leg:
    bayern_goals: 4
    psg_goals: 5
    bayern_xg: 2.51
    psg_xg: 1.91

scenario_weights:
  psg_shape:
    wze_rb_ruiz_mid: 0.60
    wze_mid_alt_rb: 0.25
    unclear_hybrid: 0.15
  davies_present: 0.60
  psg_fatigue:
    shows_after_60: 0.36
    masked_until_extra_time: 0.40
    not_visible: 0.24
  neuer_state:
    strong: 0.24
    normal: 0.54
    bad_tail: 0.22
  karl_available: 0.55
  bischof_available: 0.35

simulation:
  runs: 300000
  random_seed: 202605021337
```

## Outputs

The executable simulation should return a structured result:

```json
{
  "runs": 300000,
  "probabilities_90": {
    "bayern_win": 0.5967,
    "draw": 0.1646,
    "psg_win": 0.2387
  },
  "qualification": {
    "bayern": 0.5190,
    "psg": 0.4810
  },
  "paths": {
    "bayern_in_90": 0.3966,
    "psg_in_90": 0.4033,
    "bayern_in_extra_time": 0.0802,
    "psg_in_extra_time": 0.0413,
    "bayern_on_penalties": 0.0421,
    "psg_on_penalties": 0.0364
  },
  "scorelines": [
    {"score": "3-2", "probability": 0.0643},
    {"score": "3-1", "probability": 0.0597},
    {"score": "2-1", "probability": 0.0594}
  ],
  "projections": {
    "average_goals": 5.37,
    "over_4_5": 0.6117,
    "both_teams_score": 0.8462,
    "bayern_shots": 21.47,
    "psg_shots": 18.27,
    "bayern_sot": 11.38,
    "psg_sot": 8.46
  },
  "conditional": {
    "davies_present": {"bayern_qualify": 0.5485},
    "davies_absent": {"bayern_qualify": 0.4748}
  }
}
```

## Command-Line Interface

Planned command:

```bash
python -m src.simulate --config configs/bayern_psg.yaml --runs 300000
```

Planned options:

- `--runs`: number of Monte Carlo runs
- `--seed`: random seed
- `--config`: model configuration file
- `--scenario`: named scenario override
- `--output`: path to JSON result

## Reproducibility Requirements

- All random runs must accept a seed.
- All scenario weights must be config-driven.
- No hard-coded source values should be hidden inside simulation functions.
- The output JSON should include the config hash or embedded config.
- Every final figure in the README should be reproducible from a saved config.

