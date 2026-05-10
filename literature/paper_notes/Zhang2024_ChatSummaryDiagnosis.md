# Paper Notes: Chat, Summary and Diagnosis: A LLM-Enhanced Conversational Agent for Interactive Depression Detection

**Full Citation:**
```bibtex
@inproceedings{zhang2024chat,
  author    = {Zhang, Xiaoheng and Wang, Junjie and Cui, Weigang and Li, Yang},
  title     = {Chat, Summary and Diagnosis: A LLM-Enhanced Conversational Agent for Interactive Depression Detection},
  booktitle = {Proc. 4th Int. Conf. Industrial Automation, Robotics and Control Engineering (IARCE)},
  year      = {2024},
  pages     = {343--348},
  url       = {https://doi.org/10.1109/IARCE64300.2024.00070},
}
```

**Date Read:** [YOUR DATE]
**Reading Time:** [YOUR TIME]

---

## First Impressions (written before detailed reading)

Reading the abstract: three modules - a chat agent, a summariser, and a classifier. The architecture splits the dialogue from the prediction step, which is interesting because most prior work feeds raw dialogue directly to the classifier. I expect the summariser to be the key contribution.

---

## Detailed Notes

### Problem Statement
Static questionnaires miss context-dependent symptoms. Feeding raw dialogue to a classifier means the classifier has to do both information extraction and prediction in one step. The authors decouple these: a dialogue agent collects information, a summariser extracts a structured report, and the classifier predicts from the report.

### Related Work They Reference
- Du et al. (2023), the D4 corpus paper - the source of their dataset.
- Yang et al. (2023), ChatGLM-6B - the backbone they fine-tune.

### Technical Approach
Three modules. (1) Dialogue agent: ChatGLM-6B fine-tuned with an Iterative Knowledge-Aware Prompter to ask adaptive follow-up questions. (2) Summariser: produces a clinical-style symptom report from the dialogue transcript. (3) Classifier: predicts depression and suicide severity from the report.

### Key Innovation
Validating empirically that summary-as-input beats raw-dialogue-as-input by a large margin (4-class F1: 0.46 -> 0.78 on suicide, 0.46 -> 0.74 on depression).

### Experimental Setup
- **Datasets used:** D4 (Chinese-language depression dialogue corpus).
- **Evaluation metrics:** Four-class weighted F1 for depression severity and suicide severity.
- **Hardware/compute:** Not explicitly stated.
- **Training details:** Fine-tuning of ChatGLM-6B with the Iterative Knowledge-Aware Prompter; classifier trained separately on summary inputs.

### Results

| Method | Dataset | Metric | Score |
|--------|---------|--------|-------|
| Raw dialogue input | D4 | Suicide F1 (4-cls) | 0.46 |
| Summary input | D4 | Suicide F1 (4-cls) | 0.78 |
| Raw dialogue input | D4 | Depression F1 (4-cls) | 0.46 |
| Summary input | D4 | Depression F1 (4-cls) | 0.74 |

### Limitations Acknowledged by Authors
The summariser and the dialogue agent are evaluated jointly; isolating the contribution of each is not straightforward. The corpus is Chinese.

### My Critical Assessment
[YOUR REFLECTION NEEDED]

### Relevance to My Task 2 Work
Validates the summary-as-intermediate pattern that my proposed pipeline relies on (Scale-CoT items + DALE domain reports as the summary that feeds the final classifier).

### Follow-up Papers to Read
- Ding et al. (2025), DALE - same dataset, more disentangled summary.

---

## Second Read Notes (optional)

*Date of second read:*
*What new things did you notice?*
*Did your understanding change?*
