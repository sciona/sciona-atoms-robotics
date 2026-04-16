from __future__ import annotations

import numpy as np
import icontract

from sciona.ghost.registry import register_atom

from .witnesses import witness_estimate_flex_deflection


@register_atom(witness_estimate_flex_deflection)
@icontract.require(lambda hip_positions: hip_positions.ndim >= 1, "hip_positions must have at least one dimension")
@icontract.require(lambda hip_efforts: hip_efforts.ndim >= 1, "hip_efforts must have at least one dimension")
@icontract.require(lambda stance_mask: stance_mask.ndim >= 1, "stance_mask must have at least one dimension")
@icontract.require(lambda hip_positions: hip_positions is not None, "hip_positions cannot be None")
@icontract.require(lambda hip_positions: isinstance(hip_positions, np.ndarray), "hip_positions must be np.ndarray")
@icontract.require(lambda hip_efforts: hip_efforts is not None, "hip_efforts cannot be None")
@icontract.require(lambda hip_efforts: isinstance(hip_efforts, np.ndarray), "hip_efforts must be np.ndarray")
@icontract.require(lambda stance_mask: stance_mask is not None, "stance_mask cannot be None")
@icontract.require(lambda stance_mask: isinstance(stance_mask, np.ndarray), "stance_mask must be np.ndarray")
@icontract.ensure(lambda result: isinstance(result, np.ndarray), "result must be np.ndarray")
@icontract.ensure(lambda result: result is not None, "result must not be None")
def estimate_flex_deflection(
    hip_positions: np.ndarray,
    hip_efforts: np.ndarray,
    stance_mask: np.ndarray,
) -> np.ndarray:
    """Estimate per-leg flex deflection from hip effort on stance legs."""

    _ = hip_positions
    compliance = 1e-3
    deflection = np.zeros(hip_efforts.shape[0], dtype=np.float64)
    for index in range(hip_efforts.shape[0]):
        if stance_mask[index]:
            deflection[index] = compliance * hip_efforts[index]
    return deflection
