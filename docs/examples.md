# Crux Examples

These examples show the shape of a useful request and the result Crux should converge toward. They are not fixed response templates.

Start with the concrete [paper-coaching exchange](../examples/paper-coaching/README.md) and run `python scripts/verify_paper_coaching.py`. A separate [product-decision fixture](../examples/product-pilot/README.md) tests recommendation and rollback behavior.

## Paper deep-reading

### Coach my understanding

```text
$crux Use coach mode. I think the paper's main contribution is the training objective.
Do not summarize the whole paper yet. Ask the single question that best tests whether
I understand what the objective adds over the strongest baseline.
```

Expected shape: one discriminating question, followed in later turns by a claim-evidence map and a correction only where the user's reconstruction fails.

### Deliver a critical review

```text
$crux Use deliver mode. Reconstruct the paper's conceptual, algorithmic, and empirical
claims. Separate direct measurements from inference, reconstruct the strongest alternative
explanation, and end with a minimal replication and a go/no-go judgment.
```

Expected shape: contribution judgment, evidence limits, serious rival explanation, minimal replication, confidence, and what result would reverse the judgment.

## Research coaching

```text
$crux Collaborate with me on this hypothesis: longer chain-of-thought improves robustness.
Build the strongest competing mechanism and artifact explanation. Propose the cheapest
experiment whose predicted results differ across the three accounts, with a stop criterion.
```

Expected shape: a compact rival set, distinguishable predictions, intervention and control, primary metric, confound checks, estimated cost, and run/revise/stop criteria.

## Personal decision

```text
$crux I am choosing between staying in my current role and joining an early-stage startup.
Separate my values from factual forecasts. Ask at most one question if it could change
the ranking; otherwise recommend a small reversible next action and a decision deadline.
```

Expected shape: strongest reason for and against, the threshold that flips the recommendation, a reversible information-gathering step, and a checkpoint.

## Product or business decision

```text
$crux We are considering a six-week build for an AI research assistant. Challenge the
current plan without inventing equal evidence for both sides. Identify the riskiest
assumption, the smallest prototype that can falsify it, and explicit go/stop metrics.
```

Expected shape: current judgment, evidence and assumptions, a low-cost falsification test, measurable success criteria, and a rollback condition.

## Response audit

```text
$crux Audit this recommendation for disclosure, grounding, adversarial balance,
convergence, and action quality. Name one primary failure class per finding and revise
the response instead of merely rejecting it.
```

Expected shape: separated findings with reasons, followed by a corrected response that stays within the relevant disclosure contract.
