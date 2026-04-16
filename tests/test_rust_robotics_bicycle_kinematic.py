from __future__ import annotations

import json

import numpy as np

from sciona.atoms.robotics.rust_robotics.bicycle_kinematic.atoms import (
    computelinearizedstatematrices,
    computesideslipangle,
    constructgeometrymodel,
    evaluateandinvertdynamics,
    loadmodelfromfile,
    querygeometryparameters,
)


def test_model_construction_and_queries_are_consistent() -> None:
    model = constructgeometrymodel(1.2, 1.6)

    assert model["lf"] == 1.2
    assert model["lr"] == 1.6
    assert model["L"] == 2.8
    assert querygeometryparameters(model) == (1.2, 1.6, 2.8)


def test_load_model_from_file_round_trips_geometry(tmp_path) -> None:
    path = tmp_path / "bike.json"
    path.write_text(json.dumps({"lf": 1.4, "lr": 1.1, "L": 2.5}))

    model = loadmodelfromfile(str(path))

    assert querygeometryparameters(model) == (1.4, 1.1, 2.5)


def test_sideslip_matches_closed_form_relation() -> None:
    model = constructgeometrymodel(1.2, 1.6)
    delta = 0.18

    beta = computesideslipangle(model, delta)

    expected = np.arctan(model["lr"] / model["L"] * np.tan(delta))
    assert np.isclose(beta, expected)


def test_linearization_matches_closed_form_bicycle_jacobians() -> None:
    model = constructgeometrymodel(1.2, 1.6)
    x = np.array([2.0, -1.0, 0.25, 8.0])
    u = np.array([0.12, 0.5])

    A, B = computelinearizedstatematrices(model, x, u)

    theta = x[2]
    v = x[3]
    delta = u[0]
    lr = model["lr"]
    L = model["L"]
    beta = np.arctan(lr / L * np.tan(delta))
    dbeta_ddelta = (lr / L) / (np.cos(delta) ** 2) / (1.0 + (lr / L * np.tan(delta)) ** 2)

    expected_A = np.zeros((4, 4))
    expected_A[0, 2] = -v * np.sin(theta + beta)
    expected_A[0, 3] = np.cos(theta + beta)
    expected_A[1, 2] = v * np.cos(theta + beta)
    expected_A[1, 3] = np.sin(theta + beta)
    expected_A[2, 3] = np.sin(beta) / lr

    expected_B = np.zeros((4, 2))
    expected_B[0, 0] = -v * np.sin(theta + beta) * dbeta_ddelta
    expected_B[1, 0] = v * np.cos(theta + beta) * dbeta_ddelta
    expected_B[2, 0] = v * np.cos(beta) * dbeta_ddelta / lr
    expected_B[3, 1] = 1.0

    assert np.allclose(A, expected_A)
    assert np.allclose(B, expected_B)


def test_forward_and_inverse_dynamics_are_internally_consistent() -> None:
    model = constructgeometrymodel(1.2, 1.6)
    x = np.array([0.0, 0.0, 0.35, 6.5])
    u = np.array([0.1, 1.25])
    desired = np.array([0.0, 0.0, 0.0, -0.75])

    x_dot, jacobian, inferred = evaluateandinvertdynamics(model, x, u, 0.0, desired)

    beta = np.arctan(model["lr"] / model["L"] * np.tan(u[0]))
    expected_x_dot = np.array(
        [
            x[3] * np.cos(x[2] + beta),
            x[3] * np.sin(x[2] + beta),
            x[3] * np.sin(beta) / model["lr"],
            u[1],
        ]
    )
    expected_jacobian = np.zeros((4, 4))
    expected_jacobian[0, 2] = -x[3] * np.sin(x[2] + beta)
    expected_jacobian[0, 3] = np.cos(x[2] + beta)
    expected_jacobian[1, 2] = x[3] * np.cos(x[2] + beta)
    expected_jacobian[1, 3] = np.sin(x[2] + beta)
    expected_jacobian[2, 3] = np.sin(beta) / model["lr"]

    assert np.allclose(x_dot, expected_x_dot)
    assert np.allclose(jacobian, expected_jacobian)
    assert np.allclose(inferred, np.array([u[0], desired[3]]))
