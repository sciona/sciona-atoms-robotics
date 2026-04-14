from __future__ import annotations

from sciona.ghost.abstract import AbstractArray, AbstractDistribution, AbstractScalar, AbstractSignal


def witness_update_state_estimate(
    prior_state: AbstractArray,
    measurement_packet: AbstractArray,
) -> AbstractArray:
    """Describe the updated state estimate after ingesting a measurement packet."""
    _ = measurement_packet
    result = AbstractArray(
        shape=prior_state.shape,
        dtype="float64",)

    return result
