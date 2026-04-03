"""
AI Governance Checklist Auditor — Schema & Data Models
Covers: HIPAA BAA status, data handling, NIST AI RMF (Govern/Map/Measure/Manage),
vendor categorization, and risk scoring.
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


# ─── Enums ────────────────────────────────────────────────────────────────────

class RiskLevel(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    UNKNOWN = "UNKNOWN"

class BAAStatus(str, Enum):
    SIGNED = "Signed"
    NOT_SIGNED = "Not Signed"
    NOT_REQUIRED = "Not Required"
    PENDING = "Pending Review"
    UNKNOWN = "Unknown"

class DataResidency(str, Enum):
    US_ONLY = "US Only"
    US_AND_INTERNATIONAL = "US + International"
    INTERNATIONAL_ONLY = "International Only"
    UNKNOWN = "Unknown"

class VendorCategory(str, Enum):
    AMBIENT_SCRIBE = "Ambient Scribe / Documentation AI"
    SCHEDULING = "Scheduling & Intake AI"
    DIAGNOSTIC = "Diagnostic / Clinical Decision Support AI"
    BILLING = "Billing & RCM Automation"
    EHR_INTEGRATED = "EHR-Integrated AI (Epic, Oracle, etc.)"
    PATIENT_ENGAGEMENT = "Patient Engagement / Chatbot"
    ADMINISTRATIVE = "Administrative Automation"
    GENERAL_LLM = "General-Purpose LLM (ChatGPT, Claude, etc.)"
    OTHER = "Other"

class ModelTraining(str, Enum):
    NOT_TRAINED_ON_PHI = "Not trained on clinic PHI"
    TRAINED_WITH_CONSENT = "Trained on PHI with patient consent"
    TRAINED_UNKNOWN = "Training data practices unknown"
    FINE_TUNED_ON_PHI = "Fine-tuned on clinic/patient data"


# ─── Core Intake Form ──────────────────────────────────────────────────────────

@dataclass
class VendorIntake:
    """Structured intake record for a single AI vendor/tool."""

    # ── Identity
    vendor_name: str = ""
    product_name: str = ""
    vendor_category: VendorCategory = VendorCategory.OTHER
    version_or_date: str = ""
    primary_contact: str = ""

    # ── HIPAA / BAA
    baa_status: BAAStatus = BAAStatus.UNKNOWN
    baa_date_signed: Optional[str] = None
    phi_touches_product: bool = True           # Does the tool see/handle PHI?
    phi_types_accessed: list = field(default_factory=list)   # e.g. ["demographics", "notes", "billing"]

    # ── Data Handling
    data_residency: DataResidency = DataResidency.UNKNOWN
    data_leaves_us: Optional[bool] = None
    data_encrypted_at_rest: Optional[bool] = None
    data_encrypted_in_transit: Optional[bool] = None
    data_retention_days: Optional[int] = None
    data_deletion_policy: str = ""
    subprocessors_documented: Optional[bool] = None

    # ── Model / Training
    model_training: ModelTraining = ModelTraining.TRAINED_UNKNOWN
    model_trained_on_clinic_data: Optional[bool] = None
    model_type_disclosed: Optional[bool] = None      # Does vendor disclose what model powers the tool?
    human_oversight_required: Optional[bool] = None  # Is there a clinician-in-the-loop?

    # ── Access & Auth
    sso_mfa_supported: Optional[bool] = None
    rbac_supported: Optional[bool] = None
    audit_logging_available: Optional[bool] = None

    # ── NIST AI RMF — Govern
    ai_governance_policy_exists: Optional[bool] = None        # Does vendor have a published AI governance policy?
    accountability_owner_named: Optional[bool] = None         # Named person responsible for AI decisions?
    incident_response_plan_covers_ai: Optional[bool] = None

    # ── NIST AI RMF — Map
    use_case_documented: Optional[bool] = None
    clinical_impact_documented: Optional[bool] = None         # Does tool influence clinical decisions?
    is_fda_regulated_device: Optional[bool] = None            # SaMD classification?
    third_party_audit_completed: Optional[bool] = None

    # ── NIST AI RMF — Measure
    bias_testing_performed: Optional[bool] = None
    performance_metrics_disclosed: Optional[bool] = None      # Sensitivity, specificity, error rates
    model_drift_monitoring: Optional[bool] = None

    # ── NIST AI RMF — Manage
    rollback_plan_exists: Optional[bool] = None
    vendor_breach_notification_sla_hours: Optional[int] = None  # e.g. 24, 48, 72
    last_pentest_date: Optional[str] = None
    soc2_or_hitrust_certified: Optional[bool] = None

    # ── Clinic Context
    currently_deployed: bool = False
    date_deployed: Optional[str] = None
    staff_trained_on_tool: Optional[bool] = None
    tool_in_ai_inventory: Optional[bool] = None               # Is this tool listed in clinic's AI inventory?

    # ── Auditor Notes
    auditor_notes: str = ""
    flags: list = field(default_factory=list)  # Auto-populated during scoring
