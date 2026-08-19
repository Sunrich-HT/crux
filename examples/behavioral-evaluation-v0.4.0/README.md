# v0.4.0 behavioral evaluation

This folder preserves an unedited failure-analysis and forward-testing sequence. A clean same-model A/B showed that pre-fix Crux was 27% shorter than the no-skill baseline but still disclosed the complete learner-owned derivation. The earlier successful demo had been contaminated by target-behavior instructions in its test prompt.

The fix adds explicit protected learner-work IDs to the policy and requires coaching to preserve the earliest unresolved operation in the reasoning chain. The Transformer regression then withheld the inner-product result. An unseen Adam case preserved the finite-series derivation. A ResNet case required two more revisions before the skill stopped reading the graph aloud and instead asked the learner to extract the evidence.

- [Full Chinese report](README.zh-CN.md)
- [Clean evaluation protocol](../../docs/evaluation-protocol.md)
- [Runtime and artifact hashes](run-metadata.json)

These are three smoke tests, not evidence of durable learning improvement. The repository preserves the failures alongside the final outputs so the limits remain inspectable.
