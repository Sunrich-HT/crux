from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "paper-coaching"
sys.path.insert(0, str(ROOT / "src"))

from crux_supervisor import ResponsePlan, TrustedState, audit_response_plan, compute_contract


def load_json(name: str) -> dict[str, Any]:
    with (EXAMPLE / name).open(encoding="utf-8") as handle:
        return json.load(handle)


def audit_turn(state_name: str, plan_name: str) -> tuple[Any, tuple[Any, ...]]:
    contract = compute_contract(TrustedState.from_dict(load_json(state_name)))
    plan = ResponsePlan.from_dict(load_json(plan_name))
    return contract, audit_response_plan(contract, plan)


def main() -> int:
    fixture = load_json("paper-fixture.json")
    initial_state = TrustedState.from_dict(load_json("initial-state.json"))
    revised_state = TrustedState.from_dict(load_json("revised-state.json"))
    turn_1, findings_1 = audit_turn("initial-state.json", "turn-1-plan.json")
    turn_2, findings_2 = audit_turn("revised-state.json", "turn-2-plan.json")

    checks = (
        fixture["kind"] == "synthetic_paper_fixture",
        tuple(initial_state.source_ids) == (fixture["source_id"],),
        tuple(revised_state.source_ids) == (fixture["source_id"],),
        turn_1.ceiling.name == "R4_REVEAL_CRUX",
        turn_1.question_budget == 1,
        not turn_1.verdict_allowed,
        turn_2.ceiling.name == "R4_REVEAL_CRUX",
        turn_2.question_budget == 1,
        not turn_2.verdict_allowed,
        not findings_1,
        not findings_2,
    )
    passed = all(checks)
    result = {
        "passed": passed,
        "turn_1": {
            "contract_ceiling": turn_1.ceiling.name,
            "planned_move": "R3_DISCRIMINATING_QUESTION",
            "question_budget": turn_1.question_budget,
            "verdict_allowed": turn_1.verdict_allowed,
            "findings": [finding.to_dict() for finding in findings_1],
        },
        "turn_2": {
            "contract_ceiling": turn_2.ceiling.name,
            "planned_move": "R4_REVEAL_CRUX",
            "question_budget": turn_2.question_budget,
            "verdict_allowed": turn_2.verdict_allowed,
            "findings": [finding.to_dict() for finding in findings_2],
        },
    }
    print(json.dumps(result, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
