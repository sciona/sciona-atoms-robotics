from __future__ import annotations

from sciona.ghost.abstract import AbstractArray, AbstractDistribution, AbstractScalar, AbstractSignal


def witness_initialize_filter(
    family: object,
    event_shape: object,
) -> AbstractDistribution:
    """Shape-and-type check for prior init: initialize filter. Returns output metadata without running the real computation."""
    return AbstractDistribution(
        family=family,
        event_shape=event_shape,)


def witness_predict_step(current_state: AbstractArray, model_params: AbstractArray, dt: AbstractArray) -> AbstractArray:
    """Shape-and-type check for predict step. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=current_state.shape,
        dtype="float64",)

    return result

def witness_update_step(prior: AbstractDistribution, likelihood: AbstractDistribution, data_shape: tuple[int, ...]) -> AbstractDistribution:
    """Shape-and-type check for posterior update: update step. Returns output metadata without running the real computation."""
    prior.assert_conjugate_to(likelihood)
    return AbstractDistribution(
        family=prior.family,
        event_shape=prior.event_shape,
        batch_shape=prior.batch_shape,
        support_lower=prior.support_lower,
        support_upper=prior.support_upper,
        is_discrete=prior.is_discrete,
    )

def witness_query_stance(current_state: AbstractArray) -> AbstractArray:
    """Shape-and-type check for query stance. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=current_state.shape,
        dtype="float64",)

    return result
