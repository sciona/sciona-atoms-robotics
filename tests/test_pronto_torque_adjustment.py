from __future__ import annotations

import pytest

from sciona.atoms.robotics.pronto.torque_adjustment import apply_torque_adjustment


def test_apply_torque_adjustment_matches_pronto_effort_over_gain_correction() -> None:
    result = apply_torque_adjustment(
        names=["hip", "knee", "ankle"],
        positions=[1.0, 2.0, 3.0],
        efforts=[0.2, -0.5, 10.0],
        joints_to_filter=["hip", "knee", "ankle"],
        filter_gains=[10.0, 5.0, 20.0],
    )

    assert result == pytest.approx([0.98, 2.1, 2.9])


def test_apply_torque_adjustment_skips_zero_and_infinite_gains() -> None:
    result = apply_torque_adjustment(
        names=["hip", "knee"],
        positions=[1.0, 2.0],
        efforts=[5.0, 5.0],
        joints_to_filter=["hip", "knee"],
        filter_gains=[0.0, float("inf")],
    )

    assert result == [1.0, 2.0]


def test_apply_torque_adjustment_rejects_missing_filter_joint() -> None:
    with pytest.raises(ValueError, match="not present"):
        apply_torque_adjustment(
            names=["hip"],
            positions=[1.0],
            efforts=[0.1],
            joints_to_filter=["ankle"],
            filter_gains=[10.0],
        )
