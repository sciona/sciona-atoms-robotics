from __future__ import annotations

from sciona.ghost.abstract import AbstractArray


def witness_estimate_flex_deflection(
    hip_positions: AbstractArray,
    hip_efforts: AbstractArray,
    stance_mask: AbstractArray,
) -> AbstractArray:
    """Describe the estimated flex deflection from hip effort on stance legs."""

    _ = hip_positions
    _ = stance_mask
    return AbstractArray(shape=hip_efforts.shape, dtype="float64")
