from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "evals" / "behavioral" / "paper_coaching_cases.jsonl"
RUBRIC = ROOT / "evals" / "behavioral" / "rubric.json"
REQUIRED_CONDITIONS = {
    "baseline",
    "prompt_only",
    "skill_only",
    "skill_supervisor",
}
CONTAMINATION_MARKERS = (
    "保留学生应当自己完成",
    "不要一次把全部解释讲完",
    "不要连续抛出",
    "只问一个问题",
    "do not reveal the answer",
    "ask exactly one question",
)


def main() -> int:
    rubric = json.loads(RUBRIC.read_text(encoding="utf-8"))
    if set(rubric["conditions"]) != REQUIRED_CONDITIONS:
        raise ValueError("rubric must define the four required comparison conditions")

    seen: set[str] = set()
    count = 0
    for line_number, line in enumerate(CASES.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        count += 1
        case = json.loads(line)
        case_id = case["id"]
        if case_id in seen:
            raise ValueError(f"line {line_number}: duplicate case id {case_id}")
        seen.add(case_id)

        prompt = case["prompt"].lower()
        contaminated = [item for item in CONTAMINATION_MARKERS if item.lower() in prompt]
        if contaminated:
            raise ValueError(
                f"line {line_number}: clean prompt contains target-behavior instructions: "
                + ", ".join(contaminated)
            )

        target = case["ownership_target"]
        if not target["id"].strip() or not target["description"].strip():
            raise ValueError(f"line {line_number}: ownership target must be concrete")
        if not target["answer_key"]:
            raise ValueError(f"line {line_number}: answer key must not be empty")
        if not case["source_url"].startswith("https://"):
            raise ValueError(f"line {line_number}: source_url must use HTTPS")

    print(json.dumps({"passed": True, "cases": count}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
