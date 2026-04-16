from __future__ import annotations

import numpy as np

from sciona.atoms.robotics.pronto.dynamic_stance_estimator_d12.atoms import (
    stance_estimation,
    stance_state_init,
)


def test_stance_state_init_allocates_expected_buffers() -> None:
    state = stance_state_init({"n_legs": 4, "force_threshold": 42.0})

    assert np.array_equal(state["stance"], np.zeros(4, dtype=np.float64))
    assert np.array_equal(state["grf_history"], np.zeros(4, dtype=np.float64))
    assert float(state["force_threshold"][0]) == 42.0
    assert int(state["n_legs"][0]) == 4


def test_stance_estimation_thresholds_each_leg_without_mutating_input() -> None:
    state = stance_state_init({"n_legs": 4, "force_threshold": 50.0})
    original = {key: value.copy() for key, value in state.items()}
    observation = np.array([49.9, 50.0, 73.2, 12.5], dtype=np.float64)

    next_state, estimate = stance_estimation(state, observation)

    expected = np.array([0.0, 1.0, 1.0, 0.0], dtype=np.float64)
    assert np.array_equal(estimate, expected)
    assert np.array_equal(next_state["stance"], expected)
    assert np.array_equal(next_state["grf_history"], observation)
    for key, value in original.items():
        assert np.array_equal(state[key], value)
