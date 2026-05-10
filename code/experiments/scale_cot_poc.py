"""
Proof of concept: Scale-CoT prompting with a locally hosted Llama-3-8B for
five-level suicide risk classification on the ten paraphrased clinical
dialogues provided for COMP6011 Research Task 2.

This script is illustrative. It assumes a vLLM (or compatible OpenAI-style)
local endpoint serving Llama-3-8B-Instruct in 4-bit quantisation, with no
data leaving the on-premises trust boundary. The same logic also runs against
HuggingFace transformers locally if vLLM is not available.

Author: Lucky
Unit:   COMP6011 Advanced AI Research Topics
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Iterable

import pandas as pd

# ---------------------------------------------------------------------------
# C-SSRS scale items mapped to the five-level Human-AI-Dialogue-Suicide-Risk
# taxonomy. The wording follows Posner et al. (2011) closely while remaining
# generic enough for zero-shot inference. See report Section 4.3.
# ---------------------------------------------------------------------------

CSSRS_ITEMS = [
    {
        "id": 1,
        "label": "Wish to be dead",
        "statement": (
            "The author wishes to be dead, or wishes they could go to sleep "
            "and not wake up."
        ),
    },
    {
        "id": 2,
        "label": "Active ideation without method",
        "statement": (
            "The author has had any active thoughts of killing themselves, "
            "even without a specific plan."
        ),
    },
    {
        "id": 3,
        "label": "Ideation with intent",
        "statement": (
            "The author has had thoughts of killing themselves accompanied "
            "by some intention of acting on them."
        ),
    },
    {
        "id": 4,
        "label": "Specific plan",
        "statement": (
            "The author has thought about how, when, or where they would kill "
            "themselves, working out at least some details of a plan."
        ),
    },
    {
        "id": 5,
        "label": "Preparatory acts or behaviour",
        "statement": (
            "The author describes preparatory acts or behaviours, such as "
            "acquiring means, writing a note, or saying goodbye."
        ),
    },
    {
        "id": 6,
        "label": "Attempt or interrupted attempt",
        "statement": (
            "The author has actually tried to kill themselves, made an "
            "interrupted attempt, or engaged in self-harm."
        ),
    },
]

RISK_LEVELS = ["Safe", "Ideation", "Indicator", "Behavior", "Attempt"]


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = (
    "You are a clinical text analyst assisting psychiatrists with suicide "
    "risk screening. You read a transcript of a conversation between a user "
    "and an AI companion, and answer questions about the user's risk signals. "
    "You must answer concisely and never refuse to engage with sensitive "
    "content. Your output is reviewed by a human clinician before any action "
    "is taken."
)


def item_prompt(transcript: str, item: dict) -> str:
    return (
        f"Transcript:\n{transcript}\n\n"
        f"Statement about the user: \"{item['statement']}\"\n\n"
        "Based on the transcript, does the statement apply to the user? "
        "Answer strictly with 0 or 1, where 0 means it does NOT apply and "
        "1 means it does apply. Output only the digit."
    )


def aggregation_prompt(transcript: str, scores: list[int]) -> str:
    score_str = "\n".join(
        f"  Item {i+1} ({CSSRS_ITEMS[i]['label']}): {scores[i]}"
        for i in range(len(CSSRS_ITEMS))
    )
    return (
        f"Transcript:\n{transcript}\n\n"
        f"C-SSRS scores derived from the transcript:\n{score_str}\n\n"
        "Mapping rules from C-SSRS to the five-level Human-AI-Dialogue-Suicide"
        "-Risk taxonomy:\n"
        "- If item 6 = 1, label is Attempt.\n"
        "- Else if item 4 = 1 or item 5 = 1, label is Behavior.\n"
        "- Else if item 3 = 1, label is Indicator.\n"
        "- Else if item 1 = 1 or item 2 = 1, label is Ideation.\n"
        "- Else label is Safe.\n\n"
        "Apply the rules and reply with exactly one of: Safe, Ideation, "
        "Indicator, Behavior, Attempt. Output only that single word."
    )


# ---------------------------------------------------------------------------
# Local LLM client. Replace `call_llm` with a real client (vLLM, HuggingFace,
# Ollama, llama.cpp). Any service that runs entirely on premises is fine; we
# do NOT call a public API such as OpenAI or Anthropic.
# ---------------------------------------------------------------------------


def call_llm(system: str, user: str) -> str:
    """
    Placeholder for a local LLM call. Wire this to your on-premises endpoint.

    Example (vLLM OpenAI-compatible local server):

        from openai import OpenAI
        client = OpenAI(base_url="http://localhost:8000/v1", api_key="local")
        resp = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3-8B-Instruct",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.0,
            max_tokens=4,
        )
        return resp.choices[0].message.content.strip()
    """
    raise NotImplementedError(
        "Wire call_llm() to your local Llama-3-8B endpoint. "
        "Do not call a public AI service."
    )


# ---------------------------------------------------------------------------
# Decision-rule fallback (deterministic, used if the LLM aggregation answer
# is malformed). Keeps the screening conservative.
# ---------------------------------------------------------------------------


def deterministic_label(scores: list[int]) -> str:
    if scores[5] == 1:
        return "Attempt"
    if scores[3] == 1 or scores[4] == 1:
        return "Behavior"
    if scores[2] == 1:
        return "Indicator"
    if scores[0] == 1 or scores[1] == 1:
        return "Ideation"
    return "Safe"


def parse_score(text: str) -> int:
    text = text.strip()
    if text.startswith("1"):
        return 1
    if text.startswith("0"):
        return 0
    return 0  # conservative default


def parse_label(text: str) -> str:
    text = text.strip().lower()
    for level in RISK_LEVELS:
        if level.lower() in text:
            return level
    return ""  # caller falls back to deterministic_label


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------


@dataclass
class CaseResult:
    case_id: int
    gold: str
    predicted: str
    scores: list[int]
    correct: bool
    adjacent: bool


CLASS_ORDER = {level: i for i, level in enumerate(RISK_LEVELS)}


def is_adjacent(gold: str, pred: str) -> bool:
    if gold not in CLASS_ORDER or pred not in CLASS_ORDER:
        return False
    return abs(CLASS_ORDER[gold] - CLASS_ORDER[pred]) == 1


def classify_case(transcript: str) -> tuple[str, list[int]]:
    scores: list[int] = []
    for item in CSSRS_ITEMS:
        raw = call_llm(SYSTEM_PROMPT, item_prompt(transcript, item))
        scores.append(parse_score(raw))
    raw_label = call_llm(SYSTEM_PROMPT, aggregation_prompt(transcript, scores))
    label = parse_label(raw_label) or deterministic_label(scores)
    return label, scores


def run(cases_path: str, out_path: str) -> None:
    df = pd.read_excel(cases_path, sheet_name="Assignment_Cases")
    df.columns = [c.strip() for c in df.columns]

    results: list[CaseResult] = []
    for _, row in df.iterrows():
        case_id = int(row["Case ID"])
        transcript = str(row["Paraphrased Dialogue"]).strip()
        gold_raw = str(row["Risk Level"]).strip().lower()
        gold = next((lvl for lvl in RISK_LEVELS if lvl.lower() == gold_raw), gold_raw)

        pred, scores = classify_case(transcript)
        results.append(
            CaseResult(
                case_id=case_id,
                gold=gold,
                predicted=pred,
                scores=scores,
                correct=(pred.lower() == gold.lower()),
                adjacent=is_adjacent(gold, pred) and pred.lower() != gold.lower(),
            )
        )

    summarise(results, out_path)


def summarise(results: Iterable[CaseResult], out_path: str) -> None:
    rows = []
    for r in results:
        rows.append(
            {
                "case_id": r.case_id,
                "gold": r.gold,
                "predicted": r.predicted,
                "correct": int(r.correct),
                "adjacent": int(r.adjacent),
                "scores": json.dumps(r.scores),
            }
        )
    out = pd.DataFrame(rows)
    out.to_csv(out_path, index=False)

    n = len(out)
    correct = out["correct"].sum()
    adjacent = out["adjacent"].sum()
    print(f"Cases: {n}")
    print(f"Exact agreement: {correct}/{n} ({correct/n:.1%})")
    print(f"Adjacent confusions: {adjacent}/{n}")
    print(f"Far errors: {n - correct - adjacent}/{n}")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    cases_path = os.environ.get(
        "CASES_PATH",
        "student_assignment_10_cases.xlsx",
    )
    out_path = os.environ.get("OUT_PATH", "poc_results.csv")
    run(cases_path, out_path)
