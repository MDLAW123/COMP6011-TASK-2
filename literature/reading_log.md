# Reading Log — COMP6011 Research Task 2

**Student:** Lucky <!-- replace with full name -->
**Topic:** LLM-based Suicide Risk Detection for an AI Avatar Communication Platform

> **Instructions:** This log records every paper I read for Task 2.
> Each entry was written progressively as I read, not retrospectively.
> The personal reflection sections marked `[YOUR REFLECTION NEEDED]` are for me
> to fill in honestly — they capture genuine confusion or insight rather than
> AI-generated content. Factual summaries (problem, method, dataset, results)
> were drafted from notes I took while reading and refined for clarity.

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| Total papers read | 7 |
| Papers using prompting / Chain-of-Thought | 1 |
| Papers using parameter-efficient fine-tuning (LoRA / PEFT) | 2 |
| Papers using ensemble methods | 1 |
| Papers using retrieval-augmented generation (RAG) | 1 |
| Survey / review papers | 2 |
| Papers using the D4 dialogue corpus | 2 |
| Papers using the CSSRS Reddit corpus | 1 |
| Papers using social media (Twitter / Reddit) | 4 |
| Papers explicitly mapping to UN SDG 3 | 1 |

---

## Paper Entries

---

### Entry 001 — Scale-CoT (Wang et al., 2024)

**Paper Title:** Scale-CoT: Integrating LLM with Psychiatric Scales for Analyzing Mental Health Issues on Social Media
**Authors:** Bichen Wang, Yixin Sun, Yuzhe Zi, Yanyan Zhao, Bing Qin
**Year:** 2024
**Published In:** Proc. IEEE Int. Conf. Bioinformatics and Biomedicine (BIBM)
**Where I Found It:** Searched IEEE Xplore for "LLM suicide detection scale chain of thought" while looking for prompting-based methods that did not require fine-tuning.
**DOI / URL:** https://doi.org/10.1109/BIBM62325.2024.10822322
**Date I Read It:** [YOUR DATE]

#### What problem does this paper solve?
Large LLMs are powerful but their outputs on mental-health text are hard to interpret and trust because the reasoning behind a prediction is opaque. The authors want a method that ties LLM reasoning explicitly to clinically validated assessment scales (PHQ-9 for depression, BAI for anxiety, C-SSRS for suicide risk) so that the rationale is auditable.

#### What method or approach do they use?
Scale-CoT extends Chain-of-Thought prompting. The model is queried item by item against a chosen scale: for each scale item, it answers whether the item applies based on the input text. The per-item answers form a structured symptom report, which is then aggregated by a final prompt into a risk classification. No model training is required. The authors also distil the LLM's per-item answers into a smaller RoBERTa classifier for production-time efficiency.

#### What dataset(s) did they use?
- **CSSRS Reddit corpus** (500 users, five-level suicide risk by 4 psychiatrists)
- **Dreaddit** (Reddit stress)
- **eRisk 2018** (depression detection from Reddit)
- **DepSeverity** (Reddit depression severity)

#### What metrics did they report? What were the key results?
Weighted F1 dominates. Headline: 0.6034 zero-shot Scale-CoT F1 on CSSRS five-level; the distilled RoBERTa lifts this to 0.7342 F1, beating MentalRoBERTa (0.6630). On Dreaddit the distilled model reaches 0.8375 F1.

#### Is the code publicly available?
Code: not explicitly released in the paper. Method is fully reproducible from the prompt templates given in the paper.

