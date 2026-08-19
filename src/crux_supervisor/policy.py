from __future__ import annotations

from .models import (
    Contract,
    CruxKind,
    CruxStatus,
    DisclosureLevel,
    EvidenceStatus,
    InteractionGoal,
    Mode,
    Reversibility,
    Stakes,
    TrustedState,
)


def _learning_ceiling(state: TrustedState, reasons: list[str]) -> DisclosureLevel:
    if state.mastery < 0.25:
        ceiling = DisclosureLevel.R5_SERIOUS_ALTERNATIVES
    elif state.mastery < 0.5:
        ceiling = DisclosureLevel.R4_REVEAL_CRUX
    elif state.mastery < 0.75:
        ceiling = DisclosureLevel.R3_DISCRIMINATING_QUESTION
    else:
        ceiling = DisclosureLevel.R2_SURFACE_DIMENSION
    reasons.append("mastery band sets the initial learning scaffold")

    if state.has_artifact and ceiling < DisclosureLevel.R4_REVEAL_CRUX:
        ceiling = DisclosureLevel.R4_REVEAL_CRUX
        reasons.append("a concrete attempt raises the floor to useful feedback")
    if state.attempts >= 3 and ceiling < DisclosureLevel.R5_SERIOUS_ALTERNATIVES:
        ceiling = DisclosureLevel.R5_SERIOUS_ALTERNATIVES
        reasons.append("repeated attempts justify a stronger scaffold")
    if state.answer_authorized:
        ceiling = DisclosureLevel.R7_JUDGMENT_AND_ACTION
        reasons.append("an explicit explain-mode authorization permits the full answer")
    return ceiling


def _research_ceiling(state: TrustedState, reasons: list[str]) -> DisclosureLevel:
    if state.crux_status is CruxStatus.UNKNOWN:
        ceiling = DisclosureLevel.R3_DISCRIMINATING_QUESTION
        reasons.append("the research crux is not yet identified")
    elif state.evidence_status in {EvidenceStatus.NONE, EvidenceStatus.ASSERTED}:
        ceiling = DisclosureLevel.R4_REVEAL_CRUX
        reasons.append("claims exist, but the evidence base is not sourced")
    elif state.crux_status is CruxStatus.IDENTIFIED:
        ceiling = DisclosureLevel.R6_EVIDENCE_MAP
        reasons.append("sourced evidence supports comparison but not closure")
    elif state.evidence_status is EvidenceStatus.VERIFIED:
        ceiling = DisclosureLevel.R7_JUDGMENT_AND_ACTION
        reasons.append("the decisive crux has verified evidence")
    else:
        ceiling = DisclosureLevel.R6_EVIDENCE_MAP
        reasons.append("the crux is resolved provisionally on sourced evidence")

    if state.interaction_goal is InteractionGoal.COACH and not state.answer_authorized:
        ceiling = min(ceiling, DisclosureLevel.R5_SERIOUS_ALTERNATIVES)
        reasons.append("coach mode preserves synthesis work for the researcher")
    elif state.interaction_goal is InteractionGoal.DELIVER:
        if state.evidence_status in {EvidenceStatus.SOURCED, EvidenceStatus.VERIFIED}:
            ceiling = DisclosureLevel.R7_JUDGMENT_AND_ACTION
            reasons.append("deliver mode requests a conclusion backed by available sources")
    return ceiling


def _decision_ceiling(state: TrustedState, reasons: list[str]) -> DisclosureLevel:
    if state.stakes is Stakes.LOW and state.reversibility is Reversibility.EASY:
        reasons.append("a low-cost reversible decision favors action over more dialogue")
        return DisclosureLevel.R7_JUDGMENT_AND_ACTION

    if state.crux_kind is CruxKind.VALUE and not state.preference_known:
        reasons.append("the decisive value preference is unknown")
        return DisclosureLevel.R3_DISCRIMINATING_QUESTION

    factual = state.crux_kind in {
        CruxKind.FACTUAL,
        CruxKind.CAUSAL,
        CruxKind.FEASIBILITY,
        CruxKind.MIXED,
    }
    if factual and state.evidence_status in {EvidenceStatus.NONE, EvidenceStatus.ASSERTED}:
        reasons.append("a factual decision crux lacks sourced evidence")
        return DisclosureLevel.R3_DISCRIMINATING_QUESTION
    if state.crux_status is CruxStatus.UNKNOWN:
        reasons.append("the decision-changing variable is still unknown")
        return DisclosureLevel.R3_DISCRIMINATING_QUESTION
    if state.crux_status is CruxStatus.IDENTIFIED:
        reasons.append("the competing cases can be shown before a verdict")
        return DisclosureLevel.R5_SERIOUS_ALTERNATIVES

    if (
        state.stakes is Stakes.HIGH
        and state.reversibility is Reversibility.IRREVERSIBLE
        and state.evidence_status is not EvidenceStatus.VERIFIED
    ):
        reasons.append("an irreversible high-stakes choice needs verified evidence")
        return DisclosureLevel.R6_EVIDENCE_MAP

    reasons.append("the crux is resolved well enough for a conditional recommendation")
    return DisclosureLevel.R7_JUDGMENT_AND_ACTION


