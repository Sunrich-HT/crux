from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .audit import ResponsePlan, audit_response_plan
from .models import Contract, DisclosureLevel, Mode, TrustedState
from .policy import compute_contract


def _load(path: str) -> Any:
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def _print(payload: Any) -> None:
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def _contract_from_dict(raw: dict[str, Any]) -> Contract:
    return Contract(
        mode=Mode(raw["mode"]),
        ceiling=DisclosureLevel(raw["ceiling"]),
        one_move=raw["one_move"],
        question_budget=raw["question_budget"],
        verdict_allowed=raw["verdict_allowed"],
        research_required=raw["research_required"],
        evidence_rule=raw["evidence_rule"],
        stop_condition=raw["stop_condition"],
        required_output=tuple(raw["required_output"]),
        forbidden_output=tuple(raw["forbidden_output"]),
        reasons=tuple(raw["reasons"]),
        allowed_source_ids=tuple(raw["allowed_source_ids"]),
    )


def _run_contract(args: argparse.Namespace) -> int:
    contract = compute_contract(TrustedState.from_dict(_load(args.state)))
    _print(contract.to_dict())
    return 0


def _run_audit(args: argparse.Namespace) -> int:
    contract = _contract_from_dict(_load(args.contract))
    plan = ResponsePlan.from_dict(_load(args.plan))
    findings = audit_response_plan(contract, plan)
    _print(
        {
            "passed": not any(item.severity == "error" for item in findings),
            "findings": [item.to_dict() for item in findings],
        }
    )
    return 1 if any(item.severity == "error" for item in findings) else 0


def _run_evals(args: argparse.Namespace) -> int:
    failures: list[dict[str, Any]] = []
    count = 0
    with Path(args.cases).open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            count += 1
            case = json.loads(line)
            contract = compute_contract(TrustedState.from_dict(case["state"]))
            expected = case["expect"]
            actual = contract.to_dict()
            mismatches = {
                key: {"expected": value, "actual": actual.get(key)}
                for key, value in expected.items()
                if actual.get(key) != value
            }
            if mismatches:
                failures.append(
                    {
                        "line": line_number,
                        "name": case["name"],
                        "mismatches": mismatches,
                    }
                )
    _print({"passed": not failures, "cases": count, "failures": failures})
    return 1 if failures else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="crux", description="Compute and audit Crux disclosure contracts."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    contract = subparsers.add_parser("contract", help="compute a contract")
    contract.add_argument("state", help="path to trusted-state JSON")
    contract.set_defaults(handler=_run_contract)

    audit = subparsers.add_parser("audit", help="audit a response plan")
    audit.add_argument("contract", help="path to computed-contract JSON")
    audit.add_argument("plan", help="path to response-plan JSON")
    audit.set_defaults(handler=_run_audit)

    evals = subparsers.add_parser("eval", help="run deterministic JSONL cases")
    evals.add_argument("cases", help="path to eval JSONL")
    evals.set_defaults(handler=_run_evals)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())

