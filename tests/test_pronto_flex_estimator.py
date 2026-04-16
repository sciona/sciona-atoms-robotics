from __future__ import annotations

import numpy as np

from sciona.atoms.robotics.pronto.flex_estimator import estimate_flex_deflection


def test_estimate_flex_deflection_only_updates_stance_legs() -> None:
    hip_positions = np.zeros((4, 3), dtype=np.float64)
    hip_efforts = np.array([10.0, -5.0, 2.0, 1.5], dtype=np.float64)
    stance_mask = np.array([True, False, True, False], dtype=bool)
    observed = estimate_flex_deflection(hip_positions, hip_efforts, stance_mask)
    expected = np.array([0.01, 0.0, 0.002, 0.0], dtype=np.float64)
    np.testing.assert_allclose(observed, expected, rtol=1e-12, atol=1e-12)


def test_estimate_flex_deflection_preserves_signed_effort_scaling() -> None:
    hip_positions = np.ones((2, 3), dtype=np.float64)
    hip_efforts = np.array([-3.0, 4.5], dtype=np.float64)
    stance_mask = np.array([True, True], dtype=bool)
    observed = estimate_flex_deflection(hip_positions, hip_efforts, stance_mask)
    expected = np.array([-0.003, 0.0045], dtype=np.float64)
    np.testing.assert_allclose(observed, expected, rtol=1e-12, atol=1e-12)
