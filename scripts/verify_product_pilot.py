from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "product-pilot"
sys.path.insert(0, str(ROOT / "src"))

from crux_supervisor import ResponsePlan, TrustedState, audit_response_plan, compute_contract


def load_json(name: str) -> dict[str, Any]:
    with (EXAMPLE / name).open(encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    observation = load_json("pilot-observation.json")
    initial = compute_contract(TrustedState.from_dict(load_json("initial-state.json")))
    resolved_state = TrustedState.from_dict(load_json("resolved-state.json"))
    resolved = compute_contract(resolved_state)
    plan = ResponsePlan.from_dict(load_json("response-plan.json"))
    findings = audit_response_plan(resolved, plan)

    checks = (
        initial.ceiling.name == "R3_DISCRIMINATING_QUESTION",
        initial.question_budget == 1,
        not initial.verdict_allowed,
        initial.research_required,
        resolved.ceiling.name == "R7_JUDGMENT_AND_ACTION",
        resolved.verdict_allowed,
        not resolved.research_required,
        observation["kind"] == "simulated_test_fixture",
        tuple(resolved_state.source_ids) == (observation["source_id"],),
        not findings,
    )
    passed = all(checks)

    result = {
        "passed": passed,
        "initial": {
            "ceiling": initial.ceiling.name,
            "question_budget": initial.question_budget,
            "verdict_allowed": initial.verdict_allowed,
            "research_required": initial.research_required,
        },
        "resolved": {
            "ceiling": resolved.ceiling.name,
            "question_budget": resolved.question_budget,
            "verdict_allowed": resolved.verdict_allowed,
            "research_required": resolved.research_required,
        },
        "audit": {
            "passed": not findings,
            "findings": [finding.to_dict() for finding in findings],
        },
    }
    print(json.dumps(result, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
