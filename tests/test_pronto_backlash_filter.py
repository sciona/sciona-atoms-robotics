from __future__ import annotations

import numpy as np

from sciona.atoms.robotics.pronto.backlash_filter.atoms import (
    initialize_backlash_filter_state,
    update_alpha_parameter,
    update_crossing_time_maximum,
)


def test_initialize_backlash_filter_state_returns_default_state() -> None:
    state = initialize_backlash_filter_state()

    assert np.array_equal(state, np.array([0.5, 1.0, 0.0, 0.0], dtype=np.float64))


def test_update_alpha_parameter_only_changes_alpha_slot() -> None:
    state = initialize_backlash_filter_state()
    updated = update_alpha_parameter(state, 0.75)

    assert updated[0] == 0.75
    assert np.array_equal(updated[1:], state[1:])
    assert np.array_equal(state, np.array([0.5, 1.0, 0.0, 0.0], dtype=np.float64))


def test_update_crossing_time_maximum_only_changes_threshold_slot() -> None:
    state = initialize_backlash_filter_state()
    updated = update_crossing_time_maximum(state, 2.5)

    assert updated[1] == 2.5
    assert updated[0] == state[0]
    assert np.array_equal(updated[2:], state[2:])
