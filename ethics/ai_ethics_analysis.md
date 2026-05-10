# AI Ethics Analysis - COMP6011 Task 2

This file records how the proposed system maps onto Australia's eight AI Ethics Principles (Department of Industry, Science and Resources, 2019, updated 2024). The analysis goes deeper than the report's Section 5 because the page limit forced concision there.

Each principle has three blocks: what the principle says, how the system addresses it, and the residual risks that I am explicit about.

---

## Principle 1: Human, Societal and Environmental Wellbeing

**Principle:** AI systems should benefit individuals, society, and the environment.

**How addressed:**
- Designed to reduce preventable suicide mortality and to extend access to early screening.
- Particular benefit to populations underserved by face-to-face psychiatric services (rural, remote, low-income).
- Environmental impact constrained by on-premises inference rather than continuous cloud calls. Estimated lifecycle emissions in Section 6.2 of the report: training adapters approximately 1.32 kg CO2eq, annual inference at 50,000 dialogues approximately 10.3 kg CO2eq.

**Residual risks:**
- A poorly calibrated system could increase demand on already-stretched mental health services through false positives. Mitigated by per-class threshold tuning and by the human review step.
- Concentrating mental health screening through a single technology stack creates a single point of failure. Mitigated by the documented rollback procedure that lets the engine be disabled without disrupting human-led screening.

---

## Principle 2: Human-Centred Values

**Principle:** AI systems should respect human rights, diversity, and the autonomy of individuals.

**How addressed:**
- The engine never delivers a clinical diagnosis or therapeutic recommendation directly to the user.
- All elevated-risk outputs are routed to accredited mental-health professionals.
- Users retain the right to refuse the AI screening and request a fully human review at no cost.
- Clinical judgement remains central; the model is positioned as a triage assistant, not a decision-maker.

**Residual risks:**
- Power asymmetry: a service user may feel pressured to accept the AI screening because alternative pathways take longer. Mitigated by clear, plain-language disclosure and by ensuring that the human pathway is genuinely accessible, not just nominally available.

---

## Principle 3: Fairness

**Principle:** AI systems should be inclusive and accessible, and not unfairly discriminate.

**How addressed:**
- Training corpus supplemented with demographically diverse Australian dialogue samples.
- Quarterly post-hoc subgroup performance audits (by age band, gender, language).
- Aggregate fairness metrics published alongside the engine's release notes.
- Multilingual extension to the principal community languages of the catchment population is in the future-work roadmap.

**Residual risks:**
- D4 is Chinese-language and CSSRS Reddit is English-language; both skew toward majority demographics in their respective populations. Australian Indigenous and culturally-and-linguistically-diverse (CALD) communities are likely under-represented. Mitigated by domain adaptation on partner-clinic data with explicit demographic balancing, and by the public commitment to publish subgroup metrics.
- Bias in psychiatric instruments themselves (the C-SSRS was developed in a US context) may transfer into the model. The fairness audit needs to include not just model-level but also instrument-level bias.

---

## Principle 4: Privacy Protection and Security

**Principle:** AI systems should respect and uphold privacy rights and data protection.

**How addressed:**
- All dialogue processed entirely on premises. No data is transmitted to ChatGPT or any other public AI service - this is the lecturer's hard constraint, and is the central design decision of the system.
- Patient identifiers removed before storage.
- Encryption at rest (LUKS) and in transit (TLS) is mandatory.
- Role-based access control restricts who can see raw text vs aggregated dashboards.
- HL7 FHIR-aligned data governance for integration with the electronic medical record.
- Logs segmented: raw text only in the highest-trust zone, only de-identified summary statistics in monitoring dashboards.

**Compliance with Australian regulations:**
- Privacy Act 1988 and the Australian Privacy Principles.
- State-level health records legislation (HRIP Act in NSW, HRA in Victoria, etc).
- HIPAA-equivalent expectations where collaborating with overseas insurers or research partners.

