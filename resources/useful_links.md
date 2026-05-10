# Useful Resources - COMP6011 Task 2

A working reference of resources I drew on while researching LLM-based suicide risk detection.

---

## Paper search engines

| Tool | URL | Best for |
|------|-----|----------|
| Google Scholar | https://scholar.google.com | General academic search, citation tracking |
| Semantic Scholar | https://www.semanticscholar.org | AI/ML papers, citation graphs |
| arXiv | https://arxiv.org | Preprints (cs.CL for NLP, cs.LG for ML) |
| IEEE Xplore | https://ieeexplore.ieee.org | IEEE conference and journal papers (BIBM, ICDEW, etc) |
| ACL Anthology | https://aclanthology.org | NLP conferences (ACL, EMNLP, NAACL) |
| PubMed | https://pubmed.ncbi.nlm.nih.gov | Clinical literature on suicide prevention and screening |

---

## Datasets relevant to this task

| Dataset | URL | Task | Notes |
|---------|-----|------|-------|
| Human-AI-Dialogue-Suicide-Risk | https://doi.org/10.5281/zenodo.18684594 | 5-level suicide risk (Chen et al. 2026) | The corpus the assignment cases are drawn from. |
| D4 | https://arxiv.org/abs/2205.11764 | depression dialogue | Used by DALE and Zhang et al. |
| CSSRS Reddit | https://github.com/AmanuelF/Suicide-Risk-Assessment-using-Reddit | 5-level suicide risk | Reddit corpus annotated by 4 psychiatrists. |
| Dreaddit | https://github.com/gillian-perkins/dreaddit | binary stress | Reddit. |
| eRisk 2018 | https://erisk.irlab.org/2018/ | binary depression | CLEF lab corpus. |
| twitter-suicidal-data | https://www.kaggle.com/datasets/nikhileswarkomati/suicide-watch | binary suicide | Kaggle, used by SENTINEL-LLM. |

---

## Clinical instruments

| Instrument | URL | Use |
|------------|-----|-----|
| C-SSRS (Columbia Suicide Severity Rating Scale) | https://cssrs.columbia.edu/ | Six-item suicide-risk assessment used by Scale-CoT. |
| PHQ-9 (Patient Health Questionnaire) | https://www.apa.org/depression-guideline/patient-health-questionnaire.pdf | Depression severity. |
| BAI (Beck Anxiety Inventory) | https://www.apa.org/pi/about/publications/caregivers/practice-settings/assessment/tools/beck-anxiety | Anxiety severity. |

---

## Conferences and journals to monitor

For LLM-based mental health detection, the active venues are:

- **IEEE BIBM** - International Conference on Bioinformatics and Biomedicine. Both Scale-CoT and DALE were published here.
- **ACL / EMNLP / NAACL** - top NLP conferences; mental-health applications appear in dedicated workshops (CLPsych in particular).
- **CLPsych** - Computational Linguistics and Clinical Psychology workshop, hosted at NAACL or ACL.
- **JMIR Mental Health** - journal coverage of digital mental health interventions.
- **NeurIPS / ICLR** - foundational LLM and PEFT papers.
- **AAAI / IJCAI** - applied AI papers including clinical decision support.

---

## Tools used in this project

| Tool | URL | Purpose |
|------|-----|---------|
| Hugging Face Hub | https://huggingface.co | Model weights, tokenisers, datasets. |
| HF transformers | https://github.com/huggingface/transformers | Loading and serving Llama-3 / Qwen-2.5. |
| bitsandbytes | https://github.com/TimDettmers/bitsandbytes | 4-bit NF4 quantisation. |
| PEFT | https://github.com/huggingface/peft | LoRA / QLoRA for the DALE-style adapters. |
| vLLM | https://github.com/vllm-project/vllm | High-throughput on-prem inference server. |
| Ollama | https://ollama.com | Lightweight local model serving for development. |
| Google Colab | https://colab.research.google.com | Free T4 GPU for the proof of concept. |

---

## Australian AI ethics resources

| Resource | URL | Purpose |
|----------|-----|---------|
| AI Ethics Principles | https://www.industry.gov.au/publications/australias-artificial-intelligence-ethics-framework/australias-ai-ethics-principles | The eight principles I map against in `ethics/`. |
| AI Impact Navigator | https://www.industry.gov.au/publications/voluntary-ai-safety-standard | Risk-assessment framework for AI deployment. |
| Voluntary AI Safety Standard | https://www.industry.gov.au/publications/voluntary-ai-safety-standard | Standard published 2024 to operationalise the principles. |
| Privacy Act 1988 (Cth) | https://www.legislation.gov.au/C2004A03712 | Federal privacy legislation. |
| Australian Privacy Principles | https://www.oaic.gov.au/privacy/australian-privacy-principles | Practical APP guidelines. |

---

## UN sustainable development context

| Resource | URL | Purpose |
|----------|-----|---------|
| UN SDG 3 (Good Health and Well-being) | https://sdgs.un.org/goals/goal3 | Primary alignment of the project. |
| UN SDG 10 (Reduced Inequalities) | https://sdgs.un.org/goals/goal10 | Secondary alignment via geographic/socioeconomic reach. |
| WHO Suicide fact sheet | https://www.who.int/news-room/fact-sheets/detail/suicide | Source of the 720,000+ deaths/year statistic. |
| WHO World Mental Health Report 2022 | https://www.who.int/publications/i/item/9789240049338 | Source of the one-billion-people-with-mental-disorder statistic. |

---

## Carbon footprint estimation

| Resource | URL | Purpose |
|----------|-----|---------|
| ML CO2 Impact calculator | https://mlco2.github.io/impact/ | Estimating training and inference emissions. |
| Lacoste et al. (2019), Quantifying Carbon | https://arxiv.org/abs/1910.09700 | The methodology behind the calculator. |
| Australian grid carbon intensity | https://www.aer.gov.au/wholesale-markets | Used for the Australian factor in the report. |
