from __future__ import annotations

import icontract
import numpy as np

from sciona.ghost.registry import register_atom

from .witnesses import witness_update_state_estimate


@register_atom(witness_update_state_estimate)
@icontract.require(lambda prior_state: prior_state.ndim >= 1, "prior_state must have at least one dimension")
@icontract.require(lambda prior_cov: prior_cov.ndim >= 1, "prior_cov must have at least one dimension")
@icontract.require(lambda measurement: measurement.ndim >= 1, "measurement must have at least one dimension")
@icontract.require(lambda prior_state: prior_state is not None, "prior_state cannot be None")
@icontract.require(lambda prior_state: isinstance(prior_state, np.ndarray), "prior_state must be np.ndarray")
@icontract.require(lambda prior_cov: prior_cov is not None, "prior_cov cannot be None")
@icontract.require(lambda prior_cov: isinstance(prior_cov, np.ndarray), "prior_cov must be np.ndarray")
@icontract.require(lambda measurement: measurement is not None, "measurement cannot be None")
@icontract.require(lambda measurement: isinstance(measurement, np.ndarray), "measurement must be np.ndarray")
@icontract.require(lambda utime: utime is not None, "utime cannot be None")
@icontract.ensure(lambda result: isinstance(result, np.ndarray), "result must be np.ndarray")
@icontract.ensure(lambda result: result is not None, "result must not be None")
def update_state_estimate(
    prior_state: np.ndarray,
    prior_cov: np.ndarray,
    measurement: np.ndarray,
    utime: int,
) -> np.ndarray:
    """Fuse a measurement into the RBIS state using an EKF-style linear update."""

    _ = utime
    n_state = prior_state.shape[0]
    n_meas = measurement.shape[0]
    H = np.eye(n_meas, n_state, dtype=np.float64)
    R = np.eye(n_meas, dtype=np.float64) * 1e-2
    innovation = measurement - H @ prior_state
    S = H @ prior_cov @ H.T + R
    K = prior_cov @ H.T @ np.linalg.inv(S)
    return prior_state + K @ innovation
