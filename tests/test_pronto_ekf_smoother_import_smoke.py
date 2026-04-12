import importlib


def test_pronto_ekf_smoother_import_smoke() -> None:
    assert importlib.import_module("sciona.atoms.robotics.pronto.ekf_smoother") is not None
    assert importlib.import_module("sciona.probes.robotics.pronto_ekf_smoother") is not None
