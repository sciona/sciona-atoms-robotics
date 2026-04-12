import importlib


def test_pronto_backlash_filter_import_smoke() -> None:
    assert importlib.import_module("sciona.atoms.robotics.pronto.backlash_filter") is not None
    assert importlib.import_module("sciona.probes.robotics.pronto_backlash_filter") is not None
