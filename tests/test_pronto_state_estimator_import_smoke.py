import importlib


def test_pronto_state_estimator_import_smoke() -> None:
    assert importlib.import_module("sciona.atoms.robotics.pronto.state_estimator") is not None
    assert importlib.import_module("sciona.probes.robotics.pronto_state_estimator") is not None
