from __future__ import annotations

import numpy as np

from sciona.atoms.robotics.pronto.state_estimator import update_state_estimate


def test_update_state_estimate_matches_closed_form_identity_measurement_update() -> None:
    prior_state = np.array([0.0, 0.0], dtype=np.float64)
    prior_cov = np.eye(2, dtype=np.float64)
    measurement = np.array([1.0, -2.0], dtype=np.float64)
    observed = update_state_estimate(prior_state, prior_cov, measurement, 123)
    expected = np.array([1.0, -2.0], dtype=np.float64) * (1.0 / 1.01)
    np.testing.assert_allclose(observed, expected, rtol=1e-10, atol=1e-10)


def test_update_state_estimate_respects_nonzero_prior_state() -> None:
    prior_state = np.array([1.5], dtype=np.float64)
    prior_cov = np.array([[2.0]], dtype=np.float64)
    measurement = np.array([0.5], dtype=np.float64)
    observed = update_state_estimate(prior_state, prior_cov, measurement, 456)
    kalman_gain = 2.0 / (2.0 + 0.01)
    expected = np.array([1.5 + kalman_gain * (0.5 - 1.5)], dtype=np.float64)
    np.testing.assert_allclose(observed, expected, rtol=1e-10, atol=1e-10)
