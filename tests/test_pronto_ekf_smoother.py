from __future__ import annotations

import numpy as np

from sciona.atoms.robotics.pronto.ekf_smoother import initialize_state_estimator_state


def test_initialize_state_estimator_state_builds_expected_shapes_and_histories() -> None:
    state = initialize_state_estimator_state()
    assert state["x"].shape == (6,)
    assert state["P"].shape == (6, 6)
    assert state["A"].shape == (6, 6)
    assert state["Q"].shape == (6, 6)
    assert state["H"].shape == (6, 6)
    assert state["R"].shape == (6, 6)
    assert state["x_history"] == []
    assert state["P_history"] == []
    assert state["x_pred_history"] == []
    assert state["P_pred_history"] == []


def test_initialize_state_estimator_state_uses_expected_defaults() -> None:
    state = initialize_state_estimator_state()
    np.testing.assert_allclose(state["x"], np.zeros(6, dtype=np.float64))
    np.testing.assert_allclose(np.diag(state["P"]), np.full(6, 1e2, dtype=np.float64))
    np.testing.assert_allclose(np.diag(state["Q"]), np.full(6, 1e-3, dtype=np.float64))
    np.testing.assert_allclose(np.diag(state["R"]), np.full(6, 1e-1, dtype=np.float64))
    assert state["A"][0, 3] == 0.01
    assert state["A"][1, 4] == 0.01
    assert state["A"][2, 5] == 0.01
    assert np.allclose(state["H"], np.eye(6, dtype=np.float64))
