# Crux Architecture

## The Core Thesis

Crux joins two complementary controls:

```text
bilateral steelman + crux discovery
              │
              ▼
      evidence / uncertainty map
              │
              ▼
 typed disclosure contract (policy core)
              │
              ▼
       one model move + response
              │
              ▼
        deterministic / rubric audit
              │
              ▼
       state transition + next turn
```

The steelman process improves the quality of the candidate reasoning. The policy core controls how much of that reasoning is exposed and whether a conclusion is justified. Neither layer is sufficient alone:

- steelmanning without evidence can produce persuasive fiction or false symmetry;
- withholding without a crux can become evasive questioning;
- a model judge without typed state can silently grant itself permission;
- a deterministic policy without a revision path can over-block honest help.

## Trust Boundaries

The production shape should separate five roles:

1. **State adapter:** reads the user turn, artifact, retrieval results, and external checks; emits only a closed typed state proposal.
2. **Policy core:** pure code. Reads trusted state only and computes the disclosure ceiling, evidence rule, one-move budget, and stop condition.
3. **Reasoning planner:** generates private candidates: strongest position, strongest alternative, crux queue, and possible next moves.
4. **Actor:** writes the user-facing response under the contract.
5. **Auditor:** checks the response plan and source IDs. Deterministic checks run first; model-based review is a second layer, not the source of truth.

The state writer must be single-owner. A planner or actor may suggest a state update, but only a typed transition handler should persist it.

## Why The Policy Is Not One Prompt

A prompt can tell a model to be Socratic, balanced, evidence-based, and decisive. Under pressure, these goals conflict. A typed contract makes the highest-risk choice inspectable:

- `assessment_lock` cannot be overridden by a user sentence;
- `question_budget` prevents an endless Socratic loop;
- `source_ids` define which citations are legal;
- `evidence_status` blocks factual verdicts without evidence;
- `interaction_goal` distinguishes coaching from delivery.

The actor still needs a good prompt, but prompt quality no longer determines the permission boundary.

## Modes

### Learn

Preserve the learner's cognitive work. A concrete attempt raises the helpfulness floor; repeated failure can raise the scaffold. An active assessment lock wins over all other permissions.

### Research

Preserve hypothesis ownership while forcing rival explanations and discriminating tests. A factual conclusion requires sourced or independently checked evidence, not just a steelman.

### Decide

Separate values, facts, forecasts, and constraints. Scale effort to stakes and reversibility. A reversible low-stakes decision can conclude quickly; an irreversible high-stakes decision needs stronger evidence and review.

## Failure Taxonomy

Every rejection should name one primary cause:

- `DISCLOSURE`: exceeded the allowed level or revealed a hidden inference;
- `GROUNDING`: cited an unavailable source or presented an unsupported fact;
- `BALANCE`: weakened one side, created false symmetry, or ignored a third option;
- `CONVERGENCE`: asked a low-value or extra question instead of progressing;
- `ACTION`: gave a verdict without a falsifiable next step or rollback condition.

This taxonomy keeps evaluation interpretable. A grounding failure should not be “fixed” by making the tutor less helpful, and a convergence failure should not be counted as evidence that withholding works.

