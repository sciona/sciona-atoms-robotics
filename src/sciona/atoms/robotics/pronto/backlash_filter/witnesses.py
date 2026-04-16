from __future__ import annotations
from sciona.ghost.abstract import AbstractArray, AbstractDistribution, AbstractScalar, AbstractSignal

def witness_initialize_backlash_filter_state() -> AbstractArray:
    """Shape-and-type check for initialize backlash filter state. Returns output metadata without running the real computation."""
    return AbstractArray(shape=("S",), dtype="float64")

def witness_update_alpha_parameter(state_in: AbstractArray, alpha_in: AbstractArray) -> AbstractArray:
    """Shape-and-type check for update alpha parameter. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=state_in.shape,
        dtype="float64",)
    
    return result

def witness_update_crossing_time_maximum(state_in: AbstractArray, t_crossing_max_in: AbstractArray) -> AbstractArray:
    """Shape-and-type check for update crossing time maximum. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=state_in.shape,
        dtype="float64",)
    
    return result
