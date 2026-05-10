# Paper Notes: SENTINEL-LLM: Suicide Ensemble-Based Text Intelligence and Natural Language Evaluation Through Large Language Models

**Full Citation:**
```bibtex
@inproceedings{lashgari2025sentinel,
  author    = {Lashgari, Farzaneh and Pourvahab, Mehran and Sousa, Antonio and Monteiro, Anilson and Pais, Sebastiao},
  title     = {SENTINEL-LLM: Suicide Ensemble-Based Text Intelligence and Natural Language Evaluation Through Large Language Models},
  booktitle = {Proc. 11th Int. Conf. Web Research (ICWR)},
  year      = {2025},
  pages     = {299--305},
  url       = {https://doi.org/10.1109/ICWR65219.2025.11006176},
}
```

**Date Read:** [YOUR DATE]
**Reading Time:** [YOUR TIME]

---

## First Impressions (written before detailed reading)

An ensemble of three LLMs plus a hand-curated dictionary. I expect strong raw accuracy and weak interpretability; high training cost.

---

## Detailed Notes

### Problem Statement
Different LLMs catch different kinds of suicide-related signals. Can a soft-voting ensemble plus a hand-curated dictionary improve robustness?

### Related Work They Reference
- Yang et al. (2024), MentaLLaMA - the Llama-based mental-health model used in the ensemble.
- Black et al. (2022), GPT-NEO - one of the three ensemble members.

### Technical Approach
Three fine-tuned LLMs (Qwen2.5, GPT-NEO, Llama3) plus a Frequent-Rare suicide-related dictionary, soft-voting on the binary suicide/non-suicide prediction.

### Key Innovation
Combination of an ensemble across three different model families with an explicit lexical resource. The dictionary is the smaller contribution; the ensemble dominates the gain.

### Experimental Setup
- **Datasets used:** twitter-suicidal-data - public binary Twitter corpus.
- **Evaluation metrics:** Accuracy and F1.
- **Hardware/compute:** Not explicitly stated; ensemble training is GPU-intensive.
- **Training details:** Each member fine-tuned independently; soft voting combined at inference.

### Results

| Method | Dataset | Metric | Score |
|--------|---------|--------|-------|
| SENTINEL-LLM ensemble | twitter-suicidal-data | Accuracy | 0.9254 |
| SENTINEL-LLM ensemble | twitter-suicidal-data | F1 | 0.9237 |

### Limitations Acknowledged by Authors
Binary scope; no five-level evaluation. No explanation layer beyond the predicted label. Training cost roughly 3x a single fine-tuned model.

### My Critical Assessment
[YOUR REFLECTION NEEDED]

### Relevance to My Task 2 Work
Useful as a reference comparator in my benchmarking table. Not adopted as a candidate because its binary scope and lack of explanation rule it out for clinical screening.

### Follow-up Papers to Read
- Wang et al. (2024), Scale-CoT - explanation-first alternative.

---

## Second Read Notes (optional)

*Date of second read:*
*What new things did you notice?*
*Did your understanding change?*
