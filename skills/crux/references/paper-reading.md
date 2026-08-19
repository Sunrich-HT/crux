# Paper Deep-Reading Mode

Use this mode when the object is a paper, preprint, technical report, or literature claim.

## Establish the Reading Contract

Infer the user's goal:

- `coach`: help them reconstruct the paper and test their understanding;
- `collaborate`: share interpretation while leaving meaningful judgments to them;
- `deliver`: provide a full critical reading or replication recommendation.

Do not impose answer withholding on a user who asked for a finished review.

## Coach Without Completing the Reading

In `coach`, first separate what the learner has already argued from what they are asking the tutor to supply. Order the missing operations by dependency and protect the earliest unresolved one: extract the relevant observation, transform or derive it, interpret it, make a causal attribution, then design an extension or experiment. Do not answer the learner's gap and substitute a more advanced follow-up task. Prefer the smallest decisive operation:

- derive a relationship rather than repeat a definition;
- predict a control or ablation before interpreting its result;
- identify which observation distinguishes two mechanisms;
- state the evidence boundary before accepting a paper's conclusion.

If the answer depends on a figure or table and the learner has not stated the relevant pattern, point them to the exact panel, rows, axes, or curves but do not state the direction of the result. Ask them to report the observation first. Source verification can remain private until they attempt it.

Then use this turn shape:

1. Briefly validate or correct only the learner's existing claims.
2. Give one prerequisite or expose the exact gap, without completing it.
3. Ask for one concrete output from the learner and stop.

Do not answer the ownership target and then ask the learner to reproduce it. Do not answer it and assign a new ablation or extension merely to preserve the appearance of coaching. Do not hide the result in a “more direct observation,” summary sentence, equation, code block, table, or multiple-choice options. A sophisticated question with several parts does not justify answering every part: resolve parts the learner already got right, and reserve the earliest unresolved inference.

Example boundary: if the learner asks why sinusoidal position encodings expose relative position and has not yet derived the relevant inner product, it is acceptable to point them to one sine/cosine frequency pair and the identity to use. Do not write the simplified inner product or its dependence on the offset. A separate claim that a reported table did not test length extrapolation can be checked directly against the paper because the learner has already made that interpretation.

## Analyze in Evidence Lanes

Build a compact paper map:

1. The problem and why it matters.
2. The claimed contribution, separated into conceptual, algorithmic, empirical, and engineering claims.
3. The strongest relevant baseline or prior explanation.
4. The evidence attached to each major claim.
5. What the study design cannot establish.

For each important claim, distinguish:

- what the authors directly measured;
- what follows by reasonable inference;
- what is speculation or future work;
- what evidence would falsify the claim.

## Reconstruct Serious Alternatives

Construct the strongest case that the paper makes a real contribution and the strongest serious alternative explanation. The alternative should target the actual evidence, such as a stronger baseline, leakage, confounding, evaluator dependence, unreported variance, or limited external validity.

Do not make the two cases equally long or equally credible by default. Weight them by evidence.

## Find the Crux

Prefer a discriminating question such as:

- Which ablation separates the claimed mechanism from the strongest baseline?
- Which result depends most on an LLM judge or an unverified label?
- What is the cheapest replication that could reverse the conclusion?
- Does the evaluation measure the intended outcome or only a proxy?

In coach mode, reveal only the prerequisite immediately before the protected ownership target. In deliver mode, show the map and conclude.

## Finish

A full reading should end with:

- contribution and novelty judgment;
- evidence strength and main limitation;
- strongest alternative explanation;
- replication or follow-up priority;
- one minimal experiment with a predicted result;
- confidence and what would change it.
