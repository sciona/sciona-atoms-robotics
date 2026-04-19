from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "src" / "sciona" / "atoms" / "robotics"
PRONTO_ROOT = ROOT / "pronto"
RUST_ROOT = ROOT / "rust_robotics"


def _expected_atom_keys(family_root: Path) -> set[str]:
    keys: set[str] = set()
    for refs_path in sorted(family_root.rglob("references.json")):
        data = json.loads(refs_path.read_text())
        keys.update(data.get("atoms", {}).keys())
    return keys


def _assert_bundle(bundle_path: Path, family: str, provider_repo: str, family_root: Path, has_uncertainty_summaries: bool) -> None:
    bundle = json.loads(bundle_path.read_text())
    expected_keys = _expected_atom_keys(family_root)

    assert bundle["family"] == family
    assert bundle["provider_repo"] == provider_repo
    assert bundle["review_status"] == "partial"
    assert bundle["trust_readiness"] == "blocked_on_uncertainty_backfill"
    assert len(bundle["rows"]) == len(expected_keys)
    assert {row["atom_fqdn"] for row in bundle["rows"]} == expected_keys

    if has_uncertainty_summaries:
        assert any(summary["has_uncertainty"] for summary in bundle["subfamily_summaries"])

    summaries = {summary["subfamily"]: summary for summary in bundle["subfamily_summaries"]}
    for idx, row in enumerate(bundle["rows"]):
        assert row["review_record_path"] == f"src/sciona/atoms/{family.replace('.', '/')}/review_bundle.json#rows[{idx}]"
        assert row["source_path"].startswith(f"sciona/atoms/{family.replace('.', '/')}/")
        assert row["review_status"] == "reviewed"
        assert row["semantic_verdict"] == "publishable_candidate"
        assert row["authoritative_sources"][0].startswith(f"src/sciona/atoms/{family.replace('.', '/')}/")
        assert row["authoritative_sources"][1].endswith("cdg.json")
        has_matches = any(source.endswith("matches.json") for source in row["authoritative_sources"])
        if row["subfamily"] == family.split(".", 1)[1] or not summaries[row["subfamily"]]["has_matches"]:
            assert not has_matches
        else:
            assert has_matches


def test_pronto_review_bundle_covers_all_rows() -> None:
    _assert_bundle(PRONTO_ROOT / "review_bundle.json", "robotics.pronto", "sciona-atoms-robotics", PRONTO_ROOT, True)


def test_rust_robotics_review_bundle_covers_all_rows() -> None:
    _assert_bundle(RUST_ROOT / "review_bundle.json", "robotics.rust_robotics", "sciona-atoms-robotics", RUST_ROOT, True)
