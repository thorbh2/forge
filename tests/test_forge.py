"""Executable Forge V2 source, milestone, risk, consensus, and fallback tests."""

import json
from pathlib import Path


CONTRACT = str(Path(__file__).resolve().parents[1] / "contracts" / "forge_v2.py")


def _deploy_record(deploy, vm, owner):
    vm.warp("2026-07-16T12:00:00Z")
    vm.sender = owner
    contract = deploy(CONTRACT)
    record_id = str(contract.create_idea(
        "Validator toolkit",
        "A scoped public build plan with measurable acceptance criteria.",
        "https://example.com/spec",
        "tooling",
    ))
    contract.add_spec_source(record_id, "https://example.org/market", "market", "Demand evidence")
    contract.add_milestone(record_id, "Public alpha", "https://example.org/acceptance", "six weeks")
    contract.add_risk(record_id, "External API availability", "https://example.org/risk")
    return contract, record_id


def _mock_review(vm):
    vm.mock_llm(
        r"Forge V2, a pragmatic",
        json.dumps({
            "verdict": "greenlit", "score": 86, "confidenceBps": 8500,
            "feasibilityBps": 8200, "marketBps": 7600, "executionRiskBps": 2100,
            "summary": "The evidence, milestone and risk register support a bounded build.",
            "rationale": "Acceptance evidence is explicit and the disclosed risk is manageable.",
            "recommendedNextStep": "fund_public_alpha", "riskFlags": [], "sourceScores": [],
        }),
    )


def _mock_ruling(vm, pattern, ruling, revised):
    vm.mock_llm(
        pattern,
        json.dumps({
            "ruling": ruling, "revisedVerdict": revised,
            "confidenceDeltaBps": -1100 if revised == "shelved" else 900,
            "scoreDelta": -20 if revised == "shelved" else 18,
            "reason": "The filing provides controlling public evidence.", "riskFlags": [],
        }),
    )


def test_consensus_covers_every_final_record_field():
    source = Path(CONTRACT).read_text(encoding="utf-8")
    assert "verdict, score, confidenceBps, feasibilityBps, marketBps, executionRiskBps" in source
    assert "riskFlags, recommendedNextStep and every sourceScores entry are exactly identical" in source
    assert "ruling, revisedVerdict, scoreDelta, confidenceDeltaBps and riskFlags are exactly identical" in source


def test_full_v2_workflow_and_permissionless_dispute_resolution(
    deploy, direct_vm, direct_alice, direct_bob
):
    contract, record_id = _deploy_record(deploy, direct_vm, direct_alice)
    _mock_review(direct_vm)
    contract.review_idea_with_genlayer(record_id)
    record = json.loads(contract.get_idea_record(record_id))
    assert record["status"] == "CHALLENGE_WINDOW"
    assert len(record["sourceIds"]) == 2
    assert len(record["milestoneIds"]) == 1
    assert len(record["riskIds"]) == 1

    direct_vm.sender = direct_bob
    challenge_id = contract.submit_challenge(
        record_id, "A material dependency is unavailable.", "https://example.org/challenge"
    )
    _mock_ruling(direct_vm, r"Forge V2 challenge", "accepted", "shelved")
    contract.resolve_challenge_with_genlayer(record_id, challenge_id)
    assert json.loads(contract.get_idea_record(record_id))["verdict"] == "shelved"

    appeal_id = contract.submit_appeal(
        record_id, "The dependency now has a signed availability commitment.", "https://example.net/appeal"
    )
    _mock_ruling(direct_vm, r"Forge V2 appeal", "granted", "greenlit")
    contract.resolve_appeal_with_genlayer(record_id, appeal_id)
    direct_vm.warp("2026-07-16T14:00:05Z")
    contract.finalize_idea(record_id)
    assert json.loads(contract.get_idea_record(record_id))["status"] == "FINALIZED"


def test_permissionless_expiry_prevents_an_adverse_filing_from_blocking_forever(
    deploy, direct_vm, direct_alice, direct_bob
):
    contract, record_id = _deploy_record(deploy, direct_vm, direct_alice)
    _mock_review(direct_vm)
    contract.review_idea_with_genlayer(record_id)
    direct_vm.sender = direct_bob
    challenge_id = contract.submit_challenge(
        record_id, "Unresolved adverse filing.", "https://example.org/adverse"
    )
    direct_vm.warp("2026-07-16T13:00:01Z")
    assert contract.expire_challenge(record_id, challenge_id) == "expired"
    direct_vm.warp("2026-07-16T14:00:02Z")
    contract.finalize_idea(record_id)
    record = json.loads(contract.get_idea_record(record_id))
    assert record["status"] == "FINALIZED"
