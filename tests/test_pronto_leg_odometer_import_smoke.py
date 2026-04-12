import importlib


def test_pronto_leg_odometer_import_smoke() -> None:
    assert importlib.import_module("sciona.atoms.robotics.pronto.leg_odometer") is not None
    assert importlib.import_module("sciona.probes.robotics.pronto_leg_odometer") is not None
