from __future__ import annotations

from sciona.ghost.abstract import AbstractArray, AbstractSignal


def witness_inverse_schmitt_trigger_transform(input_signal: AbstractArray) -> AbstractArray:
    """Shape-and-type check for inverse_schmitt_trigger_transform."""

    return AbstractSignal(
        shape=input_signal.shape,
        dtype="float64",
        sampling_rate=getattr(input_signal, "sampling_rate_prime", 44100.0),
        domain="time",
    )
