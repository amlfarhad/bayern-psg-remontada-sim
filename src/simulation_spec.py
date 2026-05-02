"""
Simulation design notes for the Bayern vs PSG second-leg project.

This file is intentionally not the final executable model yet. It documents the
intended code structure so implementation can follow the methodology cleanly.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


TeamName = Literal["Bayern", "PSG"]
PSGShape = Literal["WZE_RB_Ruiz_mid", "WZE_mid_alt_RB", "unclear_hybrid"]
FatigueState = Literal["shows_after_60", "masked_until_ET", "not_visible"]
NeuerState = Literal["strong", "normal", "bad_tail"]


@dataclass(frozen=True)
class TeamData:
    """Observed team-level statistical inputs."""

    goals: float
    xg: float
    goals_against: float
    xga: float
    shots: float
    shots_on_target: float


@dataclass(frozen=True)
class FirstLegData:
    """First-leg score and xG context."""

    bayern_goals: int
    psg_goals: int
    bayern_xg: float
    psg_xg: float


@dataclass(frozen=True)
class ScenarioWeights:
    """Configurable scenario probabilities."""

    psg_wze_rb_ruiz_mid: float
    psg_wze_mid_alt_rb: float
    psg_unclear_hybrid: float
    davies_present: float
    fatigue_shows_after_60: float
    fatigue_masked_until_et: float
    fatigue_not_visible: float
    neuer_strong: float
    neuer_normal: float
    neuer_bad_tail: float
    karl_available: float
    bischof_available: float


@dataclass(frozen=True)
class ModelConfig:
    """Top-level model configuration."""

    bayern: TeamData
    psg: TeamData
    first_leg: FirstLegData
    scenarios: ScenarioWeights
    runs: int
    seed: int


@dataclass
class MatchState:
    """Mutable state for one simulated match."""

    minute: int = 0
    bayern_goals: int = 0
    psg_goals: int = 0
    bayern_xg: float = 0.0
    psg_xg: float = 0.0
    bayern_shots: int = 0
    psg_shots: int = 0
    bayern_sot: int = 0
    psg_sot: int = 0

    def aggregate_diff_bayern(self, first_leg: FirstLegData) -> int:
        """Return Bayern aggregate goals minus PSG aggregate goals."""

        return (first_leg.bayern_goals + self.bayern_goals) - (
            first_leg.psg_goals + self.psg_goals
        )


def planned_simulation_steps() -> list[str]:
    """Return the intended implementation steps."""

    return [
        "Load config and validate scenario weights.",
        "Sample match-level scenario states.",
        "Simulate regulation time in 15-minute blocks.",
        "Apply tactical, lineup, fatigue, and game-state modifiers per block.",
        "Sample open-play goals, penalty events, and system-transition events.",
        "Resolve qualification after 90 minutes.",
        "If needed, simulate extra time and penalties.",
        "Aggregate scoreline, path, and conditional scenario probabilities.",
        "Write reproducible JSON output.",
    ]

