import unittest

from crux_supervisor import DisclosureLevel, TrustedState, compute_contract
from crux_supervisor.audit import ResponsePlan, audit_response_plan
from crux_supervisor.models import (
    CruxKind,
    CruxStatus,
    EvidenceStatus,
    InteractionGoal,
    Mode,
    Reversibility,
    Stakes,
)


class PolicyTests(unittest.TestCase):
    def test_unknown_state_fields_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "student_message"):
            TrustedState.from_dict({"mode": "learn", "student_message": "let me see the answer"})

    def test_protected_work_ids_must_be_unique_and_nonblank(self) -> None:
        with self.assertRaisesRegex(ValueError, "must be unique"):
            TrustedState(
                mode=Mode.LEARN,
                protected_work_ids=("derive-relative-position", "derive-relative-position"),
            )
        with self.assertRaisesRegex(ValueError, "must not contain blank"):
            TrustedState(mode=Mode.LEARN, protected_work_ids=(" ",))
        with self.assertRaisesRegex(ValueError, "at most one"):
            TrustedState(
                mode=Mode.LEARN,
                protected_work_ids=("derive-mechanism", "interpret-ablation"),
            )

    def test_assessment_lock_overrides_authorization_and_attempts(self) -> None:
        contract = compute_contract(
            TrustedState(
                mode=Mode.LEARN,
                mastery=0.1,
                attempts=4,
                has_artifact=True,
                assessment_lock=True,
                answer_authorized=True,
            )
        )
        self.assertEqual(contract.ceiling, DisclosureLevel.R1_CLARIFY)
        self.assertFalse(contract.verdict_allowed)

    def test_concrete_attempt_raises_low_help_floor(self) -> None:
        contract = compute_contract(
            TrustedState(mode=Mode.LEARN, mastery=0.9, has_artifact=True)
        )
        self.assertEqual(contract.ceiling, DisclosureLevel.R4_REVEAL_CRUX)

    def test_coach_contract_protects_one_learner_work_item(self) -> None:
        contract = compute_contract(
            TrustedState(
                mode=Mode.LEARN,
                interaction_goal=InteractionGoal.COACH,
                mastery=0.5,
                protected_work_ids=("derive-relative-position",),
            )
        )
        self.assertEqual(contract.protected_work_ids, ("derive-relative-position",))
        self.assertIn("elicit one protected work item", contract.one_move)
        self.assertTrue(
            any("protected work ID" in item for item in contract.forbidden_output)
        )

    def test_answer_authorization_releases_protected_work(self) -> None:
        contract = compute_contract(
            TrustedState(
                mode=Mode.LEARN,
                interaction_goal=InteractionGoal.COACH,
                answer_authorized=True,
                protected_work_ids=("derive-relative-position",),
            )
        )
        self.assertEqual(contract.protected_work_ids, ())

    def test_research_requires_evidence_before_verdict(self) -> None:
        contract = compute_contract(
            TrustedState(
                mode=Mode.RESEARCH,
                interaction_goal=InteractionGoal.DELIVER,
                crux_status=CruxStatus.IDENTIFIED,
                crux_kind=CruxKind.CAUSAL,
                evidence_status=EvidenceStatus.ASSERTED,
            )
        )
        self.assertTrue(contract.research_required)
        self.assertFalse(contract.verdict_allowed)

    def test_two_question_rounds_force_convergence_for_reversible_decision(self) -> None:
        contract = compute_contract(
            TrustedState(
                mode=Mode.DECIDE,
                crux_kind=CruxKind.VALUE,
                crux_status=CruxStatus.IDENTIFIED,
                evidence_status=EvidenceStatus.SOURCED,
                question_rounds=2,
                max_question_rounds=2,
                stakes=Stakes.MEDIUM,
                reversibility=Reversibility.COSTLY,
            )
        )
        self.assertEqual(contract.question_budget, 0)
        self.assertTrue(contract.verdict_allowed)


