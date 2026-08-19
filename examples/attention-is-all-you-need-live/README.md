# Live installed-skill test: Attention Is All You Need

This is a captured run, not a scripted demo. On 2026-08-19, Crux was installed from the public GitHub repository and invoked in a separate Codex CLI task. The task read Section 3.5 and Table 3 row (E) of the original [Attention Is All You Need](https://arxiv.org/abs/1706.03762) paper, then conducted two turns of research coaching.

The student asked why the sinusoidal encoding's linear-offset property helps attention represent relative position, and correctly challenged whether Table 3 actually tested length extrapolation. Crux separated mathematical representability, learned behavior, and empirical evidence. It supplied a rotation-matrix scaffold but left the decisive inner-product derivation to the student. In turn two, it evaluated the student's derivation and tightened its limits.

- [Full Chinese case report](README.zh-CN.md)
- [Turn 1 prompt](prompt-turn-1.md) and [unedited output](raw-turn-1.md)
- [Turn 2 prompt](prompt-turn-2.md) and [unedited output](raw-turn-2.md)
- [Runtime, source, task ID, and SHA-256 hashes](run-metadata.json)

This run supports reproducibility and process inspection, not an accuracy percentage or a claim of improved learning. It also exposes a concrete weakness: the first response gave substantial mathematical scaffolding before asking the learner to complete the central derivation.
