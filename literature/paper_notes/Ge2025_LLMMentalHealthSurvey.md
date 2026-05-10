# Paper Notes: A Survey of Large Language Models in Mental Health Disorder Detection on Social Media

**Full Citation:**
```bibtex
@inproceedings{ge2025survey,
  author    = {Ge, Zhuohan and Hu, Nicole and Li, Darian and Wang, Yubo and Qi, Shihao and Xu, Yuming and Shi, Han and Zhang, Jason},
  title     = {A Survey of Large Language Models in Mental Health Disorder Detection on Social Media},
  booktitle = {Proc. IEEE 41st Int. Conf. Data Engineering Workshops (ICDEW)},
  year      = {2025},
  pages     = {164--176},
  url       = {https://doi.org/10.1109/ICDEW67478.2025.00027},
}
```

**Date Read:** [YOUR DATE]
**Reading Time:** [YOUR TIME]

---

## First Impressions (written before detailed reading)

A survey paper. I expect a taxonomy of methods and datasets, plus a discussion of open issues. Useful to scaffold my own literature review even if it does not contain a single specific method to adopt.

---

## Detailed Notes

### Problem Statement
The literature on LLMs for mental-health text is scattered across many tasks (depression, anxiety, suicide, eating disorders, PTSD) and many venues. The authors organise it.

### Related Work They Reference
- N/A - survey paper, references span the whole field.

### Technical Approach
Structured review. Methods are classified into prompting, parameter-efficient fine-tuning, full fine-tuning, retrieval-augmented generation, and domain pre-training. Datasets are organised by platform (Reddit, Twitter, clinical interview).

### Key Innovation
The five-pattern taxonomy is a useful organising frame. Coverage is broader than most surveys in this space.

### Experimental Setup
- **Datasets used:** Surveys datasets including Dreaddit, eRisk, CSSRS, Twitter Depression, GoEmotions, MentalSym.
- **Evaluation metrics:** Comparative weighted F1 tables across the surveyed methods.
- **Hardware/compute:** N/A.
- **Training details:** N/A.

### Results

| Method | Dataset | Metric | Score |
|--------|---------|--------|-------|
| Survey-level findings | Multiple | Weighted F1 range | 0.45 - 0.93 |
| Cited stat (WHO) | Global | Suicides per year | 720,000+ |

### Limitations Acknowledged by Authors
The ethics section is shorter than expected; data licensing of social-media corpora is barely discussed.

### My Critical Assessment
[YOUR REFLECTION NEEDED]

### Relevance to My Task 2 Work
Direct source of the five-pattern taxonomy in Section 2.1 of my report. Also the source of the WHO suicide statistic and the psychiatrist-shortage figure I cite.

### Follow-up Papers to Read
- Wang et al. (2024), Scale-CoT - prompting representative.
- Ding et al. (2025), DALE - PEFT representative.

---

## Second Read Notes (optional)

*Date of second read:*
*What new things did you notice?*
*Did your understanding change?*
