"""
AI Governance Checklist Auditor — Report Generator
Generates:
  1. Vendor Risk Card (Markdown)
  2. Full Audit Report (Markdown, multi-vendor)
"""

from datetime import datetime
from .schema import VendorIntake, RiskLevel
from .scorer import score_vendor


RISK_BADGE = {
    RiskLevel.CRITICAL: "🔴 CRITICAL",
    RiskLevel.HIGH:     "🟠 HIGH",
    RiskLevel.MEDIUM:   "🟡 MEDIUM",
    RiskLevel.LOW:      "🟢 LOW",
    RiskLevel.UNKNOWN:  "⚪ UNKNOWN",
}

SEVERITY_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}


def _bool_display(val):
    if val is True:
        return "✅ Yes"
    elif val is False:
        return "❌ No"
    return "⚠️ Unknown"


def generate_vendor_risk_card(intake: VendorIntake) -> str:
    """Generate a single-page Markdown vendor risk card."""
    score, level, findings = score_vendor(intake)
    findings_sorted = sorted(findings, key=lambda f: SEVERITY_ORDER.get(f["severity"], 9))

    badge = RISK_BADGE[level]
    audit_date = datetime.now().strftime("%B %d, %Y")

    lines = []
    lines.append(f"# Vendor Risk Card — {intake.vendor_name}")
    lines.append(f"> **Product:** {intake.product_name}  ")
    lines.append(f"> **Category:** {intake.vendor_category.value}  ")
    lines.append(f"> **Audit Date:** {audit_date}  ")
    lines.append(f"> **Auditor Notes:** {intake.auditor_notes or 'None'}  ")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(f"## Overall Risk Score: {score}/100 — {badge}")
    lines.append("")

    # ── Quick Status Table
    lines.append("## At-a-Glance Status")
    lines.append("")
    lines.append("| Control Area | Status |")
    lines.append("|---|---|")
    lines.append(f"| BAA Signed | {intake.baa_status.value} |")
    lines.append(f"| PHI Touches Product | {_bool_display(intake.phi_touches_product)} |")
    lines.append(f"| Data Stays in US | {_bool_display(not intake.data_leaves_us if intake.data_leaves_us is not None else None)} |")
    lines.append(f"| Encrypted at Rest | {_bool_display(intake.data_encrypted_at_rest)} |")
    lines.append(f"| Encrypted in Transit | {_bool_display(intake.data_encrypted_in_transit)} |")
    lines.append(f"| MFA / SSO Supported | {_bool_display(intake.sso_mfa_supported)} |")
    lines.append(f"| RBAC Supported | {_bool_display(intake.rbac_supported)} |")
    lines.append(f"| Audit Logging Available | {_bool_display(intake.audit_logging_available)} |")
    lines.append(f"| SOC 2 / HITRUST Certified | {_bool_display(intake.soc2_or_hitrust_certified)} |")
    lines.append(f"| Model Training on PHI Known | {_bool_display(intake.model_training.value != 'Training data practices unknown')} |")
    lines.append(f"| Bias Testing Performed | {_bool_display(intake.bias_testing_performed)} |")
    lines.append(f"| AI Governance Policy Exists | {_bool_display(intake.ai_governance_policy_exists)} |")
    lines.append(f"| In Clinic AI Inventory | {_bool_display(intake.tool_in_ai_inventory)} |")
    lines.append(f"| Staff Trained | {_bool_display(intake.staff_trained_on_tool)} |")
    lines.append("")

    # ── BAA Detail
    lines.append("## HIPAA BAA Details")
    lines.append("")
    if intake.baa_date_signed:
        lines.append(f"- **Date Signed:** {intake.baa_date_signed}")
    if intake.vendor_breach_notification_sla_hours:
        lines.append(f"- **Breach Notification SLA:** {intake.vendor_breach_notification_sla_hours} hours")
    if intake.phi_types_accessed:
        lines.append(f"- **PHI Types Accessed:** {', '.join(intake.phi_types_accessed)}")
    if intake.data_deletion_policy:
        lines.append(f"- **Data Deletion Policy:** {intake.data_deletion_policy}")
    if intake.data_retention_days:
        lines.append(f"- **Retention Period:** {intake.data_retention_days} days")
    lines.append("")

    # ── Findings
    lines.append("## Findings & Required Actions")
    lines.append("")
    if not findings:
        lines.append("✅ No significant findings. Continue monitoring on scheduled review cadence.")
    else:
        for f in findings_sorted:
            sev_icon = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"}.get(f["severity"], "⚪")
            lines.append(f"### {sev_icon} [{f['severity']}] {f['domain']}")
            lines.append(f"**Finding:** {f['message']}")
            lines.append(f"*Finding Code: `{f['code']}`*")
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Recommended Actions")
    lines.append("")

    # Prioritized action list
    critical_findings = [f for f in findings if f["severity"] == "CRITICAL"]
    high_findings = [f for f in findings if f["severity"] == "HIGH"]

    if critical_findings:
        lines.append("**Immediate (Before Next Use):**")
        for f in critical_findings:
            lines.append(f"- Resolve `{f['code']}`: {f['message'][:80]}...")
        lines.append("")

    if high_findings:
        lines.append("**Within 30 Days:**")
        for f in high_findings:
            lines.append(f"- Resolve `{f['code']}`: {f['message'][:80]}...")
        lines.append("")

    medium_findings = [f for f in findings if f["severity"] == "MEDIUM"]
    if medium_findings:
        lines.append("**Within 90 Days:**")
        for f in medium_findings:
            lines.append(f"- Resolve `{f['code']}`: {f['message'][:80]}...")
        lines.append("")

    lines.append("---")
    lines.append("*Generated by AI Governance Checklist Auditor — github.com/itsnmills/ai-governance-auditor*")
    lines.append("")

    return "\n".join(lines)


