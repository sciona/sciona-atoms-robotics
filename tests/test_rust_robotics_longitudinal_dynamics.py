from __future__ import annotations

import json

import numpy as np

from sciona.atoms.robotics.rust_robotics.longitudinal_dynamics.atoms import (
    compute_aerodynamic_force,
    compute_gravity_grade_force,
    compute_rolling_force,
    deserialize_model_spec,
    evaluate_dynamics_derivatives,
    initialize_model,
    linearize_dynamics,
    solve_control_for_target_derivative,
)


def test_force_terms_match_closed_form_vehicle_model() -> None:
    initialize_model(1500.0, 2.2)
    velocity = 10.0
    grade = 0.1

    aero = compute_aerodynamic_force(velocity)
    rolling = compute_rolling_force(grade)
    gravity = compute_gravity_grade_force(grade)

    assert np.isclose(aero, 0.5 * 1.225 * 0.3 * 2.2 * velocity**2)
    assert np.isclose(rolling, 1500.0 * 9.81 * 0.01 * np.cos(grade))
    assert np.isclose(gravity, 1500.0 * 9.81 * np.sin(grade))


def test_dynamics_and_linearization_are_internally_consistent() -> None:
    initialize_model(1500.0, 2.2)
    x = np.array([0.0, 12.0])
    u = np.array([2500.0, 0.05])

    x_dot = evaluate_dynamics_derivatives(x, u, 0.0)
    jac = linearize_dynamics(x, u, 0.0)

    expected_drag = 0.5 * 1.225 * 0.3 * 2.2 * x[1] ** 2
    expected_roll = 1500.0 * 9.81 * 0.01 * np.cos(u[1])
    expected_grade = 1500.0 * 9.81 * np.sin(u[1])
    expected_accel = (u[0] - expected_drag - expected_roll - expected_grade) / 1500.0

    assert np.allclose(x_dot, np.array([x[1], expected_accel]))
    assert np.allclose(jac, np.array([[0.0, 1.0], [0.0, -(1.225 * 0.3 * 2.2 * x[1]) / 1500.0]]))


def test_inverse_control_recovers_requested_acceleration() -> None:
    initialize_model(1500.0, 2.2)
    x = np.array([5.0, 8.0])
    desired = np.array([8.0, 1.5])

    control = solve_control_for_target_derivative(x, desired, 0.0)
    realized = evaluate_dynamics_derivatives(x, control, 0.0)

    assert np.allclose(realized, desired)
    assert control.shape == (2,)


def test_deserialize_model_spec_loads_and_updates_model(tmp_path) -> None:
    spec_path = tmp_path / 'model.json'
    spec_path.write_text(json.dumps({'mass': 1200.0, 'area_frontal': 1.9}))

    model = deserialize_model_spec(str(spec_path))

    assert model['mass'] == 1200.0
    assert model['area_frontal'] == 1.9
    assert np.isclose(compute_aerodynamic_force(10.0), 0.5 * 1.225 * 0.3 * 1.9 * 100.0)
