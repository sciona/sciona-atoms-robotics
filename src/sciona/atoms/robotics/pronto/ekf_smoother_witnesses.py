from __future__ import annotations

from sciona.ghost.abstract import AbstractArray


def witness_stateestimatorinit() -> AbstractArray:
    """Shape witness for the initialized state vector."""
    return AbstractArray(shape=(6,), dtype="float64")
