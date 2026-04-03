# AI Governance Policy
**[CLINIC NAME]**
**Effective Date:** [DATE] | **Review Cycle:** Annual (or upon deployment of new AI tool)
**Policy Owner:** [NAME, TITLE] | **Version:** 1.0

---

## 1. Purpose

This policy establishes a governance framework for all artificial intelligence (AI) tools deployed or under consideration at [CLINIC NAME]. It ensures that AI tools are evaluated, monitored, and managed in a manner consistent with:

- HIPAA Privacy Rule (45 CFR §164.500–164.534)
- HIPAA Security Rule (45 CFR §164.300–164.318)
- HIPAA Breach Notification Rule (45 CFR §164.400–164.414)
- NIST AI Risk Management Framework (NIST AI 100-1, 2023)
- HHS Office for Civil Rights AI Guidance (2025)
- [State] medical privacy laws

---

## 2. Scope

This policy applies to:

- All AI tools that access, process, transmit, or store Protected Health Information (PHI)
- All AI tools that influence clinical decisions, patient scheduling, billing, or communications
- All staff, contractors, and vendors who deploy or use AI tools on behalf of [CLINIC NAME]
- "Shadow AI" use: staff use of personal AI tools (e.g., consumer ChatGPT) on clinic business

---

## 3. Definitions

| Term | Definition |
|---|---|
| **AI Tool** | Any software system using machine learning, large language models, or automated decision-making that processes clinic data or influences clinical/administrative workflows |
| **PHI** | Protected Health Information as defined under HIPAA (45 CFR §160.103) |
| **BAA** | Business Associate Agreement — a HIPAA-required contract with vendors who handle PHI |
| **NIST AI RMF** | NIST AI Risk Management Framework — a voluntary governance framework for responsible AI use |
| **Shadow AI** | Use of AI tools not formally approved or inventoried by the clinic |
| **AI Inventory** | The clinic's documented registry of all AI tools in use or under evaluation |
| **SaMD** | Software as a Medical Device — AI tools that may require FDA review |

---

## 4. AI Governance Structure

### 4.1 AI Accountability Owner
[CLINIC NAME] designates **[NAME, TITLE]** as the AI Accountability Owner, responsible for:
- Maintaining the AI Inventory
- Reviewing new AI tool requests
- Coordinating annual re-audits
- Serving as the point of contact for vendor AI-related incidents

### 4.2 AI Review Committee
New AI tool deployments require sign-off from:
- [ ] AI Accountability Owner
- [ ] HIPAA Privacy Officer
- [ ] IT/Security Lead
- [ ] Clinical Lead (for tools affecting care delivery)

### 4.3 Escalation
Any concern about an AI tool's compliance, safety, or data handling is escalated to the AI Accountability Owner within **48 hours**. Patient safety concerns are escalated immediately.

---

## 5. AI Vendor Approval Process

No AI tool that handles PHI may be deployed without completing the following steps:

### Step 1 — Intake & Classification
Complete the **AI Vendor Intake Form** (see `templates/vendor_intake_form.md`) to document:
- Vendor identity and product category
- PHI exposure and data handling practices
- BAA status

### Step 2 — BAA Execution
If the tool accesses PHI, a **Business Associate Agreement must be executed before any PHI flows to the vendor.** The BAA must specify:
- Permitted uses and disclosures of PHI
- Encryption and security requirements
- Breach notification timeline (target: ≤72 hours)
- Data deletion upon contract termination
- Subprocessor obligations

### Step 3 — Risk Assessment
Complete the **AI Governance Checklist Audit** using the `run_audit.py` tool. Document the risk score and all findings.

### Step 4 — Approval or Conditional Approval
- **CRITICAL or HIGH risk score (≥45/100):** Requires written remediation plan before deployment
- **MEDIUM risk score (20–44/100):** May deploy with documented remediation timeline
- **LOW risk score (<20/100):** Approved; add to AI Inventory and schedule annual review

