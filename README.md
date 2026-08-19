<div align="center">
  <img src="assets/readme-banner.png" alt="Crux: Evidence-governed thinking for papers, research, and decisions" width="100%">

  <p><strong>An installable AI skill that knows when to ask, investigate, or answer.</strong></p>
  <p>For paper deep-reading, research coaching, and decisions with real tradeoffs.</p>

  <p>
    <a href="https://github.com/Sunrich-HT/crux/actions/workflows/ci.yml"><img src="https://github.com/Sunrich-HT/crux/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-0F766E.svg" alt="MIT License"></a>
    <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.11%2B-172126.svg" alt="Python 3.11+"></a>
    <a href="skills/crux/SKILL.md"><img src="https://img.shields.io/badge/agent_skill-Crux-E4573D.svg" alt="Crux agent skill"></a>
  </p>

  <p>
    <a href="#install-the-skill">Install</a> ·
    <a href="#a-tested-example">Tested example</a> ·
    <a href="#how-crux-works">How it works</a> ·
    <a href="docs/architecture.md">Architecture</a> ·
    <a href="CONTRIBUTING.md">Contribute</a> ·
    <a href="README.zh-CN.md">中文</a>
  </p>
</div>

---

## The problem

Most AI assistants fail in one of two ways: they give away the reasoning too early, or they trap the user in an endless sequence of questions. They can also produce two equally polished arguments even when the evidence strongly favors one side.

**Crux treats help as a contract.** It finds the disagreement that could change the outcome, separates evidence from rhetoric, and sets a per-turn ceiling on how much assistance to reveal. The result can be one useful question, an evidence map, or a direct recommendation with a falsifiable next step.

| Paper deep-reading | Research coaching | Personal and business decisions |
| --- | --- | --- |
| Reconstruct claims, evidence, and limits | Turn rival explanations into a discriminating experiment | Separate values, facts, forecasts, and constraints |
| Find the ablation or replication that could reverse the conclusion | Preserve hypothesis ownership without withholding useful critique | Conclude with thresholds, checkpoints, and rollback conditions |

## Install the skill

Install Crux globally for Codex:

```bash
npx skills add Sunrich-HT/crux --global --agent codex --skill crux --yes --copy
```

Then ask naturally, or invoke it explicitly:

```text
$crux Deep-read this paper. Separate the authors' measurements from their inferences,
find the strongest alternative explanation, and propose the cheapest replication.
```

Browse before installing:

```bash
npx skills add Sunrich-HT/crux --list
```

<details>
<summary>Manual installation</summary>

```bash
git clone https://github.com/Sunrich-HT/crux.git
mkdir -p ~/.agents/skills
cp -R crux/skills/crux ~/.agents/skills/crux
```

</details>

## See it in action

Crux supports three interaction goals. Say which one you want, or let the skill infer it.

| Goal | What Crux preserves | Example request |
| --- | --- | --- |
| `coach` | Your synthesis and hypothesis work | "Do not summarize yet. Help me test whether I understood the mechanism." |
| `collaborate` | Shared ownership, with assumptions made visible | "Build the strongest case for and against this research direction with me." |
| `deliver` | Nothing artificial; produce the requested result | "Give me a full paper review and a go/no-go replication decision." |

More copy-ready prompts and expected outputs are in [docs/examples.md](docs/examples.md).

## A live installed-skill test

