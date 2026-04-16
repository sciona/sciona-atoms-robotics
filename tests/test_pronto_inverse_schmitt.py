from __future__ import annotations

import numpy as np

from sciona.atoms.robotics.pronto.inverse_schmitt import inverse_schmitt_trigger_transform


def test_inverse_schmitt_trigger_transform_toggles_only_at_threshold_crossings() -> None:
    signal = np.array([0.8, 0.6, 0.2, 0.5, 0.9, 0.4, 0.1], dtype=np.float64)
    observed = inverse_schmitt_trigger_transform(signal)
    expected = np.array([0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0], dtype=np.float64)
    np.testing.assert_array_equal(observed, expected)


def test_inverse_schmitt_trigger_transform_honors_custom_thresholds_and_prior_state() -> None:
    payload = {
        "signal": np.array([0.55, 0.45, 0.25, 0.6, 0.95], dtype=np.float64),
        "low_threshold": 0.3,
        "high_threshold": 0.8,
        "prev_output": True,
    }
    observed = inverse_schmitt_trigger_transform(payload)
    expected = np.array([1.0, 1.0, 1.0, 1.0, 0.0], dtype=np.float64)
    np.testing.assert_array_equal(observed, expected)
