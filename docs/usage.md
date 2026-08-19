# Using Crux

## Invoke the skill

After global installation, start a new Codex task. Type `$` and select `crux`, or begin the request with:

```text
$crux
```

Use `$crux`, not `/crux`. The mention already invokes the skill, so “please use this skill” is unnecessary. Crux is explicit-only and is not loaded in conversations that do not include the `$crux` mention.

## Paper coaching

```text
$crux

Use coach mode. Work from the attached paper's primary text.
My current interpretation is: ...
What I still cannot explain is: ...
Check the reasoning I have already done and continue coaching me.
```

## Complete paper review

```text
$crux

Use deliver mode. Reconstruct the paper's conceptual, algorithmic, and empirical claims.
Separate direct measurements, reasonable inference, and speculation. Give the strongest
alternative explanation, a minimal replication, confidence, and what would change the judgment.
```

## Research collaboration

```text
$crux

Use collaborate mode. My hypothesis is: ...
My current evidence is: ...
My data, compute, and time constraints are: ...
Build the strongest competing mechanism and artifact explanation with me, then design the
cheapest experiment with different predictions and explicit run, revise, or stop criteria.
```

## Product or business decision

```text
$crux

Use deliver mode. We are deciding whether to spend six weeks building: ...
The target user, current evidence, budget, and constraints are: ...
Identify the assumption most likely to reverse the plan. Recommend continue, narrow, or stop,
with validation metrics, a review date, and a rollback condition.
```

## Continue or switch modes

```text
$crux Continue in coach mode. Here is my attempted derivation: ...
```

```text
$crux Switch to deliver mode. Now give the complete derivation and identify what I missed.
```

See the [Chinese usage guide](usage.zh-CN.md) and the official [OpenAI Skills documentation](https://learn.chatgpt.com/docs/build-skills).
