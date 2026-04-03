# AI Vendor Intake Form
**AI Governance Checklist Auditor — Clinic Intake Worksheet**

> Complete one form per AI tool. Use this for new vendor evaluation OR annual re-audit.
> Return completed form to your auditor or import into the Python auditor tool.

---

## 1. Vendor Identity

| Field | Response |
|---|---|
| **Vendor / Company Name** | |
| **Product Name** | |
| **Product Version / Release Date** | |
| **Primary Vendor Contact & Email** | |
| **Vendor Website** | |

**AI Tool Category** *(select one)*:
- [ ] Ambient Scribe / Documentation AI (e.g., DAX Copilot, Abridge, Suki)
- [ ] Scheduling & Intake AI
- [ ] Diagnostic / Clinical Decision Support AI
- [ ] Billing & Revenue Cycle Management (RCM) Automation
- [ ] EHR-Integrated AI (Epic, Oracle, Athena, etc.)
- [ ] Patient Engagement / Chatbot
- [ ] Administrative Automation (coding, prior auth, etc.)
- [ ] General-Purpose LLM (ChatGPT, Claude, Gemini — staff-used)
- [ ] Other: ___________

---

## 2. HIPAA & BAA Status

| Question | Response |
|---|---|
| Does this tool access, process, transmit, or store **Protected Health Information (PHI)**? | Yes / No |
| **BAA Status** | Signed / Not Signed / Pending / Not Required / Unknown |
| **BAA Date Signed** | MM/DD/YYYY |
| **BAA Document Location** (file path or folder) | |
| Does the BAA explicitly cover **AI training, fine-tuning, and inference** use cases? | Yes / No / Unknown |
| Does the BAA specify a **breach notification timeline**? | Yes / No |
| If yes, what is the breach notification SLA? | ___ hours |

**PHI Types Accessed** *(check all that apply)*:
- [ ] Patient demographics (name, DOB, address)
- [ ] Clinical notes / encounter summaries
- [ ] Diagnoses / ICD codes
- [ ] Medications / prescriptions
- [ ] Lab results / imaging
- [ ] Insurance / billing information
- [ ] Mental health / substance use records (extra sensitivity)
- [ ] Other: ___________

---

## 3. Data Handling

| Question | Response |
|---|---|
| **Data Residency** | US Only / US + International / International Only / Unknown |
| Does patient data **leave the United States**? | Yes / No / Unknown |
| Is PHI **encrypted at rest**? (standard: AES-256) | Yes / No / Unknown |
| Is PHI **encrypted in transit**? (standard: TLS 1.2+) | Yes / No / Unknown |
| What is the vendor's **data retention period**? | ___ days |
| Describe the vendor's **data deletion / destruction policy**: | |
| Are the vendor's **subprocessors (4th-party vendors)** documented? | Yes / No / Unknown |
| Has the vendor provided a **data flow diagram**? | Yes / No |

---

## 4. AI Model & Training

| Question | Response |
|---|---|
| Does the vendor **disclose what AI model** powers the tool? | Yes / No |
| Is the underlying model **trained on your clinic's patient data**? | Yes / No / Unknown |
| Is the model **fine-tuned using PHI** (with or without consent)? | Yes / No / Unknown |
| If PHI is used for training, is **patient consent** documented? | Yes / No / N/A |
| Is there a **clinician-in-the-loop** requirement (human reviews AI output before it affects care)? | Yes / No |

**Model Training Classification** *(select one)*:
- [ ] Not trained on clinic PHI
- [ ] Trained on PHI with documented patient consent
- [ ] Training data practices unknown
- [ ] Fine-tuned on clinic/patient data

---

## 5. Access Controls & Security

| Question | Response |
|---|---|
| Does the product support **SSO and/or MFA**? | Yes / No |
| Does the product support **Role-Based Access Control (RBAC)**? | Yes / No |
| Does the product provide **audit logs** of user and AI activity? | Yes / No |
| When was the vendor's last **penetration test**? | MM/YYYY or Unknown |
| Does the vendor hold **SOC 2 Type II or HITRUST** certification? | Yes / No / Unknown |
| Has a **Security Risk Assessment (SRA)** been conducted for this tool? | Yes / No |

---

## 6. NIST AI RMF — Govern

| Question | Response |
|---|---|
| Does the vendor have a **published AI governance policy**? | Yes / No / Unknown |
| Is there a **named accountability owner** for AI system decisions at the vendor? | Yes / No / Unknown |
| Does the vendor's **incident response plan** cover AI-specific failures (hallucinations, drift, adversarial inputs)? | Yes / No / Unknown |

---

## 7. NIST AI RMF — Map

| Question | Response |
|---|---|
| Is the AI tool's **use case clearly documented** (what it does, what it doesn't do)? | Yes / No |
| Has the vendor documented **clinical impact scenarios** (how AI output influences care decisions)? | Yes / No / Unknown |
| Has an **FDA SaMD (Software as a Medical Device) classification** been reviewed for this tool? | Yes / No / Not Applicable |
| If FDA-regulated: what is the **SaMD class / 510(k) status**? | |
| Has an **independent third-party audit** of the AI system been completed? | Yes / No / Unknown |

---

## 8. NIST AI RMF — Measure

| Question | Response |
|---|---|
| Has the vendor performed **bias and fairness testing** across patient demographics? | Yes / No / Unknown |
| Does the vendor publicly disclose **performance metrics** (sensitivity, specificity, error rates)? | Yes / No |
| Is **model drift monitoring** in place (ongoing performance tracking post-deployment)? | Yes / No / Unknown |

---

## 9. NIST AI RMF — Manage

| Question | Response |
|---|---|
| Does a **rollback / fallback plan** exist if the AI system fails or causes patient harm? | Yes / No |
| What is the vendor's **breach notification SLA** (how fast they notify you after a breach)? | ___ hours |
| What is the **last pentest date**? | MM/YYYY |

---

## 10. Clinic Deployment Status

| Question | Response |
|---|---|
| Is this tool **currently deployed** at the clinic? | Yes / No |
| **Date deployed**: | MM/DD/YYYY |
| Is this tool listed in the **clinic's AI inventory**? | Yes / No |
| Have **staff been trained** on this tool (documented)? | Yes / No |
| Who **approved** deployment of this tool? | |

---

## 11. Auditor Notes

> *(For auditor use — additional context, red flags, follow-up items)*

```
[Write notes here]
```

---

*AI Governance Checklist Auditor — © 2025 Noah Mills Healthcare Cybersecurity Consulting*
*Framework references: HIPAA Security Rule (45 CFR §164), NIST AI RMF (NIST AI 100-1), HHS OCR Guidance 2025*
