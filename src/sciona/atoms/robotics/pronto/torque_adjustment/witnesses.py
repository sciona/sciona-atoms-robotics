from __future__ import annotations

from sciona.ghost.abstract import AbstractArray, AbstractScalar


def witness_apply_torque_adjustment(
    names: AbstractArray,
    positions: AbstractArray,
    efforts: AbstractArray,
    joints_to_filter: AbstractArray,
    filter_gains: AbstractArray,
    max_adjustment: AbstractScalar,
) -> AbstractArray:
    """Return adjusted joint-position metadata."""
    del names, efforts, joints_to_filter, filter_gains, max_adjustment
    return AbstractArray(shape=positions.shape, dtype="float64")