### Step 5 — AI Inventory Entry
All approved tools are added to the **[CLINIC NAME] AI Inventory** (maintained in [Notion / SharePoint / Google Sheet location]).

---

## 6. AI Inventory Requirements

The AI Inventory is maintained and reviewed **quarterly**. Each entry must include:

| Field | Description |
|---|---|
| Vendor & Product Name | Full product name and vendor |
| Category | (See Section 2 intake form categories) |
| BAA Status & Date | Signed / Pending / Not Required |
| Risk Score | From most recent audit |
| Last Audit Date | Date of most recent review |
| Next Review Date | Date of next scheduled review |
| AI Accountability Owner | Named individual |
| Deployment Date | When tool went live |
| PHI Access | Yes / No |
| Notes | Any pending remediation items |

---

## 7. Prohibited AI Use

The following uses of AI are **prohibited** at [CLINIC NAME]:

1. **Entering PHI into consumer AI tools** (ChatGPT free, Google Bard, consumer Claude, etc.) that have not executed a BAA and been formally approved
2. **Using AI to make unsupervised clinical decisions** without a clinician reviewing AI output before it affects patient care
3. **Deploying AI tools without completing Steps 1–5** of the vendor approval process
4. **Sharing patient data with AI vendors for model training** without documented patient consent and BAA coverage
5. **Using AI tools that have not received BAA-covered coverage** for PHI-related workflows

---

## 8. Staff Training Requirements

All staff using AI tools must:
- Complete **AI Tool Training** provided by the vendor or clinic IT before first use
- Complete **annual HIPAA refresher training** that includes AI data handling
- Review the **Prohibited AI Use** list (Section 7) during onboarding

Training completion must be documented in [HR system / training log].

---

## 9. Incident Response — AI-Specific

In addition to the clinic's existing HIPAA Breach Notification procedures, the following AI-specific incidents must be reported to the AI Accountability Owner within **24 hours**:

- PHI entered into an unapproved AI tool (shadow AI incident)
- AI tool producing outputs that may have led to a clinical error
- AI vendor notifying the clinic of a data breach or model change
- Model performance degradation affecting clinical workflows
- Suspected adversarial manipulation of an AI tool

For HIPAA-covered breaches, standard breach notification procedures apply (HHS notification within 60 days of discovery; affected individuals within 60 days).

---

## 10. Annual Re-Audit

All deployed AI tools are re-audited annually or upon:
- Major version updates by the vendor
- Changes to the tool's PHI access scope
- New regulatory guidance from HHS, FDA, or NIST
- Any AI-related security incident

Re-audits use the same **AI Vendor Intake Form** and **AI Governance Checklist Auditor** tool.

---

## 11. Policy Enforcement

Violation of this policy — including shadow AI use or deploying tools without BAA — may result in:
- Mandatory retraining
- Disciplinary action per clinic HR policy
- Reporting to HHS OCR in cases involving PHI exposure

---

## 12. Policy Review & Approval

| Role | Name | Signature | Date |
|---|---|---|---|
| AI Accountability Owner | | | |
| HIPAA Privacy Officer | | | |
| Practice Administrator / CEO | | | |

**Next Review Date:** _______________

---

## Appendix A — Framework References

- NIST AI Risk Management Framework: [https://airc.nist.gov/RMF](https://airc.nist.gov/RMF)
- HHS OCR HIPAA Resources: [https://www.hhs.gov/hipaa](https://www.hhs.gov/hipaa)
- FDA Digital Health Center of Excellence (SaMD guidance): [https://www.fda.gov/medical-devices/digital-health-center-excellence](https://www.fda.gov/medical-devices/digital-health-center-excellence)
- HIPAA Security Rule 45 CFR Part 164: [https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164)

---

## Appendix B — AI Inventory Template

| Vendor | Product | Category | BAA | Risk Score | Last Audit | Next Review | PHI | Owner |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

---

*Generated by AI Governance Checklist Auditor — github.com/itsnmills/ai-governance-auditor*
*© 2025 Noah Mills Healthcare Cybersecurity Consulting*
