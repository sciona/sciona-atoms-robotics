from __future__ import annotations

import numpy as np

from sciona.atoms.robotics.pronto.dynamic_stance_estimator.atoms import (
    initialize_filter,
    predict_step,
    query_stance,
    update_step,
)


def _example_model():
    initial_x = np.array([[1.0], [0.5]])
    initial_p = np.array([[2.0, 0.1], [0.1, 1.5]])
    a = np.array([[1.0, 1.0], [0.0, 1.0]])
    h = np.array([[1.0, 0.0]])
    q = np.array([[0.2, 0.0], [0.0, 0.1]])
    r = np.array([[0.5]])
    return initial_x, initial_p, a, h, q, r


def test_initialize_filter_preserves_state_and_model_parameters() -> None:
    initial_x, initial_p, a, h, q, r = _example_model()

    state, params = initialize_filter(initial_x, initial_p, a, h, q, r)

    assert np.allclose(state["x"], initial_x)
    assert np.allclose(state["P"], initial_p)
    assert np.allclose(params["A"], a)
    assert np.allclose(params["H"], h)
    assert np.allclose(params["Q"], q)
    assert np.allclose(params["R"], r)
    assert state["x"] is not initial_x
    assert params["A"] is not a


def test_predict_step_matches_linear_kalman_prediction() -> None:
    initial_x, initial_p, a, h, q, r = _example_model()
    state, params = initialize_filter(initial_x, initial_p, a, h, q, r)

    predicted = predict_step(state, params, 0.1)

    expected_x = a @ initial_x
    expected_p = a @ initial_p @ a.T + q
    assert np.allclose(predicted["x"], expected_x)
    assert np.allclose(predicted["P"], expected_p)


def test_update_step_matches_standard_kalman_correction() -> None:
    initial_x, initial_p, a, h, q, r = _example_model()
    state, params = initialize_filter(initial_x, initial_p, a, h, q, r)
    predicted = predict_step(state, params, 0.1)
    z = np.array([[1.4]])

    updated = update_step(predicted, params, z)

    innovation = z - h @ predicted["x"]
    s = h @ predicted["P"] @ h.T + r
    k = predicted["P"] @ h.T @ np.linalg.inv(s)
    expected_x = predicted["x"] + k @ innovation
    expected_p = (np.eye(predicted["x"].shape[0]) - k @ h) @ predicted["P"]
    assert np.allclose(updated["x"], expected_x)
    assert np.allclose(updated["P"], expected_p)


def test_query_stance_returns_first_state_component() -> None:
    initial_x, initial_p, a, h, q, r = _example_model()
    state, params = initialize_filter(initial_x, initial_p, a, h, q, r)
    predicted = predict_step(state, params, 0.1)

    assert np.isclose(query_stance(predicted), float(predicted["x"].reshape(-1)[0]))
