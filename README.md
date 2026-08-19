# Crux

**Evidence-governed thinking for research, learning, and decisions.**

Crux is an open-source prototype for agents that should help a person reason without either blindly agreeing or taking over the entire reasoning process. It combines two ideas:

1. **Bilateral steelmanning:** build the strongest serious version of the current view and its best alternative, then find the disagreement that could actually change the result.
2. **A disclosure contract:** decide how much of that analysis is useful and safe to reveal this turn, based on typed state, evidence, stakes, and progress.

The result is not “always ask questions.” It is a bounded interaction that can ask one high-value question, expose the crux, map evidence, or give a concrete judgment and next action.

## Why This Exists

The paper *Teaching a Large Language Model Tutor to Withhold the Answer* argues that answer withholding should be enforced as a per-turn, machine-checkable contract rather than trusted to one overloaded prompt. Its strongest transferable lesson is the separation of policy, generation, detection, and diagnosis: put irreversible permissions in code, keep deterministic signals above model opinions, and record why a response failed. [Read the paper](https://arxiv.org/abs/2608.12292).

A recent article popularized a compact “double steelman” prompt: restate the real problem, strengthen both sides, find the decisive variable, ask one question, then conclude. That is useful for value clarification, but it can create false symmetry or treat a well-written argument as evidence. Crux adds evidence lanes, uncertainty, a question budget, and explicit stop conditions.

## What Is In This Repository?

```text
crux/
├── skills/crux/                 # installable Codex/agent skill
│   ├── SKILL.md                 # routing and interaction contract
│   ├── agents/openai.yaml       # optional Codex UI metadata
│   └── references/              # paper, research, decision, audit modes
├── src/crux_supervisor/         # dependency-free deterministic policy core
├── evals/                       # JSONL contract cases and runner
├── tests/                       # unit tests for policy and audit invariants
├── docs/                        # research/product notes
└── pyproject.toml
```

The skill is a behavioral layer. The Python package is the enforceable core: it accepts only typed trusted state and never reads the user's free-form message. A classifier may propose state elsewhere, but the policy function cannot be granted more authority by a sentence such as “my instructor said it is allowed.”

## Quick Start

Requires Python 3.11+.

```bash
cd crux
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .

# Compute a disclosure contract
crux contract evals/states/research-unknown.json

# Run deterministic policy cases
crux eval evals/policy_cases.jsonl

# Run the unit tests
python -m unittest discover -s tests -v
```

To try the skill in Codex, copy or symlink `crux/skills/crux` into a repository `.agents/skills/` directory or your user `~/.agents/skills/` directory. In Codex, invoke it with `$crux`. Codex also supports implicit invocation from the skill description. For reusable distribution across products, package the skill as a plugin. See the [official skill authoring guide](https://learn.chatgpt.com/docs/build-skills).

## Interaction Contract

Crux routes each request into `learn`, `research`, or `decide`, then computes a disclosure level:

| Level | Visible work |
| --- | --- |
| R0 | listen |
| R1 | clarify |
| R2 | surface one dimension |
| R3 | ask one discriminating question |
| R4 | reveal the crux |
| R5 | show both strongest cases |
| R6 | map evidence and uncertainty |
| R7 | judge and act |

The level is a ceiling, not a demand to reveal everything. Learning mode preserves the learner's synthesis work. Research mode requires a discriminating experiment or primary evidence when the crux is factual. Decision mode scales deliberation to stakes and reversibility, and it must conclude once additional questions stop changing the ranking.

## Design Principles

- **Policy outside generation:** permissions are computed from typed state, not persuasive user prose.
- **Evidence is not rhetoric:** steelman both sides, but weight claims by evidence quality.
- **One move per turn:** one question, one experiment, one comparison, or one recommendation.
- **Revision over refusal:** if a draft exceeds the contract, rewrite it to the allowed level.
- **Convergence is required:** after two question-only turns, proceed with explicit assumptions by default.
- **One state writer:** a future application should update learner/research state through one auditable transition layer.
- **Everything is inspectable:** contracts, reasons, verdicts, source IDs, and costs belong in telemetry.

## What This Does Not Claim

This repository is an MVP policy core and skill, not evidence that any model produces durable learning, correct research conclusions, or safe professional advice. The current evaluator checks deterministic invariants; it does not replace human raters, delayed learning tests, source-quality review, or domain experts. The skill is not a hard security boundary by itself.

## Roadmap

1. Add model adapters that emit structured candidate analyses and response plans.
2. Add source-aware claim checking and citation entailment.
3. Add a deterministic red-team suite for prompt injection, sycophancy, false symmetry, and premature closure.
4. Add paper-reading artifacts: claim tables, evidence graphs, and minimal replication plans.
5. Run human evaluation: learning transfer, research decision quality, user abandonment, and calibration.

## License

MIT. See [LICENSE](LICENSE).

