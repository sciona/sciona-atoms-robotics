from __future__ import annotations

import numpy as np

from sciona.atoms.robotics.pronto.yaw_lock.atoms import (
    configure_correction_and_yaw_slip_policy,
    initialize_yaw_lock_state,
    read_initial_joint_angles,
    read_robot_standing_status,
    set_joint_pose_and_initial_angles,
    set_robot_standing_status,
    set_standing_link_targets,
)


def test_initialize_yaw_lock_state_sets_expected_defaults() -> None:
    state = initialize_yaw_lock_state()

    assert state == {
        "correction_period": 1.0,
        "yaw_slip_detect": False,
        "yaw_slip_threshold_degrees": 5.0,
        "yaw_slip_disable_period": 1.0,
        "is_robot_standing": False,
        "joint_name": None,
        "joint_position": None,
        "joint_angles_init": None,
        "left_standing_link": None,
        "right_standing_link": None,
    }


def test_configure_correction_and_yaw_slip_policy_updates_only_policy_fields() -> None:
    state = initialize_yaw_lock_state()

    updated = configure_correction_and_yaw_slip_policy(state, 0.2, True, 3.5, 2.0)

    assert updated["correction_period"] == 0.2
    assert updated["yaw_slip_detect"] is True
    assert updated["yaw_slip_threshold_degrees"] == 3.5
    assert updated["yaw_slip_disable_period"] == 2.0
    assert updated["is_robot_standing"] is False
    assert updated["joint_name"] is None
    assert updated is not state


def test_standing_status_round_trips_through_set_and_read() -> None:
    state = initialize_yaw_lock_state()

    updated = set_robot_standing_status(state, True)

    assert read_robot_standing_status(updated) is True
    assert read_robot_standing_status(state) is False


def test_joint_pose_and_initial_angle_updates_are_persisted() -> None:
    state = initialize_yaw_lock_state()
    assert state["joint_angles_init"] is None

    names = ["hip", "knee"]
    positions = np.array([0.25, -0.4])
    init_angles = np.array([0.1, -0.2])

    updated = set_joint_pose_and_initial_angles(state, names, positions, init_angles)

    assert updated["joint_name"] == names
    assert np.allclose(updated["joint_position"], positions)
    assert np.allclose(read_initial_joint_angles(updated), init_angles)


def test_setstandinglinktargets_updates_only_link_fields() -> None:
    state = initialize_yaw_lock_state()

    updated = set_standing_link_targets(state, "left_foot", "right_foot")

    assert updated["left_standing_link"] == "left_foot"
    assert updated["right_standing_link"] == "right_foot"
    assert updated["joint_name"] is None
    assert updated is not state
