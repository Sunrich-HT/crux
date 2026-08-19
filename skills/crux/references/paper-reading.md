# Paper Deep-Reading Mode

Use this mode when the object is a paper, preprint, technical report, or literature claim.

## Establish the Reading Contract

Infer the user's goal:

- `coach`: help them reconstruct the paper and test their understanding;
- `collaborate`: share interpretation while leaving meaningful judgments to them;
- `deliver`: provide a full critical reading or replication recommendation.

Do not impose answer withholding on a user who asked for a finished review.

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

## Bilateral Steelman

Construct the strongest case that the paper makes a real contribution and the strongest serious alternative explanation. The alternative should target the actual evidence, such as a stronger baseline, leakage, confounding, evaluator dependence, unreported variance, or limited external validity.

Do not make the two cases equally long or equally credible by default. Weight them by evidence.

## Find the Crux

Prefer a discriminating question such as:

- Which ablation separates the claimed mechanism from the strongest baseline?
- Which result depends most on an LLM judge or an unverified label?
- What is the cheapest replication that could reverse the conclusion?
- Does the evaluation measure the intended outcome or only a proxy?

In coach mode, reveal only the next useful piece of this map. In deliver mode, show the map and conclude.

## Finish

A full reading should end with:

- contribution and novelty judgment;
- evidence strength and main limitation;
- strongest alternative explanation;
- replication or follow-up priority;
- one minimal experiment with a predicted result;
- confidence and what would change it.

