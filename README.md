# AI Governance Checklist Auditor

**HIPAA + NIST AI RMF Vendor Risk Assessment for Healthcare Clinics**

> A structured intake and audit workflow that evaluates every AI tool a clinic is using — ambient scribes, scheduling AI, diagnostic AI, billing automation, EHR-integrated AI — against HIPAA requirements, BAA status, data handling practices, and the NIST AI Risk Management Framework (AI 100-1). Outputs a vendor risk card for each tool and a governance policy template.

---

## Why This Exists

**70% of healthcare organizations have AI governance committees. Only 30% maintain an actual AI inventory.**

Epic and Oracle are pushing AI features directly into EHRs in 2025. Startups are selling ambient scribes, scheduling bots, and diagnostic AI to clinic owners who have no framework for evaluating whether:

- A Business Associate Agreement (BAA) is signed
- Patient data is being used to train the vendor's model
- Data is leaving the United States
- Staff have been trained on the tool
- The AI tool appears anywhere in a formal inventory

This tool gives small-to-medium clinics a repeatable audit workflow to answer all of those questions systematically.

---

## What It Does

```
python run_audit.py
```

```
============================================================
  AI Governance Checklist Auditor
  HIPAA + NIST AI RMF Vendor Risk Assessment
============================================================

🏥 Practice: Sunrise Family Clinic
📋 Auditing 5 vendors...

  🟢 Nuance / Microsoft — DAX Copilot
     Score: 0/100 | LOW | Findings: 0
  🔴 ClearPath AI — SmartSchedule Pro
     Score: 100/100 | CRITICAL | Findings: 20
  🔴 OpenAI — ChatGPT (Consumer)
     Score: 100/100 | CRITICAL | Findings: 19
     🔴 CRITICAL: BAA is NOT signed. This tool touches PHI...
     🔴 CRITICAL: Vendor appears to be training on clinic/patient data...
  🟡 Waystar — AI Claims Assistant
     Score: 30/100 | MEDIUM | Findings: 6
  🟡 Epic Systems — Epic AI (Sepsis Predictor + In-Basket AI)
     Score: 20/100 | MEDIUM | Findings: 4

  Portfolio Avg Risk Score: 50/100
```

For each vendor it generates:
- A **Vendor Risk Card** with at-a-glance status table, findings sorted by severity, and a prioritized remediation checklist
- A **Full Audit Report** combining all vendor risk cards with an executive summary table

---

## Audit Framework

The scoring engine maps findings to three frameworks simultaneously:

| Domain | Source |
|---|---|
| BAA status, PHI handling, encryption, audit logging, breach notification | HIPAA Security Rule (45 CFR §164) |
| AI training data, model transparency, human oversight, data residency | HIPAA Privacy Rule + HHS OCR 2025 AI Guidance |
| AI governance policies, accountability structures | NIST AI RMF — **GOVERN** |
| Use case documentation, FDA SaMD classification, harm scenarios | NIST AI RMF — **MAP** |
| Bias testing, performance metrics disclosure, drift monitoring | NIST AI RMF — **MEASURE** |
| Rollback plans, incident response, penetration testing, SOC2/HITRUST | NIST AI RMF — **MANAGE** |

### Risk Score

Each finding carries a weighted penalty (0–40 points depending on severity). The raw penalty total is normalized to a 0–100 scale:

| Score Range | Risk Level |
|---|---|
| 70–100 | 🔴 CRITICAL |
| 45–69 | 🟠 HIGH |
| 20–44 | 🟡 MEDIUM |
| 0–19 | 🟢 LOW |

---

## Repository Structure

```
ai-governance-auditor/
├── auditor/
│   ├── schema.py              # VendorIntake dataclass + all enums
│   ├── scorer.py              # Weighted risk scoring engine (30 finding types)
│   ├── report_generator.py    # Vendor risk card + full audit report generator
│   └── __init__.py
├── sample_vendors/
│   └── demo_clinic.py         # 5 real-world vendor profiles (DAX, ChatGPT, Epic, etc.)
├── templates/
│   ├── vendor_intake_form.md          # Clinic-facing intake worksheet
│   ├── vendor_intake_template.json    # Machine-readable intake for CLI
│   └── ai_governance_policy_template.md  # Full governance policy template
├── reports/                   # Auto-generated output (gitignored for real audits)
│   └── [vendor]_risk_card.md
│   └── full_audit_report_[timestamp].md
├── run_audit.py               # CLI entry point
├── requirements.txt
└── README.md
```

