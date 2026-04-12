import importlib


def test_pronto_inverse_schmitt_import_smoke() -> None:
    assert importlib.import_module("sciona.atoms.robotics.pronto.inverse_schmitt") is not None
    assert importlib.import_module("sciona.probes.robotics.pronto_inverse_schmitt") is not None
