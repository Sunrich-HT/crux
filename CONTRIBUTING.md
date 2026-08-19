# Contributing to Crux

Crux welcomes focused contributions that make the interaction contract more enforceable, evidence-aware, and measurable.

## Good first contributions

- Add an adversarial policy case to `evals/policy_cases.jsonl`.
- Add a unit test for a disclosure, grounding, convergence, or action invariant.
- Improve one mode reference without turning it into a generic prompt collection.
- Document a reproducible failure with the trusted state, expected contract, and actual result.

Open a proposal before adding a new model dependency, changing the trusted-state schema, or restructuring the policy boundary.

## Development setup

Requires Python 3.11+.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m unittest discover -s tests -v
crux eval evals/policy_cases.jsonl
```

Validate the installable skill when Codex's skill tools are available:

```bash
python /path/to/skill-creator/scripts/quick_validate.py skills/crux
```

## Design constraints

Changes should preserve these boundaries:

1. The deterministic policy core reads typed trusted state, not raw user prose.
2. Evidence quality and rhetorical strength remain separate signals.
3. The disclosure level is a ceiling, not a mandatory sequence.
4. A question is allowed only when its answer can change the next output.
5. The interaction must have an explicit convergence or stop condition.
6. Evaluation failures should identify disclosure, grounding, balance, convergence, or action rather than collapse into one score.

## Pull requests

Keep changes narrow. Include:

- the user-visible or policy behavior being changed;
- why the existing behavior is insufficient;
- tests or eval cases covering the change;
- any new failure mode or trust-boundary assumption.

By contributing, you agree that your contribution is licensed under the MIT License.