**Residual risks:**
- LLMs can memorise training data; any fine-tuning on real patient text must use differential privacy or rigorous de-identification. Documented in the methodology notes.
- Model outputs themselves can be sensitive: an explanation that names a patient's stressors leaks information if logged carelessly. Mitigated by the segmented logging scheme.
- Insider threats: a clinician with legitimate access to the trust zone could in principle exfiltrate data. Mitigated by audit logging of every read access and by short data-retention windows for raw text.

---

## Principle 5: Reliability and Safety

**Principle:** AI systems should reliably operate in accordance with their intended purpose.

**How addressed:**
- Benchmarked on held-out clinician-labelled evaluation sets (planned: 1,000 dialogues at the partner clinic).
- Continuous drift monitoring via the rolling shadow-deployment evaluation (5% of dialogues independently labelled by clinicians).
- Hard-coded crisis-line escalation when the model returns *Behavior* or *Attempt*.
- Documented rollback procedure to disable the engine without disrupting human-led screening.

**Residual risks:**
- The proof of concept used only 10 cases. The full reliability story rests on the planned 1,000-dialogue prospective evaluation, which is in the future-work roadmap. Until then, the engine should not be deployed beyond shadow mode.
- Adversarial prompts and jailbreak attempts have not been systematically tested. Red-team testing is in the future-work roadmap before any production deployment.
- The system assumes adult, consenting users and is not appropriate for unsupervised use by children or by people in acute crisis without a human safety net. Documented in the limitations section of the report.

---

## Principle 6: Transparency and Explainability

**Principle:** People should be informed when they are being significantly affected by AI, and should be able to find out about the AI making decisions.

**How addressed:**
- Every prediction is accompanied by the C-SSRS scale-item evidence (six binary items) and the four DALE-style domain reports. A clinician can audit the reasoning before acting.
- Model cards and dataset datasheets published for both the backbone and the LoRA adapters.
- Patient-facing plain-language disclosure that AI is used in their screening pathway.
- Open-weight backbone (Llama-3-8B) so that the underlying model is itself inspectable.

**Residual risks:**
- The backbone's pre-training data is Meta's proprietary mix and is not fully disclosed. This is a generic limitation of open-weight LLMs.
- Per-item Scale-CoT evidence is only as informative as the C-SSRS items themselves; if a clinician disagrees with a particular item's framing, the explanation may not satisfy. Mitigated by the option to fall back to a fully human review.

---

## Principle 7: Contestability

**Principle:** When an AI system significantly impacts a person, there should be a timely process to allow them to challenge the use or output.

**How addressed:**
- Patients can request a fully human review at no cost.
- Clinicians can override any model prediction; overrides are logged and feed back into model improvement.
- Audit logs retained for the period mandated by Australian privacy law support after-the-fact contestation.

**Residual risks:**
- Contestation requires the patient to know the AI is involved. Mitigated by the disclosure step, but practically, comprehension of AI roles in clinical pathways is patchy. A literacy uplift programme accompanies the rollout.
- A human reviewer may be unduly influenced by the AI's prediction (anchoring effect). Mitigated by training the reviewer to consider the case independently and by hiding the prediction during initial review when a human is consulted.

---

## Principle 8: Accountability

**Principle:** Those responsible for AI systems should be identifiable and accountable for their outcomes.

**How addressed:**
- A clinical-AI governance committee comprising clinicians, AI engineers, an ethicist, and a consumer representative meets monthly to review incidents and override patterns.
- Every inference is logged with prompt and output for the period mandated by Australian privacy law.
- Roles and responsibilities (clinician, engineer, model owner) are documented and signed off.
- Incident response procedures are published.

**Residual risks:**
- Distributed responsibility between the model vendor (the project team), the deploying organisation (the clinical service), and the human user (the clinician) creates accountability ambiguity if a serious adverse event occurs. Mitigated by a clear chain of responsibility documented in service agreements before deployment.
- The model owner role must outlast the project team; long-term governance arrangements are needed before production deployment.
