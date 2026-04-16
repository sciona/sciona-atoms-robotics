from __future__ import annotations

import numpy as np

from sciona.atoms.robotics.pronto.leg_odometer.atoms import (
    pose_query_accessors,
    velocity_state_readout,
)


def test_velocity_state_readout_returns_velocity_and_covariance_without_mutation() -> None:
    state = {
        "xd_b": np.array([0.5, -1.2, 3.4], dtype=np.float64),
        "vel_cov": np.array(
            [[0.2, 0.01, 0.0], [0.01, 0.3, 0.02], [0.0, 0.02, 0.4]],
            dtype=np.float64,
        ),
    }
    snapshot = {key: value.copy() for key, value in state.items()}

    velocity, covariance = velocity_state_readout(state)

    assert np.array_equal(velocity, snapshot["xd_b"])
    assert np.array_equal(covariance, snapshot["vel_cov"])
    for key, value in snapshot.items():
        assert np.array_equal(state[key], value)


def test_pose_query_accessors_returns_identity_pose_defaults() -> None:
    pose = pose_query_accessors()

    assert np.array_equal(pose["position"], np.zeros(3, dtype=np.float64))
    assert np.array_equal(pose["orientation"], np.eye(3, dtype=np.float64))
