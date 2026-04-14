from __future__ import annotations

from sciona.ghost.abstract import AbstractArray


def witness_foot_sensing_state_update(
    foot_sensing_state_in: AbstractArray,
    sensor_packet: AbstractArray,
) -> AbstractArray:
    """Shape-and-type check for foot sensing state update. Returns output metadata without running the real computation."""
    _ = sensor_packet
    result = AbstractArray(
        shape=foot_sensing_state_in.shape,
        dtype="float64",)

    return result

def witness_mode_snapshot_readout(mode_state_in: AbstractArray) -> AbstractArray:
    """Describe the two-value mode snapshot returned from immutable state."""
    return AbstractArray(shape=("2",), dtype="tuple[hashable,hashable]")
