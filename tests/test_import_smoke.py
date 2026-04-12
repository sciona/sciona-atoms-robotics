import importlib

def test_robotics_import_smoke() -> None:
    assert importlib.import_module("sciona.atoms.robotics.rust_robotics") is not None
    assert importlib.import_module("sciona.probes.robotics.rust_robotics") is not None