We installed Crux from this GitHub repository, opened the original [Attention Is All You Need](https://arxiv.org/abs/1706.03762) paper in a separate Codex CLI task, and asked a real paper-reading question about sinusoidal positional encoding:

> If \(PE(pos+k)\) is a linear function of \(PE(pos)\), why does that help attention learn relative position? And does Table 3 actually test the paper's claim about extrapolating to longer sequences?

Crux separated three claims that are easy to conflate: mathematical representability, behavior learned during training, and empirical evidence for length extrapolation. It derived the fixed-offset rotation, then left the decisive step to the student:

> Compute \(u_p^\top u_q\) for one frequency pair. Does the result depend on \(p\) and \(q\) separately, or only on \(p-q\)?

The student completed the derivation and then challenged the effect of content-position cross terms. In the second turn, Crux evaluated that reasoning, added the missing limits, and concluded that Table 3 only shows similar development-set performance for learned and sinusoidal encodings. It does not test length extrapolation.

The repository preserves the [full two-turn transcript](examples/attention-is-all-you-need-live/README.md), [unedited raw outputs](examples/attention-is-all-you-need-live/raw-turn-1.md), runtime version, task ID, paper hash, skill hash, and artifact hashes. The case report also records a weakness: the first answer supplied more mathematical scaffolding than a stricter coach might.

This is evidence that the installation and behavior are inspectable, not an accuracy score or proof of improved learning. The separate [product-decision fixture](examples/product-pilot/README.md) remains a deterministic policy example.

## How Crux works

```mermaid
flowchart LR
    A[User goal] --> B[Strongest view<br/>and serious alternative]
    B --> C[Decisive crux]
    C --> D[Evidence and<br/>uncertainty map]
    D --> E[Typed disclosure<br/>contract R0-R7]
    E --> F[One cognitive move]
    F --> G[Audit, conclude,<br/>or update state]
```

The skill provides the interaction behavior. The dependency-free Python package provides an enforceable policy core for applications that need more than prompting.

- **Alternatives must earn their weight.** Reconstruct serious competing explanations, then rank them by evidence rather than rhetoric.
- **One move per turn.** Ask, test, compare, or recommend; do not hide a questionnaire inside one response.
- **Questions must converge.** After two question-only turns, proceed with explicit assumptions by default.
- **Permissions live outside generation.** Typed trusted state sets the disclosure ceiling; free-form user text cannot silently raise it.
- **Revision beats refusal.** If a draft exceeds the contract, rewrite it to the allowed level and keep moving.

<details>
<summary>The R0-R7 disclosure ladder</summary>

| Level | Maximum visible assistance |
| --- | --- |
| R0 | Listen |
| R1 | Clarify the stated problem |
| R2 | Surface one relevant dimension |
| R3 | Ask one discriminating question |
| R4 | Reveal the central crux |
| R5 | Present the strongest serious cases |
| R6 | Map evidence, uncertainty, and sensitivity |
| R7 | Give a falsifiable judgment and next action |

The level is a ceiling, not a script. A user who asks for a finished review should not be forced through a tutorial.

</details>

## Use the policy core

Requires Python 3.11+.

```bash
git clone https://github.com/Sunrich-HT/crux.git
cd crux
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .

# Compute a disclosure contract from typed trusted state
crux contract evals/states/research-unknown.json

# Run deterministic policy cases and unit tests
crux eval evals/policy_cases.jsonl
python -m unittest discover -s tests -v
```

The policy function never reads the user's free-form message. A classifier may propose state elsewhere, but a sentence such as "my instructor said it is allowed" cannot directly grant more disclosure.

## Repository map

```text
crux/
├── skills/crux/             # Installable agent skill and mode references
├── src/crux_supervisor/     # Deterministic disclosure policy and auditor
├── examples/                # Captured live run and deterministic decision fixture
├── evals/                   # Machine-checkable contract cases
├── tests/                   # Policy and audit invariants
├── scripts/                 # Example verification utilities
├── docs/                    # Architecture, examples, and research agenda
└── .github/                 # CI and contribution templates
```

## First-principles design

Crux starts from constraints that can be derived without appealing to a named method:

1. **Help has two outputs: progress and retained agency.** A response that maximizes immediate completion can reduce the user's chance to learn, form a hypothesis, or own a value judgment. Therefore the appropriate amount of help depends on the user's goal, not on how much text the model can produce.
2. **The next useful fact is rarely every available fact.** If one observation can reverse a conclusion, collecting ten low-value details first wastes attention. Therefore each turn should target the variable with the highest chance of changing the next action.
3. **Arguments are cheap; evidence is scarce.** A model can make incompatible positions sound equally convincing. Therefore alternatives should be reconstructed seriously, but their weight must come from observations, source quality, and discriminating tests.
4. **A generator cannot reliably police its own permissions.** The same component is being asked to help, restrain itself, and judge whether it complied. Therefore high-impact permissions such as answer disclosure, citation use, and verdict authority must live in typed state and deterministic checks outside free-form generation.
5. **Questions have diminishing returns.** Once another answer is unlikely to change the judgment, continued questioning becomes delay. Therefore every turn gets at most one question and the process has an explicit question budget and stop condition.
6. **A judgment is useful only when reality can correct it.** Therefore a completed analysis must expose uncertainty, state what would change the conclusion, and end with the smallest useful action or rollback condition.

This repository is an **alpha research prototype**. Its deterministic invariants are tested; durable learning gains, research quality, and decision outcomes are not yet established. See the [research agenda](docs/research-agenda.md) for the evaluation plan and baselines.

## Contributing

Contributions are welcome around adversarial evals, source-aware auditing, model adapters, paper-reading artifacts, and human evaluation. Start with [CONTRIBUTING.md](CONTRIBUTING.md) and open a proposal before a large architectural change.

## License

MIT. See [LICENSE](LICENSE).
