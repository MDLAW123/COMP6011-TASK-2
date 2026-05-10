# Paper Notes: Scale-CoT: Integrating LLM with Psychiatric Scales for Analyzing Mental Health Issues on Social Media

**Full Citation:**
```bibtex
@inproceedings{wang2024scalecot,
  author    = {Wang, Bichen and Sun, Yixin and Zi, Yuzhe and Zhao, Yanyan and Qin, Bing},
  title     = {Scale-CoT: Integrating LLM with Psychiatric Scales for Analyzing Mental Health Issues on Social Media},
  booktitle = {Proc. IEEE Int. Conf. Bioinformatics and Biomedicine (BIBM)},
  year      = {2024},
  pages     = {2651--2658},
  url       = {https://doi.org/10.1109/BIBM62325.2024.10822322},
}
```

**Date Read:** [YOUR DATE]
**Reading Time:** [YOUR TIME]

---

## First Impressions (written before detailed reading)

Reading the abstract: a prompting method that hooks LLM reasoning to validated psychiatric scales (PHQ-9, BAI, C-SSRS). I expect this to be training-free and to lean heavily on prompt engineering. Likely interpretable but not state-of-the-art on raw F1.

---

## Detailed Notes

### Problem Statement
LLM predictions on mental-health text are accurate but opaque. Without an interpretable rationale, clinicians cannot trust or audit the model. The authors want a prompting strategy whose reasoning maps onto an established clinical scale.

### Related Work They Reference
- He et al. (2023), Towards a psychological generalist AI - related effort to align LLMs with psychological constructs.
- Yang et al. (2024), MentaLLaMA - domain pre-training as an alternative path to clinical alignment.
- Wei et al. (2022), Chain-of-Thought prompting - the technique Scale-CoT extends.

### Technical Approach
Scale-CoT iterates over the items of a chosen psychiatric scale. For each item, the LLM is asked whether the item applies based on the input text. The per-item answers form a structured symptom report. A final prompt aggregates the report into a risk classification. The same scaffolding works across PHQ-9 (depression), BAI (anxiety), and C-SSRS (suicide risk). The authors also distil the LLM's per-item answers into a smaller RoBERTa classifier for production efficiency.

### Key Innovation
The scale itself is the prompt structure. Prior CoT methods produced unconstrained natural-language reasoning; Scale-CoT constrains reasoning to the discrete items of a clinically validated instrument, yielding outputs that look like the rating sheets clinicians already use.

### Experimental Setup
- **Datasets used:** CSSRS Reddit (500 users, 5-level), Dreaddit (Reddit stress, binary), eRisk 2018 (Reddit depression, binary), DepSeverity (Reddit depression severity, 4-class).
- **Evaluation metrics:** Weighted F1, weighted precision, weighted recall.
- **Hardware/compute:** API access to GPT-3.5; RoBERTa distilled model trained on a single GPU.
- **Training details:** No training for the LLM (queried via the API). The distilled RoBERTa is trained on the LLM's per-item answers as labels; standard cross-entropy on the scale-item targets.

### Results

| Method | Dataset | Metric | Score |
|--------|---------|--------|-------|
| Scale-CoT (zero-shot, GPT-3.5) | CSSRS | Weighted F1 | 0.6034 |
| Scale-Distilled RoBERTa | CSSRS | Weighted F1 | 0.7342 |
| MentalRoBERTa | CSSRS | Weighted F1 | 0.6630 |
| Scale-Distilled RoBERTa | Dreaddit | Weighted F1 | 0.8375 |

### Limitations Acknowledged by Authors
Authors note Scale-CoT depends on the quality of the scale; for conditions without a well-validated scale the method is not applicable. They also acknowledge that GPT-3.5 is closed-weight, which limits clinical deployment.

### My Critical Assessment
[YOUR REFLECTION NEEDED] One angle: the comparison is mostly against encoder baselines; a stronger comparison would be against fine-tuned LLMs on the same data.

### Relevance to My Task 2 Work
C-SSRS aligns directly with the five-level taxonomy of the assignment dataset. Scale-CoT gives a training-free path to interpretable five-level prediction. Becomes one of two top candidates in my benchmarking analysis and the explanation layer of my final design.

### Follow-up Papers to Read
- Ge et al. (2025), survey - to position Scale-CoT within the broader landscape.
- Ding et al. (2025), DALE - to compare against a fine-tuned alternative on dialogue data.

---

## Second Read Notes (optional)

*Date of second read:*
*What new things did you notice?*
*Did your understanding change?*
