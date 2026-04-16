from __future__ import annotations

from sciona.ghost.abstract import AbstractArray, AbstractScalar


def witness_update_state_estimate(
    prior_state: AbstractArray,
    prior_cov: AbstractArray,
    measurement: AbstractArray,
    utime: AbstractScalar,
) -> AbstractArray:
    """Describe the updated state estimate after ingesting a measurement packet."""

    _ = prior_cov
    _ = measurement
    _ = utime
    return AbstractArray(shape=prior_state.shape, dtype="float64")
