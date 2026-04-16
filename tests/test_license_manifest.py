from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "licenses" / "provider_license.json"


def test_robotics_license_manifest_is_repo_defaulted_and_complete_for_slice() -> None:
    data = json.loads(MANIFEST.read_text())

    assert data["provider_repo"] == "sciona-atoms-robotics"
    assert data["repository_default"]["license_expression"] == "NOASSERTION"
    assert data["repository_default"]["status"] == "unknown"
    assert data["family_overrides"] == []
    assert data["scope"] == ["robotics.pronto", "robotics.rust_robotics"]

    families = [entry["family"] for entry in data["family_inventory"]]
    assert families == ["robotics.pronto", "robotics.rust_robotics"]
    for entry in data["family_inventory"]:
        assert entry["license_expression"] == "NOASSERTION"
        assert entry["status"] == "unknown"
        assert entry["authoritative_sources"] == [f"src/sciona/atoms/{entry['family'].replace('.', '/')}"]

    assert data["unresolved_families"] == []
