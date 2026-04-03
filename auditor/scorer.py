"""
AI Governance Checklist Auditor — Risk Scoring Engine
Scores each vendor against HIPAA + NIST AI RMF requirements.
Returns a weighted risk score and a list of specific findings/flags.
"""

from .schema import VendorIntake, RiskLevel, BAAStatus


# ─── Scoring Weights ───────────────────────────────────────────────────────────
# Each finding is assigned a point penalty. Higher = more critical.
# Max possible penalty ~200 points → normalized to 0-100 risk score.

WEIGHTS = {
    # HIPAA / BAA — most critical
    "baa_not_signed_phi_touches": 40,
    "baa_unknown_phi_touches": 25,
    "baa_pending_phi_touches": 15,
    "data_leaves_us_unknown": 10,
    "data_leaves_us_confirmed": 20,
    "phi_no_encryption_rest": 25,
    "phi_no_encryption_transit": 20,
    "no_breach_notification_sla": 15,
    "breach_sla_too_long": 10,           # > 72 hours
    "no_subprocessors_documented": 10,

    # Model & Data Governance
    "trained_on_phi_unknown": 15,
    "trained_on_phi_without_consent": 25,
    "model_type_not_disclosed": 8,
    "no_human_oversight_clinical": 20,   # Clinical AI with no clinician-in-loop
    "no_data_deletion_policy": 10,
    "data_retention_over_365": 8,

    # Access Controls
    "no_mfa_sso": 12,
    "no_rbac": 10,
    "no_audit_logging": 18,

    # NIST AI RMF — Govern
    "no_ai_governance_policy": 12,
    "no_accountability_owner": 10,
    "no_ir_plan_ai": 12,

    # NIST AI RMF — Map
    "fda_device_unrecognized": 20,       # May be SaMD but not classified
    "no_clinical_impact_documented": 10,
    "no_third_party_audit": 8,

    # NIST AI RMF — Measure
    "no_bias_testing": 12,
    "no_performance_metrics": 10,
    "no_drift_monitoring": 8,

    # NIST AI RMF — Manage
    "no_rollback_plan": 10,
    "no_pentest_recent": 8,
    "no_soc2_hitrust": 8,

    # Inventory / Deployment
    "not_in_ai_inventory": 12,
    "staff_not_trained": 8,
}

MAX_RAW_SCORE = 200  # normalization ceiling


