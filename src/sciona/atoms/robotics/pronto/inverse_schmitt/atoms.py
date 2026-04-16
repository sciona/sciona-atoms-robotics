from __future__ import annotations

from collections.abc import Mapping
import ctypes
from pathlib import Path

import icontract
import numpy as np

from sciona.ghost.registry import register_atom

from .witnesses import witness_inverse_schmitt_trigger_transform


@register_atom(witness_inverse_schmitt_trigger_transform)  # type: ignore[untyped-decorator, name-defined]
@icontract.require(lambda input_signal: input_signal is not None, "input_signal cannot be None")
@icontract.ensure(lambda result: result is not None, "inverse_schmitt_trigger_transform output must not be None")
def inverse_schmitt_trigger_transform(input_signal: np.ndarray | Mapping[str, object]) -> np.ndarray:
    """Apply an inverse Schmitt trigger with hysteresis to a 1D signal."""

    if isinstance(input_signal, Mapping):
        signal = np.asarray(input_signal.get("signal", []), dtype=np.float64)
        low_thresh = float(input_signal.get("low_threshold", 0.3))
        high_thresh = float(input_signal.get("high_threshold", 0.7))
        prev_output = bool(input_signal.get("prev_output", False))
    else:
        signal = np.atleast_1d(np.asarray(input_signal, dtype=np.float64))
        low_thresh, high_thresh = 0.3, 0.7
        prev_output = False

    output = np.empty(signal.shape, dtype=np.float64)
    state = prev_output
    for index, sample in enumerate(signal):
        if sample <= low_thresh:
            state = True
        elif sample >= high_thresh:
            state = False
        output[index] = float(state)
    return output


def _inverse_schmitt_trigger_transform_ffi(input_signal: ctypes.c_void_p) -> ctypes.c_void_p:
    """Wrapper that calls the C++ version of inverse_schmitt_trigger_transform."""

    lib_path = Path(__file__).with_name("inverse_schmitt_trigger_transform.so")
    _lib = ctypes.CDLL(str(lib_path))
    _func = _lib["inverse_schmitt_trigger_transform_prime"]
    _func.argtypes = [ctypes.c_void_p]
    _func.restype = ctypes.c_void_p
    return ctypes.c_void_p(_func(input_signal))
