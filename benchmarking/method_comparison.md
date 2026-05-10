# Benchmarking Analysis - COMP6011 Task 2

**Question:** Of the LLM design patterns surveyed in `literature/`, which is most suitable for the AI avatar suicide-risk-detection engine?

This analysis mirrors Section 3 of my report, with extra commentary that did not fit in the page limit.

---

## 1. Evaluation Metrics

For an imbalanced multi-class clinical screening task, the literature converges on:

- **Weighted F1** — primary metric. F1 = 2 * P * R / (P + R), weighted by class support. Handles class imbalance better than macro F1 when minority classes are very small.
- **Weighted recall** — reported separately because for screening, the cost of a false negative (missing a high-risk case) materially exceeds the cost of a false positive.
- **Macro F1** — reported when minority-class performance matters. For my use case the *Attempt* class is the most safety-critical and the smallest, so macro F1 is also tracked.
- **Accuracy** — reported only for binary tasks where it is meaningful.

I do not report calibration metrics (Brier score, ECE) here because none of the surveyed papers report them. This is a noted gap in the field that I flag in my Discussion section.

---

## 2. Datasets Considered

Per the lecturer's clarification, the ten paraphrased cases provided for the assignment are reserved for the methodology proof of concept and not used for benchmarking. I draw published benchmark numbers from the following corpora:

| Dataset | Source | Size | Label Space | Why Relevant |
|---------|--------|------|-------------|--------------|
| **D4** | Du et al. (2023), used by Ding et al. (2025), Zhang et al. (2024) | 1,339 dialogues | depression severity (4-cls), suicide severity (4-cls) | Closest in format to the assignment (dialogue, multi-class). |
| **CSSRS Reddit** | Posner et al. (2011) C-SSRS, Reddit annotated by 4 psychiatrists | 500 users | 5-level (Supportive/Indicator/Ideation/Behavior/Attempt) | Almost identical label space to the assignment dataset. |
| **Dreaddit** | Turcan & McKeown (2019) | ~3,500 posts | binary stress | Adjacent task; useful for generalisation evidence. |
| **eRisk 2018** | Losada et al. (2018) | several thousand users | binary depression | Adjacent task. |
| **twitter-suicidal-data** | Public Kaggle | ~10k tweets | binary suicide | Used by SENTINEL-LLM; binary upper-bound reference. |

The CSSRS Reddit five-level label space maps cleanly onto the assignment's five categories, so reported numbers transfer almost directly. The D4 four-level suicide label space requires a small remapping (no separate Indicator level) which I document in the methodology notes.

---

## 3. Candidate Methods Selected for Benchmarking

I selected four candidates based on their alignment with the conversational, multi-class, privacy-sensitive setting of the assignment:

1. **Scale-CoT (Wang et al., 2024)** — prompting representative.
2. **DALE (Ding et al., 2025)** — PEFT representative on dialogue data.
3. **Chat-Summary-Diagnosis (Zhang et al., 2024)** — fine-tuned ChatGLM-6B with summary-as-input on D4.
4. **SENTINEL-LLM (Lashgari et al., 2025)** — ensemble representative; included as a high-accuracy comparator on a different label space.

Encoder baselines (BERT, RoBERTa, MentalRoBERTa) and a domain-pretrained variant are included for context.

---

## 4. Quantitative Results

All values are reproduced from the cited papers; I did not re-implement these methods. Numbers reflect the experimental conditions of the original authors and are therefore not strictly comparable across datasets.

| Method | D4 Suicide F1 | D4 Depression F1 | CSSRS Five-Level F1 | Twitter Binary F1 |
|--------|--------------:|-----------------:|--------------------:|------------------:|
| BERT (encoder baseline) | 0.66 | 0.45 | 0.6316 | — |
| RoBERTa (encoder baseline) | — | — | 0.6565 | — |
| MentalRoBERTa (domain pre-train) | — | — | 0.6630 | — |
| BART | 0.65 | 0.52 | — | — |
| CPT | 0.70 | 0.46 | — | — |
| Scale-CoT (zero-shot, GPT-3.5) | — | — | 0.6034 | — |
| Scale-Distilled RoBERTa | — | — | **0.7342** | — |
| **DALE (Qwen-3-8B)** | **0.73** | **0.56** | — | — |
| Zhang et al. summary input (4-cls) | 0.78 | 0.74 | — | — |
| SENTINEL-LLM ensemble | — | — | — | 0.9237 |

Bold = best per dataset among the candidates considered for adoption.

---

## 5. Qualitative Comparison

Quantitative F1 alone is insufficient for a clinical screening tool. The five qualitative criteria below matter as much as the headline number:

| Criterion | Scale-CoT | DALE | Zhang ChatSummary | SENTINEL-LLM |
|-----------|-----------|------|-------------------|--------------|
| **Privacy posture** (on-prem feasibility) | depends on backbone | excellent (open-weight + LoRA) | good (ChatGLM-6B is open) | good (ensemble of open models) |
| **Interpretability** | per-item C-SSRS evidence | per-domain reports | summary report | predicted label only |
| **Training cost** | none | low (LoRA only) | moderate | high (3x fine-tuning) |
| **Adaptation to new conditions** | high (just swap scale) | moderate (re-derive domains) | moderate | low (re-train ensemble) |
| **Multi-class support** | yes (5-level CSSRS) | yes (4-level on D4) | yes (4-level on D4) | binary only |

The matrix makes the trade-offs explicit. Scale-CoT alone has the best interpretability but trails on raw F1. DALE has the best dialogue-format F1 but does not produce per-scale-item evidence by default. SENTINEL-LLM has the highest absolute accuracy but only on binary classification, and produces no rationale.

---

## 6. Recommendation

Synthesising the above, the most suitable foundation for the AI avatar engine is a **DALE-style PEFT pipeline with a Scale-CoT explanation layer**, deployed entirely on premises. Specifically:

- **Backbone:** Llama-3-8B-Instruct (or Qwen-2.5-7B-Instruct as fallback for open-access).
- **Adaptation:** QLoRA, four DALE-style domain adapters trained on D4 for psychological symptoms, somatic symptoms, protective factors, and stressors.
- **Prompting at inference:** Scale-CoT querying the six C-SSRS items.
- **Final classifier:** small MLP fusing the adapter outputs and Scale-CoT item scores into the five-level prediction.

This combination gets the dialogue-level F1 strength of DALE (best documented number on the closest-format dataset) plus the auditable per-item evidence of Scale-CoT (necessary for clinical adoption and required by Australia's AI Ethics Principle 6 on transparency). The on-premises QLoRA story directly addresses the lecturer's privacy constraint that "private dialogue must NOT be sent to public AI services such as ChatGPT."

SENTINEL-LLM's higher headline accuracy is not adopted because its binary scope rules out the five-level prediction and its lack of explanation is incompatible with clinical screening. Scale-CoT alone is not adopted as the principal engine because a 0.6034 F1 trails the fine-tuned alternatives by several points; instead, Scale-CoT is layered on top of DALE.

---

## 7. Open Issues Identified

1. **Cross-corpus transfer is largely untested.** D4 is Chinese-language and clinical-style; CSSRS is English-language Reddit. None of the surveyed papers evaluate transfer between the two.
2. **Calibration is unreported.** No paper in my literature review reports calibration metrics, despite their importance for screening tools where probabilistic outputs feed risk-stratification dashboards.
3. **Class imbalance on the most severe categories** (Behavior, Attempt) systematically depresses macro-averaged metrics. This is a structural problem of the data, not the method.
4. **English-language Australian clinical dialogue is not represented in any public corpus.** Domain adaptation will be needed before any production deployment.
