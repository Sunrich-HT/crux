from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum, IntEnum
from typing import Any, Mapping


class Mode(str, Enum):
    LEARN = "learn"
    RESEARCH = "research"
    DECIDE = "decide"


class InteractionGoal(str, Enum):
    COACH = "coach"
    COLLABORATE = "collaborate"
    DELIVER = "deliver"


class EvidenceStatus(str, Enum):
    NONE = "none"
    ASSERTED = "asserted"
    SOURCED = "sourced"
    VERIFIED = "verified"


class CruxStatus(str, Enum):
    UNKNOWN = "unknown"
    IDENTIFIED = "identified"
    RESOLVED = "resolved"


class CruxKind(str, Enum):
    FACTUAL = "factual"
    VALUE = "value"
    CAUSAL = "causal"
    FEASIBILITY = "feasibility"
    MIXED = "mixed"


class Stakes(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Reversibility(str, Enum):
    EASY = "easy"
    COSTLY = "costly"
    IRREVERSIBLE = "irreversible"


class DisclosureLevel(IntEnum):
    R0_LISTEN = 0
    R1_CLARIFY = 1
    R2_SURFACE_DIMENSION = 2
    R3_DISCRIMINATING_QUESTION = 3
    R4_REVEAL_CRUX = 4
    R5_BILATERAL_STEELMAN = 5
    R6_EVIDENCE_MAP = 6
    R7_JUDGMENT_AND_ACTION = 7


DISCLOSURE_LABELS = {
    DisclosureLevel.R0_LISTEN: "listen without adding substantive content",
    DisclosureLevel.R1_CLARIFY: "clarify the stated problem",
    DisclosureLevel.R2_SURFACE_DIMENSION: "surface one relevant concept or dimension",
    DisclosureLevel.R3_DISCRIMINATING_QUESTION: "ask one decision-changing question",
    DisclosureLevel.R4_REVEAL_CRUX: "show the central disagreement or problem structure",
    DisclosureLevel.R5_BILATERAL_STEELMAN: "present the strongest serious cases on both sides",
    DisclosureLevel.R6_EVIDENCE_MAP: "map evidence, uncertainty, and sensitivity without a final verdict",
    DisclosureLevel.R7_JUDGMENT_AND_ACTION: "give a falsifiable judgment and next action",
}


@dataclass(frozen=True)
class TrustedState:
    """Typed state accepted by the policy core.

    Free-form user text is intentionally absent. A separate, non-privileged
    adapter may propose these signals, but it cannot add new fields or bypass
    validation.
    """

    mode: Mode
    interaction_goal: InteractionGoal = InteractionGoal.COLLABORATE
    mastery: float = 0.5
    attempts: int = 0
    has_artifact: bool = False
    assessment_lock: bool = False
    answer_authorized: bool = False
    evidence_status: EvidenceStatus = EvidenceStatus.NONE
    crux_status: CruxStatus = CruxStatus.UNKNOWN
    crux_kind: CruxKind = CruxKind.MIXED
    preference_known: bool = False
    question_rounds: int = 0
    max_question_rounds: int = 2
    stakes: Stakes = Stakes.MEDIUM
    reversibility: Reversibility = Reversibility.COSTLY
    source_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not 0.0 <= self.mastery <= 1.0:
            raise ValueError("mastery must be between 0 and 1")
        if self.attempts < 0 or self.question_rounds < 0:
            raise ValueError("attempt counts must be non-negative")
        if self.max_question_rounds < 0:
            raise ValueError("max_question_rounds must be non-negative")
        if len(set(self.source_ids)) != len(self.source_ids):
            raise ValueError("source_ids must be unique")

    @classmethod
    def from_dict(cls, raw: Mapping[str, Any]) -> "TrustedState":
        allowed = {field.name for field in cls.__dataclass_fields__.values()}
        unknown = set(raw) - allowed
        if unknown:
            names = ", ".join(sorted(unknown))
            raise ValueError(f"untrusted or unknown state fields: {names}")

        data = dict(raw)
        enum_fields: dict[str, type[Enum]] = {
            "mode": Mode,
            "interaction_goal": InteractionGoal,
            "evidence_status": EvidenceStatus,
            "crux_status": CruxStatus,
            "crux_kind": CruxKind,
            "stakes": Stakes,
            "reversibility": Reversibility,
        }
        for key, enum_type in enum_fields.items():
            if key in data:
                data[key] = enum_type(data[key])
        if "source_ids" in data:
            data["source_ids"] = tuple(data["source_ids"])
        return cls(**data)


@dataclass(frozen=True)
class Contract:
    mode: Mode
    ceiling: DisclosureLevel
    one_move: str
    question_budget: int
    verdict_allowed: bool
    research_required: bool
    evidence_rule: str
    stop_condition: str
    required_output: tuple[str, ...]
    forbidden_output: tuple[str, ...]
    reasons: tuple[str, ...]
    allowed_source_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["mode"] = self.mode.value
        result["ceiling"] = int(self.ceiling)
        result["ceiling_name"] = self.ceiling.name
        result["ceiling_description"] = DISCLOSURE_LABELS[self.ceiling]
        return result

