from __future__ import annotations

import ctypes
from pathlib import Path
from typing import TypedDict

import icontract
import numpy as np

from sciona.ghost.registry import register_atom

from .witnesses import witness_initialize_state_estimator_state


class StateEstimatorState(TypedDict):
    x: np.ndarray
    P: np.ndarray
    A: np.ndarray
    Q: np.ndarray
    H: np.ndarray
    R: np.ndarray
    x_history: list[np.ndarray]
    P_history: list[np.ndarray]
    x_pred_history: list[np.ndarray]
    P_pred_history: list[np.ndarray]


@register_atom(witness_initialize_state_estimator_state)
@icontract.require(lambda: True, "no preconditions for zero-parameter initializer")
@icontract.ensure(lambda result: result is not None, "initialize_state_estimator_state output must not be None")
def initialize_state_estimator_state() -> StateEstimatorState:
    """Bootstrap a default EKF smoother state estimate bundle."""

    n = 6
    dt = 0.01

    x = np.zeros(n, dtype=np.float64)
    P = np.eye(n, dtype=np.float64) * 1e2
    A = np.eye(n, dtype=np.float64)
    A[0, 3] = dt
    A[1, 4] = dt
    A[2, 5] = dt
    Q = np.eye(n, dtype=np.float64) * 1e-3
    H = np.eye(n, dtype=np.float64)
    R = np.eye(n, dtype=np.float64) * 1e-1

    return {
        "x": x,
        "P": P,
        "A": A,
        "Q": Q,
        "H": H,
        "R": R,
        "x_history": [],
        "P_history": [],
        "x_pred_history": [],
        "P_pred_history": [],
    }


def _initialize_state_estimator_state_ffi() -> ctypes.c_void_p:
    lib_path = Path(__file__).with_name("stateestimatorinit.so")
    _lib = ctypes.CDLL(str(lib_path))
    _func = _lib["stateestimatorinit_prime"]
    _func.restype = ctypes.c_void_p
    return _func()
