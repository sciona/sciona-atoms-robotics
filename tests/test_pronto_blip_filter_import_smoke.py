import importlib


def test_pronto_blip_filter_import_smoke() -> None:
    assert importlib.import_module("sciona.atoms.robotics.pronto.blip_filter") is not None
    assert importlib.import_module("sciona.probes.robotics.pronto_blip_filter") is not None
