# Methodology - Design Decisions

This file documents the rationale behind the methodology proposed in Section 4 of my report. It exists so that a marker (or a future-me revisiting the project) can see *why* each choice was made, not just *what* the choice was.

---

## 1. Pipeline Overview

```
User dialogue
    |
    v
Scale-CoT (six C-SSRS items, sequential queries to backbone)
    |
    v
LoRA adapter bank (four DALE-style domain experts)
    |
    v
Router + 5-level classifier
    |
    v
Explanation layer (per-item evidence + per-domain report)
    |
    v
Clinician review and escalation
```

The dashed boundary in the report's Figure 2 indicates the on-premises trust zone. No dialogue text crosses it; the only outputs that leave are the predicted risk level and the structured explanation, and even those go to a clinician within the same hospital network.

---

## 2. Why this base model

**Choice:** Llama-3-8B-Instruct, with Qwen-2.5-7B-Instruct as fallback.

**Rationale:**
- Open weights, deployable on premises (lecturer's hard constraint on privacy).
- 8B parameters fit on a single 48 GB GPU (4-bit NF4 quantisation), or even on a 16 GB T4 in Colab for the proof of concept.
- Strong instruction following and reasoning, both required by Scale-CoT.
- Active community support and pre-existing LoRA recipes that DALE-style training can build on.
- Fallback to Qwen-2.5-7B is documented in the notebook because Llama-3 is gated behind a Meta licence that takes time to approve.

**Rejected alternatives:**
- *GPT-4 / Claude / Gemini via API.* Highest raw capability, but transmitting clinical dialogue to a third-party API breaks the on-premises requirement. Not viable.
- *MentaLLaMA (domain pre-trained).* Strong in-domain performance but the public weights lag the latest base models, and continued pre-training is expensive when dialogue style shifts.
- *Smaller models (Phi-3, TinyLlama).* Fit on cheaper hardware but the per-item Scale-CoT instruction-following degrades; tested in a smoke run and rejected.

---

## 3. Why Scale-CoT plus DALE rather than either alone

**Scale-CoT alone:** Excellent interpretability and zero training cost, but raw F1 trails fine-tuned methods by several percentage points (0.6034 zero-shot on CSSRS vs 0.73 weighted F1 for DALE on D4 suicide).

**DALE alone:** Strongest dialogue-format F1, but the per-domain reports do not align with clinical instruments the way Scale-CoT items do. Clinicians are trained on C-SSRS and PHQ-9; they are not trained on DALE's four causal domains.

**Combined:** Scale-CoT runs at inference time over the same backbone DALE has been adapted on. The Scale-CoT item answers and the DALE domain reports are concatenated and fed to a small router. The system gets DALE's accuracy *and* Scale-CoT's clinically-aligned explanation. This is novel relative to either paper individually and is positioned as a contribution in my report.

---

## 4. Why C-SSRS specifically (and the five-level mapping)

**Choice:** Columbia Suicide Severity Rating Scale (Posner et al., 2011).

**Rationale:**
- Widely validated in clinical practice (international, multilingual translations).
- Six discrete items map cleanly to the five labels in the assignment dataset.
- Each item is binary (yes / no), which makes prompting reliable and parsing deterministic.

**Item-to-label mapping rule:**

| C-SSRS items endorsed | Mapped label |
|-----------------------|--------------|
| Item 6 (actual or interrupted attempt) | Attempt |
| Items 4 or 5 (specific plan, preparatory acts) | Behavior |
| Item 3 (ideation with intent / hopelessness / burdensomeness) | Indicator |
| Items 1 or 2 (passive ideation, active ideation without method) | Ideation |
| No item endorsed | Safe |

The rule is conservative: in a tie or a near-tie, the higher-risk label is chosen. This biases the system toward over-flagging rather than under-flagging, which is the safer error for a screening tool whose missed cases can be fatal.

---

## 5. Data strategy

**Adaptation data (training):**
- D4 corpus (Du et al., 2023; used by Ding et al., 2025 and Zhang et al., 2024).
- 1,339 multi-turn doctor-patient depression-diagnosis dialogues with depression and suicide severity labels.
- Public, research-licensed, ethically collected with informed consent.

**Domain adaptation data (planned):**
- Australian English clinical dialogue collected at the partner clinic under explicit informed consent.
- Identifiers removed before training; differential privacy applied to fine-tuning if patient text is used.
- Quarterly demographic-subgroup audits.

**Evaluation data:**
- The ten paraphrased cases provided for the assignment, used **only** for the proof of concept. Not seen during any training stage. Per the unit's ethical guidelines, all local copies are deleted on completion of the assessment.

---

## 6. Privacy and deployment

**Constraint:** Private dialogue must not be sent to public AI services. This is non-negotiable in the unit's guidelines.

**Implementation:**

| Layer | Choice | Why |
|-------|--------|-----|
| Hosting | On-premises GPU server inside hospital network | No external network egress for inference. |
| Model | Llama-3-8B-Instruct, 4-bit NF4 quantised | Fits a single 48 GB GPU; private weights. |
| Serving | vLLM or text-generation-inference | Continuous batching at clinical latency. |
| Encryption | TLS in transit, LUKS at rest | Standard health-IT baseline. |
| Audit logs | Every inference logged with prompt + output | Required for contestability and incident review. |
| Identity | Role-based access control | Clinicians, IT, and engineers have different scopes. |

For training, the on-prem server runs without external network access. Public pretrained weights are downloaded once, verified by checksum, then air-gapped.

---

## 7. Operational safeguards

Beyond the technical stack, three operational controls are mandated:

1. **Mirroring to a duty clinician.** Every prediction above the *Safe* threshold is mirrored to a clinician within minutes; *Behavior* or *Attempt* triggers an automated escalation to a 24-hour crisis line.
2. **Shadow-deployment evaluation.** A rolling 5% sample is independently labelled by clinicians and compared to model predictions to detect drift.
3. **Documented rollback procedure.** The engine can be disabled without disrupting human-led screening, since the model never replaces a clinician.

---

## 8. Alternatives considered and rejected

**Pure RAG (Xu et al., 2024 style):** Excellent recall on binary detection, but adds a retrieval index that must be maintained and audited. Treated as future work rather than a Day-1 component.

**SENTINEL-LLM ensemble:** Highest binary accuracy but no explanation layer and 3x training cost. Rejected for clinical adoption.

**Domain pre-training (MentaLLaMA-style):** Continued pre-training on a large mental-health corpus. High training cost, slower iteration, and existing public weights lag the latest base models. Rejected in favour of LoRA.

**Closed-weight commercial LLMs:** Highest raw capability but break the privacy constraint. Not viable.

---

## 9. Open questions for development

These are flagged for the development phase that follows the assignment:

1. Do the four DALE domains (psychological, somatic, protective, stressors) survive transfer from D4 (Chinese clinical) to Australian English clinical text? This needs an ablation on the partner-clinic dataset before production.
2. What is the right frequency for the demographic-subgroup audit? The Majeed and Sharmila Kumari (2025) review suggests quarterly is a defensible default, but more frequent monitoring may be needed in early deployment.
3. How should the system handle non-English languages spoken in the Australian catchment population? Multilingual extension is in the report's Future Work; a concrete plan is still required.
4. What is the calibration of the five-level output, and does it support the risk-stratification dashboards that clinicians will rely on? Calibration metrics are unreported in all surveyed papers and need primary measurement.
