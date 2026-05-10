# Paper Notes: DALE: Semantically Disentangled LoRA Expert Mixture for Depression Detection in Psychiatric Dialogue

**Full Citation:**
```bibtex
@inproceedings{ding2025dale,
  author    = {Ding, Jian and Li, Dailin and Han, Qinyu and Lv, Tengxiao and Wang, Jian and Lin, Hongfei and Luo, Ling and Sun, Yuanyuan},
  title     = {DALE: Semantically Disentangled LoRA Expert Mixture for Depression Detection in Psychiatric Dialogue},
  booktitle = {Proc. IEEE Int. Conf. Bioinformatics and Biomedicine (BIBM)},
  year      = {2025},
  pages     = {872--877},
  url       = {https://doi.org/10.1109/BIBM66473.2025.11356998},
}
```

**Date Read:** [YOUR DATE]
**Reading Time:** [YOUR TIME]

---

## First Impressions (written before detailed reading)

Reading the abstract: four LoRA adapters atop a frozen LLM, each specialised on a different causal domain. Sounds like a parameter-efficient mixture-of-experts. The 'disentangled' framing suggests the adapters are trained to capture independent factors; I expect the gain over standard LoRA fine-tuning to come from the separation rather than from the LoRA itself.

---

## Detailed Notes

### Problem Statement
Standard fine-tuned LLMs collapse multiple causal factors of depression (psychological symptoms, somatic symptoms, stressors, protective factors) into a single representation. This makes predictions hard to explain and hard to update when only one factor changes.

### Related Work They Reference
- Hu et al. (2021), LoRA - the underlying parameter-efficient fine-tuning method.
- Zhang et al. (2024), Chat Summary Diagnosis - closely related work using ChatGLM-6B on the same D4 corpus.
- Yang et al. (2024), MentaLLaMA - full fine-tuning baseline that DALE outperforms.

### Technical Approach
Four LoRA adapters are trained on top of a frozen Llama-3-8B or Qwen-3-8B backbone. Each adapter is supervised on dialogue-level annotations for one of: psychological symptoms, somatic symptoms, protective factors, social stressors. A learned router fuses the four adapter outputs, plus the backbone CLS embedding, into final depression-severity and suicide-severity predictions. Annotations are produced by GPT-4 from standard value catalogues that the authors derive from DSM-5 and ICD-11.

### Key Innovation
The semantic disentanglement of LoRA adapters by causal domain. Most LoRA work uses a single adapter per task; DALE uses four parallel adapters with explicit per-domain supervision, then fuses them. This produces interpretable per-domain reports as a by-product of the prediction.

### Experimental Setup
- **Datasets used:** D4 - 1,339 multi-turn doctor-patient depression dialogues, with both depression and suicide severity labels.
- **Evaluation metrics:** Weighted F1 on suicide severity and depression severity.
- **Hardware/compute:** Single GPU sufficient for LoRA training; not stated whether 24 GB or 48 GB.
- **Training details:** Adapters trained for a small number of epochs with cross-entropy on each domain target. The router is trained jointly. Total trainable parameters approximately 0.5% of the backbone.

### Results

| Method | Dataset | Metric | Score |
|--------|---------|--------|-------|
| DALE (Qwen-3-8B) | D4 | Suicide F1 | 0.73 |
| DALE (Qwen-3-8B) | D4 | Depression F1 | 0.56 |
| BERT | D4 | Suicide F1 | 0.66 |
| BERT | D4 | Depression F1 | 0.45 |
| BART | D4 | Suicide F1 | 0.65 |
| BART | D4 | Depression F1 | 0.52 |
| CPT | D4 | Suicide F1 | 0.70 |

### Limitations Acknowledged by Authors
The reliance on GPT-4 for annotations is acknowledged. The four chosen domains are derived from DSM-5 and ICD-11 for depression specifically and would need re-derivation for other conditions. The corpus is Chinese-language; transfer to English is not evaluated.

### My Critical Assessment
[YOUR REFLECTION NEEDED] Possible critiques: GPT-4-annotated labels could leak GPT-4's reasoning style into the adapters, hurting transfer to non-GPT backbones; the F1 numbers are reported on a single train/test split without cross-validation, which makes the apparent gains less robust.

### Relevance to My Task 2 Work
Strongest documented dialogue-format performance on a corpus closely matching the assignment scenario. Combined with Scale-CoT, forms the proposed methodology in my report. The on-premises QLoRA story directly addresses the lecturer's privacy constraint.

### Follow-up Papers to Read
- Zhang et al. (2024), Chat Summary Diagnosis - companion work on the same dataset.
- Wang et al. (2024), Scale-CoT - to compare prompting vs PEFT on similar data.

---

## Second Read Notes (optional)

*Date of second read:*
*What new things did you notice?*
*Did your understanding change?*
