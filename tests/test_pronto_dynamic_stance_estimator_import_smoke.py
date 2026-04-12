import importlib


def test_pronto_dynamic_stance_estimator_import_smoke() -> None:
    assert importlib.import_module("sciona.atoms.robotics.pronto.dynamic_stance_estimator") is not None
    assert importlib.import_module("sciona.probes.robotics.pronto_dynamic_stance_estimator") is not None