def generate_full_audit_report(
    practice_name: str,
    practice_size: str,
    auditor_name: str,
    vendors: list[VendorIntake],
) -> str:
    """Generate a full multi-vendor audit report for a clinic."""

    audit_date = datetime.now().strftime("%B %d, %Y")
    lines = []

    lines.append(f"# AI Vendor Governance Audit Report")
    lines.append(f"**Practice:** {practice_name}  ")
    lines.append(f"**Practice Size:** {practice_size}  ")
    lines.append(f"**Auditor:** {auditor_name}  ")
    lines.append(f"**Audit Date:** {audit_date}  ")
    lines.append(f"**Vendors Audited:** {len(vendors)}  ")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ── Executive Summary Table
    lines.append("## Executive Summary")
    lines.append("")
    lines.append("| Vendor | Product | Category | Score | Risk Level | BAA |")
    lines.append("|---|---|---|---|---|---|")

    all_scores = []
    all_findings_count = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    critical_vendors = []

    for v in vendors:
        score, level, findings = score_vendor(v)
        all_scores.append(score)
        badge = RISK_BADGE[level]
        for f in findings:
            if f["severity"] in all_findings_count:
                all_findings_count[f["severity"]] += 1
        if level in [RiskLevel.CRITICAL, RiskLevel.HIGH]:
            critical_vendors.append(v.vendor_name)
        lines.append(
            f"| {v.vendor_name} | {v.product_name} | {v.vendor_category.value} "
            f"| {score}/100 | {badge} | {v.baa_status.value} |"
        )

    lines.append("")

    avg_score = round(sum(all_scores) / len(all_scores)) if all_scores else 0
    lines.append(f"**Portfolio Risk Score:** {avg_score}/100")
    lines.append("")
    lines.append("**Finding Counts Across All Vendors:**")
    lines.append(f"- 🔴 Critical: {all_findings_count['CRITICAL']}")
    lines.append(f"- 🟠 High: {all_findings_count['HIGH']}")
    lines.append(f"- 🟡 Medium: {all_findings_count['MEDIUM']}")
    lines.append(f"- 🟢 Low: {all_findings_count['LOW']}")
    lines.append("")

    if critical_vendors:
        lines.append(f"> ⚠️ **Vendors requiring immediate attention:** {', '.join(critical_vendors)}")
        lines.append("")

    lines.append("---")
    lines.append("")

    # ── Per-Vendor Risk Cards (embedded)
    lines.append("## Individual Vendor Risk Cards")
    lines.append("")
    for v in vendors:
        card = generate_vendor_risk_card(v)
        lines.append(card)
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)