---

## Getting Started

### Install

```bash
git clone https://github.com/itsnmills/ai-governance-auditor
cd ai-governance-auditor
pip install -r requirements.txt
```

### Run the Demo Audit (5 sample vendors)

```bash
python run_audit.py
```

Reports are saved to `reports/`.

### Audit a Single Vendor via JSON

Copy and fill out `templates/vendor_intake_template.json`, then:

```bash
python run_audit.py --vendor templates/vendor_intake_template.json
```

### Interactive Intake Wizard

```bash
python run_audit.py --intake
```

Walks you through the key fields via stdin and generates a risk card.

### Custom Output Directory

```bash
python run_audit.py --output /path/to/output/
```

---

## Intake Form

The **`templates/vendor_intake_form.md`** is designed to be handed to clinic staff or used as a questionnaire when onboarding a new AI vendor. It covers:

1. Vendor Identity & Category
2. HIPAA & BAA Status
3. Data Handling (residency, encryption, retention, deletion)
4. AI Model & Training Data Practices
5. Access Controls & Security Certifications
6. NIST AI RMF — Govern
7. NIST AI RMF — Map
8. NIST AI RMF — Measure
9. NIST AI RMF — Manage
10. Clinic Deployment Status

---

## Governance Policy Template

**`templates/ai_governance_policy_template.md`** is a fill-in-the-blank HIPAA + NIST AI RMF aligned governance policy for clinics that have no existing AI governance infrastructure. It covers:

- AI Accountability Owner designation
- AI Review Committee structure
- Vendor approval process (5-step)
- AI Inventory requirements
- Prohibited AI uses (shadow AI section)
- Staff training requirements
- AI-specific incident response procedures
- Annual re-audit cadence

---

## Sample Vendor Profiles

The demo audit (`sample_vendors/demo_clinic.py`) includes five representative vendor scenarios:

| Vendor | Scenario | Risk |
|---|---|---|
| Nuance DAX Copilot | Well-governed ambient scribe. BAA signed, SOC2 + HITRUST, no PHI training. | 🟢 LOW |
| ClearPath AI SmartSchedule | BAA pending, data leaves US, no AI governance policy, no pentest. | 🔴 CRITICAL |
| ChatGPT (Consumer) | Shadow AI. Staff pasting patient notes. No BAA. PHI potentially used for training. | 🔴 CRITICAL |
| Waystar AI Claims | Good baseline, BAA signed. Gaps in AI-specific IR plan and bias testing documentation. | 🟡 MEDIUM |
| Epic AI (Sepsis Predictor) | Vendor-level governance is strong. Clinic hasn't added new AI features to inventory or re-trained staff. | 🟡 MEDIUM |

---

## Commercial Use Cases

This tool was designed with three buyer tiers in mind:

| Buyer | Engagement Model | Value |
|---|---|---|
| Small clinic (1–5 providers) | One-time AI vendor audit — consulting deliverable ($250) | Know if BAA is signed, if data leaves US, if staff are trained |
| Medium practice (10–50 providers) | Quarterly re-audit as AI tools update ($150/quarter) | Ongoing inventory + governance cadence |
| MSP / larger org | White-label the intake form + report template | Resell to client clinics; demonstrate AI governance capability |

---

## Regulatory References

