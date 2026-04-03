#!/usr/bin/env python3
"""
AI Governance Checklist Auditor — CLI Entry Point

Usage:
    python run_audit.py                          # Run demo audit (Sunrise Family Clinic)
    python run_audit.py --vendor path/to/vendor.json  # Audit a single vendor from JSON
    python run_audit.py --intake                 # Interactive intake wizard (stdin)
    python run_audit.py --output reports/        # Custom output directory
"""

import argparse
import json
import os
import sys
from datetime import datetime

from auditor import (
    VendorIntake, BAAStatus, DataResidency, VendorCategory, ModelTraining,
    generate_vendor_risk_card, generate_full_audit_report, score_vendor
)
from sample_vendors.demo_clinic import VENDORS, PRACTICE_NAME, PRACTICE_SIZE, AUDITOR_NAME


def vendor_from_json(path: str) -> VendorIntake:
    """Load a VendorIntake from a JSON file."""
    with open(path) as f:
        data = json.load(f)

    intake = VendorIntake()
    for key, val in data.items():
        if hasattr(intake, key):
            # Handle enum fields
            field_type = type(getattr(intake, key))
            if field_type in (BAAStatus, DataResidency, VendorCategory, ModelTraining):
                setattr(intake, key, field_type(val))
            else:
                setattr(intake, key, val)
    return intake


def interactive_intake() -> VendorIntake:
    """Basic stdin intake wizard for quick audits."""
    print("\n=== AI Governance Intake Wizard ===\n")
    intake = VendorIntake()

    intake.vendor_name = input("Vendor name: ").strip()
    intake.product_name = input("Product name: ").strip()

    print("\nCategories:")
    for i, cat in enumerate(VendorCategory):
        print(f"  {i+1}. {cat.value}")
    cat_idx = int(input("Select category number: ")) - 1
    intake.vendor_category = list(VendorCategory)[cat_idx]

    intake.phi_touches_product = input("Does the tool handle PHI? (y/n): ").lower() == "y"

    if intake.phi_touches_product:
        print("\nBAA Status options:")
        for i, status in enumerate(BAAStatus):
            print(f"  {i+1}. {status.value}")
        baa_idx = int(input("Select BAA status: ")) - 1
        intake.baa_status = list(BAAStatus)[baa_idx]

    intake.data_leaves_us = input("Does data leave the US? (y/n/unknown): ").lower()
    if intake.data_leaves_us == "y":
        intake.data_leaves_us = True
    elif intake.data_leaves_us == "n":
        intake.data_leaves_us = False
    else:
        intake.data_leaves_us = None

    intake.data_encrypted_at_rest = input("Encrypted at rest? (y/n/unknown): ").lower()
    intake.data_encrypted_at_rest = True if intake.data_encrypted_at_rest == "y" else \
        (False if intake.data_encrypted_at_rest == "n" else None)

    intake.soc2_or_hitrust_certified = input("SOC2 or HITRUST certified? (y/n/unknown): ").lower()
    intake.soc2_or_hitrust_certified = True if intake.soc2_or_hitrust_certified == "y" else \
        (False if intake.soc2_or_hitrust_certified == "n" else None)

    intake.currently_deployed = input("Currently deployed? (y/n): ").lower() == "y"
    intake.tool_in_ai_inventory = input("In your AI inventory? (y/n/unknown): ").lower()
    intake.tool_in_ai_inventory = True if intake.tool_in_ai_inventory == "y" else \
        (False if intake.tool_in_ai_inventory == "n" else None)

    intake.auditor_notes = input("Any notes: ").strip()
    return intake


def save_report(content: str, filename: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, filename)
    with open(path, "w") as f:
        f.write(content)
    print(f"  ✅ Saved: {path}")
    return path


def main():
    parser = argparse.ArgumentParser(description="AI Governance Checklist Auditor")
    parser.add_argument("--vendor", help="Path to a vendor JSON file for single-vendor audit")
    parser.add_argument("--intake", action="store_true", help="Run interactive intake wizard")
    parser.add_argument("--output", default="reports", help="Output directory (default: reports/)")
    parser.add_argument("--demo", action="store_true", default=False, help="Force demo mode")
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")

    print("\n" + "="*60)
    print("  AI Governance Checklist Auditor")
    print("  HIPAA + NIST AI RMF Vendor Risk Assessment")
    print("="*60 + "\n")

    if args.vendor:
        print(f"📋 Single-vendor audit: {args.vendor}")
        intake = vendor_from_json(args.vendor)
        score, level, findings = score_vendor(intake)
        print(f"\n  Vendor: {intake.vendor_name} — {intake.product_name}")
        print(f"  Risk Score: {score}/100 ({level.value})")
        print(f"  Findings: {len(findings)} total")
        card = generate_vendor_risk_card(intake)
        fname = f"{intake.vendor_name.replace(' ','_').lower()}_risk_card_{timestamp}.md"
        save_report(card, fname, args.output)

    elif args.intake:
        intake = interactive_intake()
        score, level, findings = score_vendor(intake)
        print(f"\n  Risk Score: {score}/100 ({level.value})")
        print(f"  Findings: {len(findings)} total\n")
        card = generate_vendor_risk_card(intake)
        fname = f"{intake.vendor_name.replace(' ','_').lower()}_risk_card_{timestamp}.md"
        save_report(card, fname, args.output)

    else:
        # Default: run demo audit
        print(f"🏥 Practice: {PRACTICE_NAME}")
        print(f"📋 Auditing {len(VENDORS)} vendors...\n")

        for v in VENDORS:
            score, level, findings = score_vendor(v)
            icon = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"}.get(level.value, "⚪")
            print(f"  {icon} {v.vendor_name} — {v.product_name}")
            print(f"     Score: {score}/100 | {level.value} | Findings: {len(findings)}")
            if any(f["severity"] == "CRITICAL" for f in findings):
                crits = [f["message"][:60] for f in findings if f["severity"] == "CRITICAL"]
                for c in crits:
                    print(f"     🔴 CRITICAL: {c}...")

        # Generate individual risk cards
        print("\n📄 Generating vendor risk cards...")
        for v in VENDORS:
            card = generate_vendor_risk_card(v)
            safe_name = v.vendor_name.replace(' ','_').replace('/','_').lower()
            fname = f"{safe_name}_risk_card.md"
            save_report(card, fname, args.output)

        # Generate full audit report
        print("\n📊 Generating full audit report...")
        full_report = generate_full_audit_report(
            practice_name=PRACTICE_NAME,
            practice_size=PRACTICE_SIZE,
            auditor_name=AUDITOR_NAME,
            vendors=VENDORS,
        )
        report_path = save_report(
            full_report,
            f"full_audit_report_{timestamp}.md",
            args.output
        )

        # Summary
        scores = [score_vendor(v)[0] for v in VENDORS]
        avg = round(sum(scores) / len(scores))
        print(f"\n{'='*60}")
        print(f"  Audit Complete")
        print(f"  Portfolio Avg Risk Score: {avg}/100")
        print(f"  Reports saved to: {os.path.abspath(args.output)}/")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
