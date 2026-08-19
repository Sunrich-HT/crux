# Paper-coaching example: one question that exposes a weak interpretation

This deliberately small synthetic paper fragment makes the coaching behavior visible. The data do not come from a real paper and support no scientific claim.

## What the paper reports

The paper claims that knowledge from relevant retrieval causes the improvement in factual accuracy.

| Condition | Factual accuracy |
| --- | ---: |
| No retrieval | 64% |
| Random documents | 71% |
| Relevant documents | 73% |

## The coaching exchange

**Learner:**

> I understand the result. Relevant documents provide knowledge, so accuracy rises from 64% to 73%. This proves that retrieved knowledge works.

**Crux, turn one:**

> If relevant knowledge caused most of those nine points, what result would you have expected from the random-document condition?

**Learner:**

> Random documents should have stayed near 64%. They actually reach 71%, so relevant knowledge may not explain most of the gain.

**Crux, turn two:**

> Right. The table directly measures a seven-point increase when random documents are added, then only two more points when those documents are relevant. It does not support attributing the full 64-to-73 increase to relevant knowledge. Extra context, a changed prompt format, or another shared factor could explain the first seven points. Because no variance or confidence interval is reported, we also do not know whether the remaining two-point difference is stable. Check one thing next: whether the authors report run-to-run variance or a significance test for 73% versus 71%.

The first turn elicits a prediction rather than delivering the analysis. Once the learner finds the discrepancy, the second turn separates measurement from inference and names one next check.

## Reproduce the policy check

```bash
python scripts/verify_paper_coaching.py
```

The verifier checks the two disclosure plans, question budget, and allowed source ID. `paper-fixture.json` explicitly identifies the data as synthetic.