- [HIPAA Security Rule — 45 CFR Part 164](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164)
- [NIST AI Risk Management Framework (AI 100-1)](https://airc.nist.gov/RMF)
- [HHS OCR HIPAA Guidance on AI (2025)](https://www.hhs.gov/hipaa/index.html)
- [FDA Digital Health Center of Excellence — SaMD Guidance](https://www.fda.gov/medical-devices/digital-health-center-excellence)
- [Censinet: AI Vendor Compliance Checklist for Healthcare](https://censinet.com/perspectives/ai-vendor-compliance-checklist-healthcare)
- [NIST AI RMF + CSF in Healthcare — Censinet](https://censinet.com/perspectives/nist-cybersecurity-framework-ai-risk-healthcare)

---

## Skills Demonstrated

This project demonstrates practical knowledge of:

- **HIPAA Security Rule** — BAA requirements, encryption standards, audit logging, breach notification
- **NIST AI Risk Management Framework** — all four functions (Govern, Map, Measure, Manage) applied to clinical AI
- **Vendor Risk Management** — structured third-party assessment methodology
- **AI Governance** — inventory management, shadow AI risk, clinical oversight requirements
- **Python** — dataclasses, enums, weighted scoring, Markdown report generation
- **Healthcare AI Risk** — FDA SaMD classification, model training on PHI, bias and fairness requirements

---

## Author

**Noah Mills** — Healthcare Cybersecurity Consulting
- GitHub: [@itsnmills](https://github.com/itsnmills)
- Portfolio: [Strands PHI Guardrails Demo](https://github.com/itsnmills/Strands-PHI-Guardrails-Demo)

---

*This tool is for educational and consulting purposes. It does not constitute legal advice. All regulatory guidance should be verified with a qualified HIPAA attorney or compliance officer.*


---

## System Requirements

| Requirement | Details |
|---|---|
| **Python** | 3.10 or higher ([python.org](https://www.python.org/downloads/)) |
| **Operating System** | Windows, macOS, or Linux |
| **Disk Space** | < 5 MB |
| **RAM** | 128 MB minimum |
| **Network** | Not required — runs entirely offline |
| **External dependencies** | **None** — this tool uses only Python standard library modules (`dataclasses`, `typing`, `enum`, `datetime`, `argparse`, `json`, `os`) |

### Installation

```bash
git clone https://github.com/itsnmills/ai-governance-auditor.git
cd ai-governance-auditor
# No external dependencies — Python stdlib only
```

### Dependencies

**This tool has zero external dependencies.** It uses only Python standard library modules:

| Module | What It Does |
|---|---|
| `dataclasses` | Defines the VendorIntake data model (40+ fields) |
| `typing` / `enum` | Type annotations and enumeration types |
| `datetime` | Timestamps for audit reports |
| `argparse` | CLI argument parsing |
| `json` | Reading/writing vendor intake data |
| `os` | File system operations for report output |

No `pip install` required. If you have Python 3.10+, you can run this tool immediately.

---

## What This Tool Accesses On Your System

This tool runs 100% locally on your machine. Here is exactly what it reads, writes, and accesses:

| What | Access Type | Details |
|---|---|---|
| **Local filesystem** | Read/Write | Reads vendor intake JSON files from `sample_vendors/` (or your own intake data). Writes risk cards and audit reports as Markdown files to `reports/`. |
| **No external APIs** | None | This tool makes zero outbound network requests. No vendor names, audit findings, or risk scores are sent anywhere. |
| **No telemetry** | None | No analytics, tracking, crash reporting, or phone-home behavior of any kind. |
| **No database** | None | No database of any kind — all data is in flat files you can read and inspect. |

**Demo mode:** The tool includes 5 realistic but entirely fictional AI vendor profiles (DAX Copilot, ChatGPT Consumer, ClearPath SmartSchedule, Waystar, Epic AI). These demonstrate the scoring engine across the full risk spectrum. No real vendor or clinic data is involved.

---

## Privacy & Open Source Transparency

**This is open-source software. You download it, you run it, you own it.**

| Concern | Answer |
|---|---|
| **Can the developer see my data?** | No. This tool runs entirely on your machine. The developer (or anyone else) has zero access to your data, your results, or your system. |
| **Does it phone home?** | No. There are no analytics, telemetry, crash reporting, update checks, or network calls of any kind. |
| **Is my data stored in the cloud?** | No. All data stays on your local machine in files you can inspect, move, back up, or delete at any time. |
| **Can I audit the code?** | Yes. Every line of source code is available in this repository. The MIT license gives you the right to use, modify, and distribute it. |
| **Is it safe to use with real organizational data?** | Yes — but as with any tool, follow your organization's data handling policies. Since everything runs locally, your data never leaves your control. |

> **If you're evaluating this tool for your organization:** Download it, review the source code, run the demo mode first, and verify for yourself that it meets your security requirements. That's the entire point of open source.

## Keeping Threat Intelligence & Regulatory Data Current

The 30 finding types are mapped to:
- **HIPAA Security Rule** (45 CFR §164 — specific section references per finding)
- **HIPAA Privacy Rule** + **HHS OCR 2025 AI Guidance**
- **NIST AI Risk Management Framework (AI 100-1)** — GOVERN, MAP, MEASURE, MANAGE functions
- **FDA SaMD classification** guidance

When regulations or AI governance frameworks are updated, the scoring engine and finding definitions will be updated accordingly:

```bash
git pull origin main
```

---

## Security

If you discover a security vulnerability in this tool, please report it responsibly by opening a GitHub issue or contacting the maintainer directly. Do not submit PHI or real patient data in bug reports.