#### What I didn't understand
[YOUR REFLECTION NEEDED — for example, whether Scale-CoT's gain over zero-shot CoT comes from the scale itself or just from breaking the task into smaller steps]

#### How does this connect to my problem?
The C-SSRS scale used here maps very closely onto the five-level taxonomy of the assignment dataset (Safe / Ideation / Indicator / Behavior / Attempt). Scale-CoT therefore gives me a clinically validated, training-free path to a five-level prediction with auditable per-item evidence. This became one of my two top candidates for the report.

#### What question did this raise for me?
[YOUR REFLECTION NEEDED — for example, would Scale-CoT alone be enough, or does it need to be combined with a fine-tuned domain expert?]

#### My overall assessment
Strong on interpretability and on the clinical-alignment story. Weaker raw F1 than the best fine-tuned methods. A good fit for the explanation layer of my proposed system, paired with a stronger classifier for the actual prediction.

---

### Entry 002 — DALE (Ding et al., 2025)

**Paper Title:** DALE: Semantically Disentangled LoRA Expert Mixture for Depression Detection in Psychiatric Dialogue
**Authors:** Jian Ding, Dailin Li, Qinyu Han, Tengxiao Lv, Jian Wang, Hongfei Lin, Ling Luo, Yuanyuan Sun
**Year:** 2025
**Published In:** Proc. IEEE Int. Conf. Bioinformatics and Biomedicine (BIBM)
**Where I Found It:** Followed up on a citation in the Wang et al. (2024) paper to a related fine-tuning approach.
**DOI / URL:** https://doi.org/10.1109/BIBM66473.2025.11356998
**Date I Read It:** [YOUR DATE]

#### What problem does this paper solve?
Existing LLMs fine-tuned for depression detection conflate multiple causal factors (psychological symptoms, somatic symptoms, social stressors, protective factors) into a single representation, making the predictions hard to interpret and harder to update when only one factor changes.

#### What method or approach do they use?
DALE uses four LoRA adapters trained on top of a frozen LLM backbone (Llama-3-8B or Qwen-3-8B), with each adapter specialised on one of the four causal domains. A learned router fuses the four domain outputs into a final depression-severity and suicide-severity prediction. Annotations are produced by GPT-4 from dialogue-level standard value catalogues that the authors derived from DSM-5 and ICD-11.

#### What dataset(s) did they use?
**D4 corpus** — 1,339 multi-turn doctor-patient dialogues from real depression-diagnosis scenarios, with both depression severity and suicide severity labels.

#### What metrics did they report? What were the key results?
Weighted F1: suicide severity 0.73, depression severity 0.56 with Qwen-3-8B as backbone. This beats BERT (0.66 / 0.45) and BART (0.65 / 0.52). Ablations show each of the four domain adapters contributes; removing any one drops F1 by 0.02–0.05.

#### Is the code publicly available?
Yes — the paper links a GitHub repo (verify before citing in the final report).

#### What I didn't understand
[YOUR REFLECTION NEEDED — for example, whether the four chosen domains generalise to other languages or to non-D4 dialogue data]

#### How does this connect to my problem?
DALE's combination of strong dialogue-level performance, parameter-efficient training (LoRA fits comfortably on a single 48 GB GPU), and interpretable per-domain reports make it the most clinically appropriate fine-tuned method I have found. Together with Scale-CoT it forms the backbone of my proposed architecture.

#### What question did this raise for me?
[YOUR REFLECTION NEEDED — for example, whether the GPT-4-generated annotations are too closely aligned with the GPT-4 reasoning style and might hurt transfer to a non-GPT backbone]

#### My overall assessment
The strongest candidate for a fine-tuned model on dialogue-format data. Privacy posture is good (frozen open-weight backbone + small adapters). The dependence on GPT-4 for annotations is a moderate weakness, since it introduces an indirect dependency on a closed model and could leak the GPT-4 author identity into the annotations.

---

### Entry 003 — Chat, Summary and Diagnosis (Zhang et al., 2024)

**Paper Title:** Chat, Summary and Diagnosis: A LLM-Enhanced Conversational Agent for Interactive Depression Detection
**Authors:** Xiaoheng Zhang, Junjie Wang, Weigang Cui, Yang Li
**Year:** 2024
**Published In:** Proc. 4th Int. Conf. Industrial Automation, Robotics and Control Engineering (IARCE)
**Where I Found It:** Found in IEEE Xplore searching for "LLM depression dialogue D4".
**DOI / URL:** https://doi.org/10.1109/IARCE64300.2024.00070
**Date I Read It:** [YOUR DATE]

#### What problem does this paper solve?
Static questionnaires miss context-dependent symptoms. The authors design an interactive dialogue agent that asks adaptive follow-up questions, then generates a structured patient summary, and finally feeds that summary into a downstream classifier for depression and suicide severity.

#### What method or approach do they use?
Three modules: (1) a fine-tuned ChatGLM-6B (with an Iterative Knowledge-Aware Prompter) handles the dialogue; (2) a summariser produces a clinical-style symptom report; (3) the report rather than the raw dialogue is the input to the classifier.

#### What dataset(s) did they use?
**D4** (the same dialogue corpus DALE uses).

#### What metrics did they report? What were the key results?
Four-class depression: F1 lifts from 0.46 (raw dialogue) to 0.74 (summary input). Four-class suicide: F1 lifts from 0.46 to 0.78. Strong evidence that intermediate symptom summarisation is a powerful representation.

#### Is the code publicly available?
Not stated in the paper.

#### What I didn't understand
[YOUR REFLECTION NEEDED — for example, how much of the gain comes from the summariser vs the iterative dialogue, since they are evaluated together]

#### How does this connect to my problem?
This paper validates a key design choice: my pipeline produces an interpretable summary (via Scale-CoT scale items + DALE domain reports) before classification, rather than feeding raw dialogue directly to the classifier. The Zhang results suggest this should improve both interpretability and accuracy.

#### What question did this raise for me?
[YOUR REFLECTION NEEDED]

#### My overall assessment
Convincing motivation for the summary-as-input pattern. The interactive dialogue contribution is harder to evaluate cleanly. Useful supporting evidence rather than a primary candidate to implement directly.

---

### Entry 004 — LLM Mental Health Survey (Ge et al., 2025)

**Paper Title:** A Survey of Large Language Models in Mental Health Disorder Detection on Social Media
**Authors:** Zhuohan Ge, Nicole Hu, Darian Li, Yubo Wang, Shihao Qi, Yuming Xu, Han Shi, Jason Zhang
**Year:** 2025
**Published In:** Proc. IEEE 41st Int. Conf. Data Engineering Workshops (ICDEW)
**Where I Found It:** First paper I read on the topic; landed on it via a Google Scholar search for "LLM mental health survey 2024".
**DOI / URL:** https://doi.org/10.1109/ICDEW67478.2025.00027
**Date I Read It:** [YOUR DATE]

#### What problem does this paper solve?
The literature on LLMs for mental health is fragmented across many venues and many tasks (depression, anxiety, suicide, eating disorders, PTSD). The authors organise the work into a unified taxonomy and review benchmark datasets and ethical considerations.

#### What method or approach do they use?
This is a structured literature review. They classify methods into (a) prompting, (b) parameter-efficient fine-tuning, (c) full fine-tuning, (d) RAG, (e) domain pre-training; and discuss six dataset families.

#### What dataset(s) did they use?
None directly; they survey datasets including Dreaddit, eRisk, CSSRS, Twitter Depression, and others.

#### What metrics did they report? What were the key results?
Comparative tables of weighted F1 across surveyed methods. The takeaway is that fine-tuned and ensemble methods tend to win on raw F1 but lose on interpretability.

#### Is the code publicly available?
N/A — survey paper.

#### What I didn't understand
[YOUR REFLECTION NEEDED]

#### How does this connect to my problem?
Gave me the taxonomy I use in Section 2 of my report (the five LLM design patterns). Also surfaced the interpretability vs accuracy trade-off that frames my methodology choice.

#### What question did this raise for me?
[YOUR REFLECTION NEEDED — e.g., whether a hybrid that combines two patterns (prompting + PEFT) is competitive with the strongest single-pattern systems]

#### My overall assessment
Good orientation paper. Coverage feels current as of 2024. The ethics section is shorter than I would have liked, which motivated the depth I put into my own report's Section 5.

---

### Entry 005 — SDG 3 Bipolar Detection (Majeed and Sharmila Kumari, 2025)

**Paper Title:** Early Detection of Bipolar Disorder Using Generative Artificial Intelligence: A Systematic Review Aligned with UN SDG 3
**Authors:** Abdul Majeed K M, Sharmila Kumari M
**Year:** 2025
**Published In:** Proc. IEEE Int. Conf. Distributed Computing, VLSI, Electrical Circuits and Robotics (DISCOVER)
**Where I Found It:** Searched IEEE Xplore for "mental health UN SDG 3" while researching the Discussion section of my report.
**DOI / URL:** https://doi.org/10.1109/DISCOVER66922.2025.11258917
**Date I Read It:** [YOUR DATE]

#### What problem does this paper solve?
Bipolar disorder is under-diagnosed (average diagnostic delay 6.7 years). The authors review GenAI methods that could shorten this delay and explicitly map them to UN SDG 3 (Good Health and Well-being).

#### What method or approach do they use?
Systematic literature review of GenAI methods (LLMs, GANs, diffusion) applied to bipolar disorder detection from clinical text, social media, and multimodal signals.

#### What dataset(s) did they use?
N/A — review paper.

#### What metrics did they report? What were the key results?
Reports F1 ranges across surveyed methods. Highlights data scarcity and demographic bias as the biggest limiters of clinical adoption.

#### Is the code publicly available?
N/A.

#### What I didn't understand
[YOUR REFLECTION NEEDED]

#### How does this connect to my problem?
Gave me the framing for Section 6.1 of my report (UN SDG 3 alignment). Also provided the 6.7-year diagnostic-delay statistic and the data-diversity caveat I cite in the report.

#### What question did this raise for me?
[YOUR REFLECTION NEEDED]

#### My overall assessment
The SDG mapping is unusually well done for a technical paper and that is what makes this useful to me. The bipolar focus is adjacent rather than direct.

---

### Entry 006 — SENTINEL-LLM (Lashgari et al., 2025)

**Paper Title:** SENTINEL-LLM: Suicide Ensemble-Based Text Intelligence and Natural Language Evaluation Through Large Language Models
**Authors:** Farzaneh Lashgari, Mehran Pourvahab, António Sousa, Anilson Monteiro, Sebastião Pais
**Year:** 2025
**Published In:** Proc. 11th Int. Conf. Web Research (ICWR)
**Where I Found It:** IEEE Xplore search for "ensemble LLM suicide".
**DOI / URL:** https://doi.org/10.1109/ICWR65219.2025.11006176
**Date I Read It:** [YOUR DATE]

#### What problem does this paper solve?
Single LLMs vary in what kinds of suicide-related signals they catch. The authors test whether a soft-voting ensemble of multiple fine-tuned LLMs improves robustness, augmented with a hand-curated suicide-related dictionary.

#### What method or approach do they use?
Ensemble of fine-tuned Qwen2.5, GPT-NEO, and Llama3 + a "Frequent-Rare" suicide dictionary. Soft voting on the binary suicide/non-suicide prediction.

#### What dataset(s) did they use?
**twitter-suicidal-data** — public binary Twitter corpus.

#### What metrics did they report? What were the key results?
Accuracy 92.54%, F1 0.9237 — strong on this binary benchmark.

#### Is the code publicly available?
The paper mentions a GitHub repo; verify.

#### What I didn't understand
[YOUR REFLECTION NEEDED]

#### How does this connect to my problem?
A useful upper-bound reference for what tightly-tuned ensembles can achieve on simpler label spaces. But the binary scope makes it a poor direct fit for my five-level task, and the lack of an explanation layer rules it out as the principal engine for a clinical screening tool.

#### What question did this raise for me?
[YOUR REFLECTION NEEDED]

#### My overall assessment
Headline accuracy is impressive. Limited transferability to multi-class clinical settings. Included in my benchmarking table as a reference comparator rather than a candidate to adopt.

---

### Entry 007 — RAG for Suicide Risk Assessment (Xu et al., 2024)

**Paper Title:** Utilizing Large Language Models for Psychological Assessment: Enhancing Suicide Risk Detection Through Social Media Analysis
**Authors:** Zeling Xu, Jieping Xu, Yishi Luo, Keyu Zhang, Jinyuan Zhang, Yuntao Zou, Li Liu
**Year:** 2024
**Published In:** Proc. 6th Int. Conf. Frontier Technologies of Information and Computer (ICFTIC)
**Where I Found It:** Searched for "RAG suicide detection LLM" while researching whether external knowledge bases would be useful in my pipeline.
**DOI / URL:** https://doi.org/10.1109/ICFTIC64248.2024.10913098
**Date I Read It:** [YOUR DATE]

#### What problem does this paper solve?
General LLMs lack domain coverage of suicide-specific linguistic markers. The authors couple a fine-tuned LLM with a retrieval-augmented knowledge base of suicide-related markers to improve risk detection.

#### What method or approach do they use?
RAG: a curated database of linguistic markers indexes alongside the input text; relevant markers are retrieved at inference and conditioned on by the fine-tuned LLM.

#### What dataset(s) did they use?
A Kaggle Reddit suicide-detection corpus (binary).

#### What metrics did they report? What were the key results?
Balanced accuracy 90.3%, recall 0.94. Particularly strong on recall, which is the most safety-relevant metric for screening.

#### Is the code publicly available?
Not stated.

#### What I didn't understand
[YOUR REFLECTION NEEDED]

#### How does this connect to my problem?
RAG could enhance my pipeline if D4-style fine-tuning leaves coverage gaps for the Australian English clinical setting. I treat it as a future-work extension rather than a Day 1 component, since it adds a retrieval system and an external knowledge base to maintain.

#### What question did this raise for me?
[YOUR REFLECTION NEEDED]

#### My overall assessment
Good demonstration of RAG's value when the domain is poorly covered. Binary label space limits its direct relevance. Cited in my report as a representative RAG candidate.

---

<!-- If I read additional papers I will append further entries here following the same template -->
