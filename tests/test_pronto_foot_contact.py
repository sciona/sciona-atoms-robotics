from __future__ import annotations

from dataclasses import dataclass

from sciona.atoms.robotics.pronto.foot_contact.atoms import (
    foot_sensing_state_update,
    mode_snapshot_readout,
)


def test_foot_sensing_state_update_overwrites_requested_flags_without_mutation() -> None:
    initial = {"lfoot_sensing_": False, "rfoot_sensing_": True, "keep": True}
    command = {"lfoot_sensing_": True, "rfoot_sensing_": False}

    updated = foot_sensing_state_update(initial, command)

    assert updated == {"lfoot_sensing_": True, "rfoot_sensing_": False, "keep": True}
    assert initial == {"lfoot_sensing_": False, "rfoot_sensing_": True, "keep": True}
    assert updated is not initial


def test_mode_snapshot_readout_supports_mapping_inputs() -> None:
    mode, previous = mode_snapshot_readout({"mode": "stance", "previous_mode": "swing"})

    assert mode == "stance"
    assert previous == "swing"


@dataclass
class _ModeState:
    mode: str
    previous_mode: str


def test_mode_snapshot_readout_supports_attribute_based_state() -> None:
    mode, previous = mode_snapshot_readout(_ModeState(mode="contact", previous_mode="flight"))

    assert mode == "contact"
    assert previous == "flight"
