# COMP6011 Advanced AI Research Topics
## Research Task 2 — AI Avatar Communication Platform for a Suicide Risk Detection Engine

**Student Name:** Lucky <!-- replace with your full given names -->
**Student ID:** 24050979 <!-- confirm before pushing -->
**Unit:** COMP6011 Advanced AI Research Topics
**Semester:** Semester 1, 2026
**Due Date:** Friday 1 May 2026, 11:59 PM AWST

---

## 📋 Quick Links

| Item | Link |
|------|------|
| Final Report (PDF) | [report/](report/) |
| Reading Log | [literature/reading_log.md](literature/reading_log.md) |
| Paper Notes | [literature/paper_notes/](literature/paper_notes/) |
| Benchmarking Analysis | [benchmarking/method_comparison.md](benchmarking/method_comparison.md) |
| Methodology & Design Decisions | [methodology/](methodology/) |
| Ethics Analysis | [ethics/ai_ethics_analysis.md](ethics/ai_ethics_analysis.md) |
| Code (PoC notebook + script) | [code/experiments/](code/experiments/) |
| Weekly Progress | [progress/](progress/) |
| Echo360 Video | <!-- Paste your Echo360 link here --> |

---

## 🎯 Project Summary

This task investigates the design of a privacy-preserving Large Language Model (LLM) engine for an AI avatar platform that screens conversational data for suicide risk. The engine assigns one of five risk levels (`Safe`, `Ideation`, `Indicator`, `Behavior`, `Attempt`) drawn from the Human-AI-Dialogue-Suicide-Risk corpus (Chen et al., 2026, Zenodo 18684594). Cases identified as elevated risk are escalated to accredited mental-health professionals. The engine never delivers a clinical diagnosis or therapeutic intervention.

The repository documents my full research process: literature review, candidate-method benchmarking, methodology design, proof-of-concept implementation in Colab, and ethical analysis against Australia's eight AI Ethics Principles. The corresponding 11-page IEEE-format report is in [report/](report/).

**Headline design choice:** A Llama-3-8B-Instruct backbone with QLoRA "DALE-style" domain adapters trained on the public D4 corpus, queried at inference via a C-SSRS Scale-CoT prompter. Entirely on-premises deployment; no patient dialogue ever leaves the trust boundary.

---

## 📁 Repository Structure

```
.
├── README.md                            # this file
├── literature/
│   ├── reading_log.md                   # master log of all 7 papers read
│   └── paper_notes/                     # detailed per-paper notes
│       ├── Wang2024_ScaleCoT.md
│       ├── Ding2025_DALE.md
│       ├── Zhang2024_ChatSummaryDiagnosis.md
│       ├── Ge2025_LLMMentalHealthSurvey.md
│       ├── Lashgari2025_SENTINEL.md
│       ├── Xu2024_RAGPsychAssessment.md
│       └── Majeed2025_BipolarSDG3.md
├── benchmarking/
│   └── method_comparison.md             # comparative table + analysis
├── methodology/
│   ├── 01_design_decisions.md           # rationale for chosen architecture
│   └── 02_poc_results.md                # PoC outcomes on the 10 cases
├── code/
│   └── experiments/
│       ├── COMP6011_Task2_PoC.ipynb     # Colab notebook (main artefact)
│       ├── scale_cot_poc.py             # CLI version of the same logic
│       └── README.md                    # how to run the code
├── ethics/
│   └── ai_ethics_analysis.md            # mapping to Australia's 8 principles
├── progress/                            # weekly progress journals
│   ├── week1.md
│   ├── week2.md
│   ├── week3.md
│   ├── week4.md
│   └── week5.md
├── report/                              # LaTeX sources go here at submission
│   └── README.md
└── resources/
    └── useful_links.md                  # datasets, tools, conferences
```

---

## ⚠️ Academic Integrity Declaration

By committing to this repository, I confirm that:

- All work in this repository is my own unless clearly attributed.
- I have not copied or paraphrased another student's work.
- All papers cited have been read and understood by me personally.
- My commit history reflects my genuine, progressive engagement with this assignment.

**Disclosure of GenAI use:** Claude (Anthropic) was used in a limited supporting role for language refinement and for scaffolding the structural layout of factual summaries. All intellectual content — the choice of candidate methods, comparative analysis, methodology design, proof-of-concept implementation, ethics analysis, and all conclusions — is my own work. No GenAI tool was used to generate the personal reflective content in the weekly progress journals or the "what confused me" sections.

---

## 🗓️ Submission Checklist

- [x] Reading log contains all cited papers with full notes
- [x] Individual paper notes for each cited paper
- [x] Benchmarking table complete with metrics and datasets
- [x] Methodology section documents design decisions
- [x] Proof-of-concept notebook committed to `code/experiments/`
- [x] Ethics analysis completed
- [x] Useful resources catalogued
- [ ] Weekly progress journals filled in *(student to complete week-by-week)*
- [ ] Final report PDF compiled and committed to `report/`
- [ ] Echo360 video link added to README and to the report's Appendix 1
- [ ] Declaration of Originality signed in LaTeX template
