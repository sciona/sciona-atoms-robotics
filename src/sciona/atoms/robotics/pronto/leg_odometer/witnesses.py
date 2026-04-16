from __future__ import annotations
from sciona.ghost.abstract import AbstractArray

def witness_velocity_state_readout(state_in: AbstractArray) -> AbstractArray:
    """Describe the velocity-vector/covariance readout from immutable odometry state."""
    return AbstractArray(shape=("2",), dtype="tuple[ndarray,float64]")

def witness_pose_query_accessors() -> AbstractArray:
    """Describe the stateless position/orientation query surface."""
    return AbstractArray(shape=("6",), dtype="float64")