def score_vendor(intake: VendorIntake) -> tuple[int, RiskLevel, list[dict]]:
    """
    Score a VendorIntake record.

    Returns:
        (risk_score_0_100, risk_level, findings)
        findings: list of {"code": str, "severity": str, "message": str, "domain": str}
    """
    raw = 0
    findings = []

    def flag(code: str, severity: str, message: str, domain: str):
        raw_add = WEIGHTS.get(code, 0)
        findings.append({
            "code": code,
            "severity": severity,
            "message": message,
            "domain": domain,
            "weight": raw_add,
        })
        return raw_add

    # ── HIPAA / BAA ─────────────────────────────────────────────────────────
    if intake.phi_touches_product:
        if intake.baa_status == BAAStatus.NOT_SIGNED:
            raw += flag("baa_not_signed_phi_touches", "CRITICAL",
                "BAA is NOT signed. This tool touches PHI and is operating outside HIPAA requirements.",
                "HIPAA / BAA")
        elif intake.baa_status == BAAStatus.UNKNOWN:
            raw += flag("baa_unknown_phi_touches", "HIGH",
                "BAA status is UNKNOWN. Must be verified before continued use.",
                "HIPAA / BAA")
        elif intake.baa_status == BAAStatus.PENDING:
            raw += flag("baa_pending_phi_touches", "MEDIUM",
                "BAA is pending. PHI should not flow to this vendor until BAA is executed.",
                "HIPAA / BAA")

    if intake.data_leaves_us is True:
        raw += flag("data_leaves_us_confirmed", "HIGH",
            f"Patient data is transferred outside the US. Verify HIPAA-compliant data processing agreements and data residency controls.",
            "Data Handling")
    elif intake.data_leaves_us is None and intake.phi_touches_product:
        raw += flag("data_leaves_us_unknown", "MEDIUM",
            "Unknown whether data leaves the US. Vendor must provide documented data residency confirmation.",
            "Data Handling")

    if intake.data_encrypted_at_rest is False:
        raw += flag("phi_no_encryption_rest", "CRITICAL",
            "PHI is NOT encrypted at rest. This is a direct HIPAA Security Rule violation (§164.312(a)(2)(iv)).",
            "HIPAA / Security Rule")
    if intake.data_encrypted_in_transit is False:
        raw += flag("phi_no_encryption_transit", "CRITICAL",
            "PHI is NOT encrypted in transit. This is a direct HIPAA Security Rule violation (§164.312(e)(2)(ii)).",
            "HIPAA / Security Rule")

    if intake.phi_touches_product and intake.vendor_breach_notification_sla_hours is None:
        raw += flag("no_breach_notification_sla", "HIGH",
            "Vendor has no documented breach notification SLA. BAA must specify notification timelines (HHS recommends ≤72 hours).",
            "HIPAA / BAA")
    elif intake.vendor_breach_notification_sla_hours and intake.vendor_breach_notification_sla_hours > 72:
        raw += flag("breach_sla_too_long", "MEDIUM",
            f"Breach notification SLA is {intake.vendor_breach_notification_sla_hours}h. HHS 2025 guidance pushes for ≤72 hours; BAA should be updated.",
            "HIPAA / BAA")

    if intake.subprocessors_documented is False:
        raw += flag("no_subprocessors_documented", "MEDIUM",
            "Vendor has not documented their subprocessors. Fourth-party risk is unquantified.",
            "Vendor Risk")

    # ── Model & Training ─────────────────────────────────────────────────────
    if intake.model_training.value == "Training data practices unknown":
        raw += flag("trained_on_phi_unknown", "MEDIUM",
            "Model training data practices are unknown. Vendor must confirm whether clinic PHI is used for training or fine-tuning.",
            "AI Model Risk")
    elif intake.model_trained_on_clinic_data is True and \
         intake.model_training.value != "Trained on PHI with patient consent":
        raw += flag("trained_on_phi_without_consent", "CRITICAL",
            "Vendor appears to be training on clinic/patient data without documented patient consent. This may violate HIPAA minimum necessary and Privacy Rule requirements.",
            "AI Model Risk")

    if intake.model_type_disclosed is False:
        raw += flag("model_type_not_disclosed", "LOW",
            "Vendor does not disclose the underlying model powering the tool. Transparency is a core NIST AI RMF (Govern) requirement.",
            "NIST AI RMF — Govern")

    if intake.vendor_category.value in [
        "Diagnostic / Clinical Decision Support AI",
        "Ambient Scribe / Documentation AI",
    ] and intake.human_oversight_required is False:
        raw += flag("no_human_oversight_clinical", "HIGH",
            "Clinical AI tool has no documented clinician-in-the-loop requirement. NIST AI RMF requires human oversight for high-risk clinical decisions.",
            "NIST AI RMF — Manage")

    if not intake.data_deletion_policy:
        raw += flag("no_data_deletion_policy", "MEDIUM",
            "No data deletion/retention policy documented. Vendor must define how and when PHI is purged.",
            "Data Handling")

    if intake.data_retention_days and intake.data_retention_days > 365:
        raw += flag("data_retention_over_365", "LOW",
            f"Data retained for {intake.data_retention_days} days. Evaluate whether extended retention is necessary and documented.",
            "Data Handling")

    # ── Access Controls ──────────────────────────────────────────────────────
    if intake.sso_mfa_supported is False:
        raw += flag("no_mfa_sso", "HIGH",
            "Vendor does not support MFA or SSO. HIPAA §164.312(d) requires unique user authentication controls.",
            "HIPAA / Access Control")
    if intake.rbac_supported is False:
        raw += flag("no_rbac", "MEDIUM",
            "Role-based access control (RBAC) is not supported. Minimum necessary access cannot be enforced without RBAC.",
            "HIPAA / Access Control")
    if intake.audit_logging_available is False:
        raw += flag("no_audit_logging", "HIGH",
            "Vendor does not provide audit logging. HIPAA §164.312(b) requires activity logs for all systems handling ePHI.",
            "HIPAA / Security Rule")

    # ── NIST AI RMF — Govern ─────────────────────────────────────────────────
    if intake.ai_governance_policy_exists is False:
        raw += flag("no_ai_governance_policy", "MEDIUM",
            "Vendor has no published AI governance policy. NIST AI RMF GOVERN function requires documented accountability structures.",
            "NIST AI RMF — Govern")
    if intake.accountability_owner_named is False:
        raw += flag("no_accountability_owner", "MEDIUM",
            "No named accountability owner for AI decisions at the vendor. Required by NIST AI RMF GOVERN 1.1.",
            "NIST AI RMF — Govern")
    if intake.incident_response_plan_covers_ai is False:
        raw += flag("no_ir_plan_ai", "MEDIUM",
            "Vendor incident response plan does not cover AI-specific failures (hallucinations, model drift, adversarial inputs).",
            "NIST AI RMF — Govern")

    # ── NIST AI RMF — Map ────────────────────────────────────────────────────
    if intake.is_fda_regulated_device is None and intake.vendor_category.value == "Diagnostic / Clinical Decision Support AI":
        raw += flag("fda_device_unrecognized", "HIGH",
            "Diagnostic/clinical AI tool has unknown FDA SaMD classification status. Tools that replace clinician judgment may require FDA premarket review.",
            "NIST AI RMF — Map")
    if intake.clinical_impact_documented is False:
        raw += flag("no_clinical_impact_documented", "MEDIUM",
            "Vendor has not documented clinical impact scenarios. NIST AI RMF MAP requires harm scenario documentation.",
            "NIST AI RMF — Map")
    if intake.third_party_audit_completed is False:
        raw += flag("no_third_party_audit", "LOW",
            "No independent third-party audit of this AI system has been completed.",
            "NIST AI RMF — Map")

    # ── NIST AI RMF — Measure ────────────────────────────────────────────────
    if intake.bias_testing_performed is False:
        raw += flag("no_bias_testing", "MEDIUM",
            "Vendor has not performed or disclosed bias/fairness testing. Required for NIST AI RMF MEASURE and critical for clinical tools serving diverse patient populations.",
            "NIST AI RMF — Measure")
    if intake.performance_metrics_disclosed is False:
        raw += flag("no_performance_metrics", "MEDIUM",
            "Vendor does not disclose performance metrics (sensitivity, specificity, error rates). Clinicians cannot evaluate tool reliability without this data.",
            "NIST AI RMF — Measure")
    if intake.model_drift_monitoring is False:
        raw += flag("no_drift_monitoring", "LOW",
            "No model drift monitoring in place. Degraded AI performance over time is a patient safety risk.",
            "NIST AI RMF — Measure")

    # ── NIST AI RMF — Manage ─────────────────────────────────────────────────
    if intake.rollback_plan_exists is False:
        raw += flag("no_rollback_plan", "MEDIUM",
            "No rollback plan exists if the AI model fails or causes harm. NIST AI RMF MANAGE requires documented fallback procedures.",
            "NIST AI RMF — Manage")
    if intake.last_pentest_date is None and intake.phi_touches_product:
        raw += flag("no_pentest_recent", "MEDIUM",
            "No recent penetration test date documented. Annual pentesting is a HIPAA best practice for systems handling PHI.",
            "NIST AI RMF — Manage")
    if intake.soc2_or_hitrust_certified is False:
        raw += flag("no_soc2_hitrust", "LOW",
            "Vendor holds no SOC 2 or HITRUST certification. These are the standard third-party assurance frameworks for healthcare AI vendors.",
            "NIST AI RMF — Manage")

    # ── Clinic Inventory / Deployment ────────────────────────────────────────
    if intake.currently_deployed and intake.tool_in_ai_inventory is False:
        raw += flag("not_in_ai_inventory", "HIGH",
            "Tool is deployed but NOT in the clinic's AI inventory. 70% of health orgs lack a complete AI inventory — this is a governance gap.",
            "AI Governance")
    if intake.currently_deployed and intake.staff_trained_on_tool is False:
        raw += flag("staff_not_trained", "MEDIUM",
            "Staff using this tool have not received documented training. HIPAA requires workforce training on all systems handling PHI.",
            "HIPAA / Workforce")

    # ── Normalize Score ───────────────────────────────────────────────────────
    risk_score = min(100, round((raw / MAX_RAW_SCORE) * 100))

    if risk_score >= 70:
        level = RiskLevel.CRITICAL
    elif risk_score >= 45:
        level = RiskLevel.HIGH
    elif risk_score >= 20:
        level = RiskLevel.MEDIUM
    else:
        level = RiskLevel.LOW

    intake.flags = [f["code"] for f in findings]
    return risk_score, level, findings
