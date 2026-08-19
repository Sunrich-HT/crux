# Tested product-decision example

This is a deterministic, end-to-end fixture, not a claim about a real pilot. The observations in `pilot-observation.json` are explicitly synthetic so that anyone can reproduce the policy transition.

## Scenario

> We have two engineers and six weeks. Should we build a full AI paper-reading product? Five researchers say it sounds useful, but we have no usage data. We can run a manual concierge pilot in five days.

With only asserted interest, `initial-state.json` produces an **R3 ceiling**: no verdict, one question, and a requirement to collect evidence.

The single decision-changing question is:

> Of the five researchers, how many will bring one real paper and return for a second session if the manual workflow saves at least 30 minutes?

The fixture then adds the observations in `pilot-observation.json`: four first sessions, three returns, and a median 42 minutes saved. `resolved-state.json` now produces an **R7 ceiling**, and `response-plan.json` passes the deterministic audit.

## Audited response

> Do not commit two engineers to a six-week full build yet. Run a 10-day narrow prototype around the workflow that produced repeat use. The observations support a recurring need, but the sample is only five people and may overstate demand because the service was manual. Continue only if at least 8 of 12 users complete one session, 6 return with a second paper within seven days, median reported time saved remains at least 30 minutes, and 3 users accept a paid pilot or sign a letter of intent. Stop or redesign if fewer than 4 return or median time saved falls below 20 minutes.

This response cites only `pilot-2026-08-19`, states uncertainty, gives a conditional verdict, and names both the next action and rollback thresholds.

## Reproduce it

```bash
python scripts/verify_product_pilot.py
```

Expected result:

```json
{
  "passed": true,
  "initial": {
    "ceiling": "R3_DISCRIMINATING_QUESTION",
    "question_budget": 1,
    "verdict_allowed": false,
    "research_required": true
  },
  "resolved": {
    "ceiling": "R7_JUDGMENT_AND_ACTION",
    "question_budget": 1,
    "verdict_allowed": true,
    "research_required": false
  },
  "audit": {
    "passed": true,
    "findings": []
  }
}
```
