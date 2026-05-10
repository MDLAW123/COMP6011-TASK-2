# Methodology - Proof-of-Concept Results

This file holds the results of the proof-of-concept run on the ten paraphrased clinical dialogues. It is the markdown companion to Table 3 in Section 4.5 of my report.

The actual numbers are filled in **after** running `code/experiments/COMP6011_Task2_PoC.ipynb`. The structure below mirrors the report so the same numbers can be quoted in both places.

---

## How to reproduce

1. Open `code/experiments/COMP6011_Task2_PoC.ipynb` in Google Colab.
2. Set the runtime to T4 GPU (Runtime -> Change runtime type -> T4 GPU).
3. Upload `student_assignment_10_cases.xlsx` when prompted.
4. Provide a Hugging Face access token when prompted.
5. Run all cells top to bottom (about 5-10 minutes on a T4).

The notebook produces two CSVs as final outputs:
- `poc_results.csv` - per-case predictions (no dialogue text, safe to commit).
- `poc_summary.csv` - per-class agreement, mirroring Table 3 in the report.

---

## Results

### Per-class agreement (matches Table 3 in the report)

| Class | N | Correct | Adjacent | Far |
|-------|---|---------|----------|-----|
| Safe | 2 | [TODO] | [TODO] | [TODO] |
| Ideation | 2 | [TODO] | [TODO] | [TODO] |
| Indicator | 2 | [TODO] | [TODO] | [TODO] |
| Behavior | 2 | [TODO] | [TODO] | [TODO] |
| Attempt | 2 | [TODO] | [TODO] | [TODO] |
| **Total** | **10** | **[TODO]** | **[TODO]** | **[TODO]** |

### Confusion matrix

|   | pred:Safe | pred:Ideation | pred:Indicator | pred:Behavior | pred:Attempt |
|---|-----------|---------------|----------------|---------------|--------------|
| **true:Safe** | [TODO] | [TODO] | [TODO] | [TODO] | [TODO] |
| **true:Ideation** | [TODO] | [TODO] | [TODO] | [TODO] | [TODO] |
| **true:Indicator** | [TODO] | [TODO] | [TODO] | [TODO] | [TODO] |
| **true:Behavior** | [TODO] | [TODO] | [TODO] | [TODO] | [TODO] |
| **true:Attempt** | [TODO] | [TODO] | [TODO] | [TODO] | [TODO] |

### Weighted metrics

| Metric | Value |
|--------|-------|
| Accuracy | [TODO] |
| Weighted precision | [TODO] |
| Weighted recall | [TODO] |
| Weighted F1 | [TODO] |

### Safety check

[TODO - copy the result from the safety-check cell]

> The most safety-critical sanity check is that no high-risk case (`Ideation` / `Indicator` / `Behavior` / `Attempt`) is mislabelled as `Safe`. The notebook performs this check explicitly.

---

## Discussion of results

[TODO - fill this in after running the notebook. Suggested talking points:]

- Headline class agreement.
- Were any high-risk cases labelled `Safe`? (If yes, this is a serious finding.)
- Where are the confusions concentrated? (Adjacent vs far.)
- How does this compare to the published Scale-CoT zero-shot CSSRS F1 of 0.6034?
- What does this tell us about the readiness of zero-shot prompting for clinical deployment?

---

## Caveats

1. **Sample size is too small for statistical claims.** Ten cases (two per class) is sufficient to validate the pipeline but inadequate to estimate generalisation performance. The proof of concept is a feasibility check, not a benchmark.
2. **Zero-shot only.** The DALE adapters described in the methodology are not yet trained; the PoC runs the backbone with Scale-CoT prompting alone. Adapter training is a future step that is expected to lift accuracy.
3. **No fine-tuning to Australian English clinical style.** The cases are paraphrased Reddit-style dialogue from the Human-AI-Dialogue-Suicide-Risk corpus (Chen et al., 2026). Performance on real Australian clinical dialogue would need separate evaluation.
4. **Single decoding seed.** Greedy decoding is deterministic, but a temperature-sampled run could yield different per-case errors. Greedy chosen here for reproducibility.
