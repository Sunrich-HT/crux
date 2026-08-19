from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from .models import Contract, DisclosureLevel


@dataclass(frozen=True)
class ResponsePlan:
    disclosure_level: DisclosureLevel
    question_count: int = 0
    citation_source_ids: tuple[str, ...] = ()
    has_verdict: bool = False
    has_action: bool = False
    states_uncertainty: bool = False

    @classmethod
    def from_dict(cls, raw: Mapping[str, Any]) -> "ResponsePlan":
        allowed = {field.name for field in cls.__dataclass_fields__.values()}
        unknown = set(raw) - allowed
        if unknown:
            names = ", ".join(sorted(unknown))
            raise ValueError(f"unknown response-plan fields: {names}")
        data = dict(raw)
        data["disclosure_level"] = DisclosureLevel(data["disclosure_level"])
        if "citation_source_ids" in data:
            data["citation_source_ids"] = tuple(data["citation_source_ids"])
        plan = cls(**data)
        if plan.question_count < 0:
            raise ValueError("question_count must be non-negative")
        return plan


@dataclass(frozen=True)
class AuditFinding:
    rule_id: str
    severity: str
    reason: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def audit_response_plan(
    contract: Contract, plan: ResponsePlan
) -> tuple[AuditFinding, ...]:
    findings: list[AuditFinding] = []
    if plan.disclosure_level > contract.ceiling:
        findings.append(
            AuditFinding(
                "CEILING_EXCEEDED",
                "error",
                f"planned R{int(plan.disclosure_level)} exceeds R{int(contract.ceiling)}",
            )
        )
    if plan.question_count > contract.question_budget:
        findings.append(
            AuditFinding(
                "QUESTION_BUDGET_EXCEEDED",
                "error",
                f"planned {plan.question_count} questions; budget is {contract.question_budget}",
            )
        )
    unsupported = set(plan.citation_source_ids) - set(contract.allowed_source_ids)
    if unsupported:
        findings.append(
            AuditFinding(
                "UNSUPPORTED_CITATION",
                "error",
                "citation IDs were not present in the contract: "
                + ", ".join(sorted(unsupported)),
            )
        )
    if plan.has_verdict and not contract.verdict_allowed:
        findings.append(
            AuditFinding(
                "PREMATURE_VERDICT",
                "error",
                "the contract does not permit a final verdict yet",
            )
        )
    if contract.verdict_allowed and plan.has_verdict and not plan.has_action:
        findings.append(
            AuditFinding(
                "MISSING_ACTION",
                "warning",
                "a permitted verdict should include a smallest useful next action",
            )
        )
    if plan.disclosure_level >= DisclosureLevel.R6_EVIDENCE_MAP and not plan.states_uncertainty:
        findings.append(
            AuditFinding(
                "HIDDEN_UNCERTAINTY",
                "warning",
                "evidence maps and verdicts must expose uncertainty or assumptions",
            )
        )
    return tuple(findings)

