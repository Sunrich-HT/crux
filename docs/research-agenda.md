# Research Agenda

Crux is an engineering hypothesis, not a demonstrated learning or decision intervention. The following studies would turn the MVP into a credible research project.

## Claims To Test

1. A typed disclosure contract reduces premature answer leakage under adversarial pressure.
2. Reconstructing the strongest serious alternative reduces agreement bias and improves recognition of live competing explanations.
3. A question budget improves completion and user satisfaction without reducing decision quality.
4. Evidence lanes reduce fabricated citations and overconfident factual conclusions.
5. In learning mode, preserving learner work improves delayed transfer rather than only in-session success.

## Evaluation Layers

### Deterministic invariants

Run on every change:

- no unknown fields enter the policy core;
- assessment lock always caps disclosure;
- no unsupported source ID passes the audit;
- no response plan exceeds the question budget;
- no verdict passes before the contract allows it.

### Model-driven red team

Use scripted personas for:

- earnest learner with a concrete attempt;
- frustrated answer seeker;
- social-engineering user claiming permission;
- prompt injector;
- user whose preferred view is weak but emotionally loaded;
- user facing a false binary;
- research claim with a seductive but confounded result.

Score disclosure, grounding, bilateral balance, convergence, and action separately. Store the rejection reason and the exact contract used for the turn.

Run the clean four-condition protocol in [evaluation-protocol.md](evaluation-protocol.md): baseline, prompt-only, skill-only, and skill plus supervisor. The natural user prompt must not contain target behaviors such as “do not reveal the answer” or “ask one question”; ownership targets and answer keys remain evaluator-only.

### Human evaluation

For learning, compare unguarded chat, Crux tutor, and instructor explain mode with a delayed tool-removed assessment. Measure transfer, persistence, time to convergence, and abandonment. For research, have domain experts judge claim reconstruction, alternative quality, experiment discriminativeness, and calibration. For decisions, use blinded scenario studies with preregistered outcomes and a separate user-value condition so factual accuracy is not confused with preference agreement.

## Strong Baselines

- direct-answer LLM;
- single-prompt question-led tutor;
- installed skill without deterministic supervision;
- installed skill plus a typed protected-work contract;
- prompt that develops only the favored explanation;
- prompt that develops two alternatives without evidence gating;
- Crux without question budget;
- Crux with deterministic policy but no alternative-reconstruction planner.

## Product Metrics

- **Leak rate:** fraction of turns that exceed the contract;
- **Earnest revision rate:** valid requests incorrectly blocked or revised;
- **Unsupported citation rate:** claims attributed to unavailable evidence;
- **Crux hit rate:** whether the selected question changes the ranking or experiment;
- **Convergence depth:** turns before an actionable, conditional conclusion;
- **Abandonment:** whether friction sends users to an unguarded tool;
- **Calibration:** whether confidence tracks expert judgment or delayed outcomes.

The target is not maximum refusal. It is the best tradeoff between preserving user agency, factual reliability, and useful progress.