def _move_for(state: TrustedState, ceiling: DisclosureLevel) -> str:
    if state.question_rounds >= state.max_question_rounds:
        return "state assumptions and advance without another question"
    if state.mode is Mode.LEARN:
        if state.protected_work_ids and not state.answer_authorized:
            return "give only the prerequisite scaffold, then elicit one protected work item"
        if state.has_artifact:
            return "ask for a prediction at the first point where the artifact diverges"
        if state.attempts == 0:
            return "elicit the learner's first model or attempted step"
        return "test one prerequisite with a contrasting case"
    if state.mode is Mode.RESEARCH:
        if (
            state.interaction_goal is InteractionGoal.COACH
            and state.protected_work_ids
            and not state.answer_authorized
        ):
            return "give only the prerequisite scaffold, then elicit one protected work item"
        if state.crux_status is CruxStatus.UNKNOWN:
            return "ask the highest-value question that separates rival explanations"
        if state.evidence_status in {EvidenceStatus.NONE, EvidenceStatus.ASSERTED}:
            return "seek the strongest disconfirming primary evidence"
        return "compare the leading claim with its strongest alternative explanation"
    if ceiling < DisclosureLevel.R7_JUDGMENT_AND_ACTION:
        return "ask the one question most likely to change the recommendation"
    return "give a conditional recommendation with a smallest reversible next step"


def compute_contract(state: TrustedState) -> Contract:
    reasons: list[str] = []

    if state.assessment_lock:
        ceiling = DisclosureLevel.R1_CLARIFY
        reasons.append("assessment lock overrides every permission and floor")
    elif state.mode is Mode.LEARN:
        ceiling = _learning_ceiling(state, reasons)
    elif state.mode is Mode.RESEARCH:
        ceiling = _research_ceiling(state, reasons)
    else:
        ceiling = _decision_ceiling(state, reasons)

    exhausted_questions = state.question_rounds >= state.max_question_rounds
    if exhausted_questions and not state.assessment_lock:
        reasons.append("question budget is exhausted; proceed using explicit assumptions")
        if state.mode is Mode.LEARN:
            ceiling = max(ceiling, DisclosureLevel.R4_REVEAL_CRUX)
        elif not (
            state.stakes is Stakes.HIGH
            and state.reversibility is Reversibility.IRREVERSIBLE
        ):
            ceiling = DisclosureLevel.R7_JUDGMENT_AND_ACTION

    factual_crux = state.crux_kind in {
        CruxKind.FACTUAL,
        CruxKind.CAUSAL,
        CruxKind.FEASIBILITY,
        CruxKind.MIXED,
    }
    research_required = (
        state.mode in {Mode.RESEARCH, Mode.DECIDE}
        and factual_crux
        and state.evidence_status in {EvidenceStatus.NONE, EvidenceStatus.ASSERTED}
    )
    verdict_allowed = ceiling >= DisclosureLevel.R7_JUDGMENT_AND_ACTION
    question_budget = 0 if exhausted_questions else 1

    if state.source_ids:
        evidence_rule = "Cite only allowed source IDs and distinguish source claims from inference."
    else:
        evidence_rule = "Do not invent citations; label unsupported factual claims as assumptions."

    if state.mode is Mode.LEARN:
        stop_condition = (
            "Stop escalating when the learner can explain, apply, and check the key step; "
            "give the full answer only when explicitly authorized."
        )
    else:
        stop_condition = (
            "Stop questioning when the next answer would not materially change the judgment, "
            "or when the question budget is exhausted; then state assumptions and conclude."
        )

    required = ["state the current crux", "make uncertainty or assumptions visible"]
    if verdict_allowed:
        required.extend(
            ["give a falsifiable judgment", "name the smallest useful next action"]
        )
    if research_required:
        required.append("retrieve evidence or propose a discriminating test")
    protects_learner_work = (
        state.interaction_goal is InteractionGoal.COACH
        and bool(state.protected_work_ids)
        and not state.answer_authorized
    )
    if protects_learner_work:
        required.append("elicit exactly one protected work item without revealing its result")

    forbidden = [
        "more than one user question in this turn",
        "a citation not present in allowed_source_ids",
        "equal evidential weight merely for rhetorical balance",
    ]
    if not verdict_allowed:
        forbidden.append("a final verdict presented as settled")
    if state.assessment_lock:
        forbidden.append("content that advances the assessed solution")
    if protects_learner_work:
        forbidden.append("the result or an equivalent solution for any protected work ID")

    return Contract(
        mode=state.mode,
        ceiling=ceiling,
        one_move=_move_for(state, ceiling),
        question_budget=question_budget,
        verdict_allowed=verdict_allowed,
        research_required=research_required,
        evidence_rule=evidence_rule,
        stop_condition=stop_condition,
        required_output=tuple(required),
        forbidden_output=tuple(forbidden),
        reasons=tuple(reasons),
        allowed_source_ids=state.source_ids,
        protected_work_ids=state.protected_work_ids if protects_learner_work else (),
    )