class AuditTests(unittest.TestCase):
    def test_audit_catches_ceiling_question_and_source_violations(self) -> None:
        contract = compute_contract(TrustedState(mode=Mode.RESEARCH))
        plan = ResponsePlan(
            disclosure_level=DisclosureLevel.R7_JUDGMENT_AND_ACTION,
            question_count=2,
            citation_source_ids=("invented",),
            has_verdict=True,
        )
        findings = audit_response_plan(contract, plan)
        self.assertEqual(
            {finding.rule_id for finding in findings if finding.severity == "error"},
            {"CEILING_EXCEEDED", "QUESTION_BUDGET_EXCEEDED", "UNSUPPORTED_CITATION", "PREMATURE_VERDICT"},
        )

    def test_permitted_verdict_requires_action_and_uncertainty(self) -> None:
        contract = compute_contract(
            TrustedState(
                mode=Mode.DECIDE,
                crux_status=CruxStatus.RESOLVED,
                crux_kind=CruxKind.VALUE,
                preference_known=True,
                evidence_status=EvidenceStatus.SOURCED,
                question_rounds=2,
                max_question_rounds=2,
            )
        )
        findings = audit_response_plan(
            contract,
            ResponsePlan(
                disclosure_level=DisclosureLevel.R7_JUDGMENT_AND_ACTION,
                has_verdict=True,
                has_action=False,
                states_uncertainty=False,
            ),
        )
        self.assertEqual(
            {finding.rule_id for finding in findings},
            {"MISSING_ACTION", "HIDDEN_UNCERTAINTY"},
        )

    def test_audit_rejects_revealing_protected_learner_work(self) -> None:
        contract = compute_contract(
            TrustedState(
                mode=Mode.LEARN,
                interaction_goal=InteractionGoal.COACH,
                protected_work_ids=("derive-relative-position",),
            )
        )
        findings = audit_response_plan(
            contract,
            ResponsePlan(
                disclosure_level=DisclosureLevel.R3_DISCRIMINATING_QUESTION,
                question_count=1,
                elicited_work_ids=("derive-relative-position",),
                revealed_work_ids=("derive-relative-position",),
            ),
        )
        self.assertIn("OWNERSHIP_LEAK", {item.rule_id for item in findings})

    def test_audit_requires_exactly_one_protected_target(self) -> None:
        contract = compute_contract(
            TrustedState(
                mode=Mode.LEARN,
                interaction_goal=InteractionGoal.COACH,
                protected_work_ids=("derive-mechanism",),
            )
        )
        missing = audit_response_plan(
            contract,
            ResponsePlan(disclosure_level=DisclosureLevel.R2_SURFACE_DIMENSION),
        )
        self.assertIn(
            "OWNERSHIP_TARGET_NOT_ELICITED", {item.rule_id for item in missing}
        )

        multiple = audit_response_plan(
            contract,
            ResponsePlan(
                disclosure_level=DisclosureLevel.R3_DISCRIMINATING_QUESTION,
                question_count=1,
                elicited_work_ids=("derive-mechanism", "interpret-ablation"),
            ),
        )
        self.assertIn("MULTIPLE_OWNERSHIP_TARGETS", {item.rule_id for item in multiple})

    def test_audit_accepts_scaffold_without_ownership_leak(self) -> None:
        contract = compute_contract(
            TrustedState(
                mode=Mode.LEARN,
                interaction_goal=InteractionGoal.COACH,
                protected_work_ids=("derive-relative-position",),
            )
        )
        findings = audit_response_plan(
            contract,
            ResponsePlan(
                disclosure_level=DisclosureLevel.R3_DISCRIMINATING_QUESTION,
                question_count=1,
                elicited_work_ids=("derive-relative-position",),
            ),
        )
        self.assertFalse([item for item in findings if item.severity == "error"])


if __name__ == "__main__":
    unittest.main()
