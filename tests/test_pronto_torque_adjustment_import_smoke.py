import importlib


def test_pronto_torque_adjustment_import_smoke() -> None:
    assert importlib.import_module("sciona.atoms.robotics.pronto.torque_adjustment") is not None
    assert importlib.import_module("sciona.probes.robotics.pronto_torque_adjustment") is not None
