import importlib


def test_pronto_yaw_lock_import_smoke() -> None:
    assert importlib.import_module("sciona.atoms.robotics.pronto.yaw_lock") is not None
    assert importlib.import_module("sciona.probes.robotics.pronto_yaw_lock") is not None
