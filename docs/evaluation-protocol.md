# Behavioral Evaluation Protocol

Crux must not be evaluated with prompts that already instruct the model to withhold answers, ask one question, or preserve learner work. That tests prompt engineering, not the skill.

## Four conditions

Run every case under the same model, source files, sampling settings, and natural user prompt:

1. `baseline`: no Crux skill or policy instructions.
2. `prompt_only`: a concise coaching prompt, without the installable skill or policy core.
3. `skill_only`: the installed Crux skill in `coach` mode.
4. `skill_supervisor`: Crux plus a typed contract containing one `protected_work_id`, followed by response-plan audit and revision on failure.

Use at least three independent generations per case before drawing a model-level conclusion. Preserve the exact prompt, output, model version, source hash, skill hash, latency, and condition. Randomize output order and hide condition labels from evaluators.

## Keep the answer out of the prompt

Each JSONL case has two separate parts:

- `prompt` is the only case content shown to the model;
- `ownership_target`, `answer_key`, and `already_established` are evaluator-only data.

The validator rejects known instruction contamination from the first live test. Run it with:

```bash
python scripts/validate_behavioral_evals.py
```

## Score distinct outcomes

Use [rubric.json](../evals/behavioral/rubric.json) rather than one overall “accuracy” score. The primary metrics are ownership leakage, technical correctness, source grounding, one-move focus, and next-turn quality. Character count and latency are secondary: brevity is not evidence of learning.

For learning claims, add a delayed, tool-removed transfer question that uses a different surface form but the same reasoning operation. A successful in-session exchange is not enough.

## Decision rule

Do not claim improvement unless `skill_only` or `skill_supervisor` reduces ownership leakage across the case set while remaining non-inferior on technical correctness and source grounding. Report per-condition distributions and failure examples, not only averages.

Treat `skill_only` and `skill_supervisor` as different products. A prompt-level skill may improve average behavior; only the external contract can provide an inspectable enforcement boundary.
