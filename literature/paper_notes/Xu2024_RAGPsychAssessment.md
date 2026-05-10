# Paper Notes: Utilizing Large Language Models for Psychological Assessment: Enhancing Suicide Risk Detection Through Social Media Analysis

**Full Citation:**
```bibtex
@inproceedings{xu2024psych,
  author    = {Xu, Zeling and Xu, Jieping and Luo, Yishi and Zhang, Keyu and Zhang, Jinyuan and Zou, Yuntao and Liu, Li},
  title     = {Utilizing Large Language Models for Psychological Assessment: Enhancing Suicide Risk Detection Through Social Media Analysis},
  booktitle = {Proc. 6th Int. Conf. Frontier Technologies of Information and Computer (ICFTIC)},
  year      = {2024},
  pages     = {1418--1421},
  url       = {https://doi.org/10.1109/ICFTIC64248.2024.10913098},
}
```

**Date Read:** [YOUR DATE]
**Reading Time:** [YOUR TIME]

---

## First Impressions (written before detailed reading)

RAG approach. I expect modest fine-tuning plus a curated knowledge base of suicide markers. Likely strong on recall (good for screening) and weaker on precision.

---

## Detailed Notes

### Problem Statement
General LLMs lack domain coverage of suicide-specific linguistic markers. Authors couple a fine-tuned LLM with a retrieval-augmented knowledge base.

### Related Work They Reference
- Lewis et al. (2020), original RAG - the technique they adapt.
- Domain LLM works such as MentaLLaMA - to motivate why RAG is preferred over full fine-tuning when the corpus is small.

### Technical Approach
RAG: a curated database of suicide-related linguistic markers indexes alongside the input text. At inference, top-k relevant markers are retrieved and concatenated with the input, conditioned on by the fine-tuned LLM. Final prediction is binary.

### Key Innovation
Curating a domain-specific knowledge base of suicide markers, rather than relying on generic web retrieval.

### Experimental Setup
- **Datasets used:** Kaggle Reddit suicide-detection corpus (binary).
- **Evaluation metrics:** Accuracy, recall, F1.
- **Hardware/compute:** Not explicitly stated.
- **Training details:** Fine-tuning of the underlying LLM plus index construction over the curated knowledge base.

### Results

| Method | Dataset | Metric | Score |
|--------|---------|--------|-------|
| RAG-LLM | Kaggle Reddit | Balanced Accuracy | 0.903 |
| RAG-LLM | Kaggle Reddit | Recall | 0.94 |

### Limitations Acknowledged by Authors
Binary scope, single dataset, no analysis of retrieval quality.

### My Critical Assessment
[YOUR REFLECTION NEEDED]

### Relevance to My Task 2 Work
Demonstrates the value of a small domain knowledge base. I treat RAG as a future-work extension rather than a Day-1 component, since maintaining a clinical knowledge base adds operational complexity.

### Follow-up Papers to Read
- Ge et al. (2025) - for general RAG context.

---

## Second Read Notes (optional)

*Date of second read:*
*What new things did you notice?*
*Did your understanding change?*
