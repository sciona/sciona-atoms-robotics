import importlib


def test_pronto_dynamic_stance_estimator_d12_import_smoke() -> None:
    assert importlib.import_module("sciona.atoms.robotics.pronto.dynamic_stance_estimator_d12") is not None
    assert importlib.import_module("sciona.probes.robotics.pronto_dynamic_stance_estimator_d12") is not None
