import importlib


def test_pronto_foot_contact_import_smoke() -> None:
    assert importlib.import_module("sciona.atoms.robotics.pronto.foot_contact") is not None
    assert importlib.import_module("sciona.probes.robotics.pronto_foot_contact") is not None
