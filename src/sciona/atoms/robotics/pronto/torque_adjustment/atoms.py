from __future__ import annotations

"""Torque-based joint-position adjustment atoms from Pronto."""

from collections.abc import Sequence
import math

import icontract

from sciona.ghost.registry import register_atom

from .witnesses import witness_apply_torque_adjustment


JointNames = Sequence[str]
ScalarVector = Sequence[float]


def _finite_vector(values: ScalarVector) -> bool:
    return all(math.isfinite(float(value)) for value in values)


def _joint_inputs_are_aligned(
    names: JointNames,
    positions: ScalarVector,
    efforts: ScalarVector,
) -> bool:
    return len(names) == len(positions) == len(efforts)


def _filter_inputs_are_aligned(joints_to_filter: JointNames, filter_gains: ScalarVector) -> bool:
    return len(joints_to_filter) == len(filter_gains)


def _limit_adjustment(value: float, max_adjustment: float) -> float:
    return max(-max_adjustment, min(max_adjustment, value))


@register_atom(witness_apply_torque_adjustment)
@icontract.require(lambda names, positions, efforts: _joint_inputs_are_aligned(names, positions, efforts), "joint names, positions, and efforts must align")
@icontract.require(lambda positions: _finite_vector(positions), "positions must be finite")
@icontract.require(lambda efforts: _finite_vector(efforts), "efforts must be finite")
@icontract.require(lambda joints_to_filter, filter_gains: _filter_inputs_are_aligned(joints_to_filter, filter_gains), "filtered joints and gains must align")
@icontract.require(lambda max_adjustment: math.isfinite(max_adjustment) and max_adjustment > 0.0, "max_adjustment must be a positive finite scalar")
@icontract.ensure(lambda result, positions: len(result) == len(positions), "adjusted positions must preserve joint count")
@icontract.ensure(lambda result: all(math.isfinite(value) for value in result), "adjusted positions must be finite")
def apply_torque_adjustment(
    names: JointNames,
    positions: ScalarVector,
    efforts: ScalarVector,
    joints_to_filter: JointNames,
    filter_gains: ScalarVector,
    max_adjustment: float = 0.1,
) -> list[float]:
    """Apply Pronto's effort-over-gain joint-position correction.

    The upstream `TorqueAdjustment::processSample` subtracts a clamped
    `effort / gain` correction from each configured joint position. Gains that
    are zero, infinite, or not-a-number disable adjustment for that joint.
    """
    adjusted = [float(position) for position in positions]
    name_to_index = {name: index for index, name in enumerate(names)}

    for joint_name, gain in zip(joints_to_filter, filter_gains, strict=True):
        if joint_name not in name_to_index:
            raise ValueError(f"filtered joint {joint_name!r} is not present in names")
        gain_value = float(gain)
        if not (math.isfinite(gain_value) and gain_value != 0.0):
            continue
        index = name_to_index[joint_name]
        correction = _limit_adjustment(float(efforts[index]) / gain_value, max_adjustment)
        adjusted[index] -= correction

    return adjusted
