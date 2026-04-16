from __future__ import annotations

from sciona.ghost.abstract import AbstractArray


def witness_initialize_state_estimator_state() -> AbstractArray:
    """Shape witness for the initialized primary state vector."""
    return AbstractArray(shape=(6,), dtype="float64")
