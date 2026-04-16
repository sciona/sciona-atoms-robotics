from __future__ import annotations
from sciona.ghost.abstract import AbstractArray, AbstractDistribution, AbstractScalar, AbstractSignal

def witness_initialize_yaw_lock_state() -> AbstractArray:
    """Shape-and-type check for initialize yaw lock state. Returns output metadata without running the real computation."""
    return AbstractArray(shape=("S",), dtype="float64")

def witness_configure_correction_and_yaw_slip_policy(state_in: AbstractArray, correction_period_in: AbstractArray, yaw_slip_detect_in: AbstractArray, yaw_slip_threshold_degrees_in: AbstractArray, yaw_slip_disable_period_in: AbstractArray) -> AbstractArray:
    """Shape-and-type check for configure correction and yaw slip policy. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=state_in.shape,
        dtype="float64",)
    
    return result

def witness_set_robot_standing_status(state_in: AbstractArray, is_robot_standing_in: AbstractArray) -> AbstractArray:
    """Shape-and-type check for set robot standing status. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=state_in.shape,
        dtype="float64",)
    
    return result

def witness_read_robot_standing_status(state_in: AbstractArray) -> AbstractArray:
    """Shape-and-type check for read robot standing status. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=state_in.shape,
        dtype="float64",)
    
    return result

def witness_set_joint_pose_and_initial_angles(state_in: AbstractArray, joint_name_in: AbstractArray, joint_position_in: AbstractArray, joint_angles_init_in: AbstractArray) -> AbstractArray:
    """Shape-and-type check for set joint pose and initial angles. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=state_in.shape,
        dtype="float64",)
    
    return result

def witness_read_initial_joint_angles(state_in: AbstractArray) -> AbstractArray:
    """Shape-and-type check for read initial joint angles. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=state_in.shape,
        dtype="float64",)
    
    return result

def witness_set_standing_link_targets(state_in: AbstractArray, left_standing_link_in: AbstractArray, right_standing_link_in: AbstractArray) -> AbstractArray:
    """Shape-and-type check for set standing link targets. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=state_in.shape,
        dtype="float64",)
    
    return result
