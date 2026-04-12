import importlib


def test_pronto_flex_estimator_import_smoke() -> None:
    assert importlib.import_module("sciona.atoms.robotics.pronto.flex_estimator") is not None
    assert importlib.import_module("sciona.probes.robotics.pronto_flex_estimator") is not None
