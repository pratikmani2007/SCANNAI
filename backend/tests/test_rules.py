"""
Comprehensive Unit Tests for Communication Intelligence, Procedural Rule Engine & Scoring Math.
Phase 3.1 Refinements:
- Verifies refined rules: PROC-IND-001 to PROC-IND-006
- Verifies 4 new edge cases: Legitimate e-Courts notice, Bank debit alert, Hinglish digital arrest, Obfuscated keywords
- Verifies scoring boundaries (34, 35, 69, 70), 85 critical rule floor, and 100 maximum score cap
- Verifies ordinary commercial UPI and business escrow are not falsely flagged
- Verifies deduplication and offline execution (zero network calls)

Product: SCANNAI | Team: ROCKERZ
"""

import socket
import pytest
from app.services.procedural_rules import (
    evaluate_procedural_fallacies,
    PROCEDURAL_RULES_REGISTRY,
)
from app.services.text_analyzer import (
    extract_threat_indicators,
    analyze_text_communication,
    synthesize_risk_score,
)
from app.models.schemas import (
    RiskClassification,
    ConfidenceLevel,
    IndicatorSeverity,
    ProceduralViolation,
    SuspiciousIndicator,
)


# ==============================================================================
# 1. CORE PROCEDURAL FALLACY UNIT TESTS
# ==============================================================================

def test_digital_arrest_statutory_fallacy():
    text = (
        "This is DCP Rajesh Sharma from Crime Branch. You are under digital arrest. "
        "Do not disconnect the video call. You must remain on video call until investigation is complete."
    )
    violations = evaluate_procedural_fallacies(text)
    codes = [v.code for v in violations]
    assert "PROC-IND-001" in codes
    assert any("BNSS" in v.official_norm for v in violations)


def test_verification_escrow_fallacy():
    text = "Transfer Rs 1,00,000 to RBI verification account to clear your name and unfreeze your bank account."
    violations = evaluate_procedural_fallacies(text)
    codes = [v.code for v in violations]
    assert "PROC-IND-002" in codes
    assert any("RBI" in v.official_norm for v in violations)


def test_generic_business_escrow_does_not_trigger_fallacy():
    """Generic business or software escrow must NOT trigger PROC-IND-002."""
    text = "We have deposited the milestone payment of USD 5,000 into the commercial escrow account as per contract clause 12."
    violations = evaluate_procedural_fallacies(text)
    codes = [v.code for v in violations]
    assert "PROC-IND-002" not in codes


def test_personal_upi_official_payment_fallacy():
    text = "Pay court bail and penalty via upi to police.clearance@okhdfcbank immediately."
    violations = evaluate_procedural_fallacies(text)
    codes = [v.code for v in violations]
    assert "PROC-IND-003" in codes


def test_ordinary_commercial_upi_does_not_trigger_fallacy():
    """Ordinary commercial UPI transactions must NOT trigger PROC-IND-003."""
    text = "Hey Priya, please transfer Rs 750 for dinner to rahul.sharma@okhdfcbank or via Google Pay."
    violations = evaluate_procedural_fallacies(text)
    codes = [v.code for v in violations]
    assert "PROC-IND-003" not in codes


def test_secrecy_prohibition_on_counsel_fallacy():
    text = "This is a secret investigation. Do not tell anyone, do not tell family or lawyer. Sit in an isolated room."
    violations = evaluate_procedural_fallacies(text)
    codes = [v.code for v in violations]
    assert "PROC-IND-004" in codes
    assert any("Article 22(1)" in v.official_norm for v in violations)
    assert any("Section 38 of the BNSS" in v.official_norm for v in violations)


def test_telecom_disconnection_threat_fallacy():
    text = "TRAI notice: Your SIM card will be disconnected in 2 hours due to illegal messaging."
    violations = evaluate_procedural_fallacies(text)
    codes = [v.code for v in violations]
    assert "PROC-IND-005" in codes


def test_courier_narcotics_extortion_fallacy():
    text = "FedEx package intercepted by customs contains narcotics and contraband. Transfer customs clearance fee immediately."
    violations = evaluate_procedural_fallacies(text)
    codes = [v.code for v in violations]
    assert "PROC-IND-006" in codes
    assert any("CBIC" in v.official_norm or "DIN" in v.official_norm for v in violations)


def test_threat_vector_extraction_impersonation_and_urgency():
    text = "CBI officer calling. Non-bailable warrant issued. Transfer funds to avoid arrest within 15 minutes."
    indicators = extract_threat_indicators(text)
    categories = [ind.category for ind in indicators]
    assert "Institutional & Law Enforcement Impersonation" in categories
    assert "Manufactured Urgency & Coercive Deadline" in categories


# ==============================================================================
# 2. FOUR MANDATORY EDGE-CASE TESTS (PHASE 3.1)
# ==============================================================================

def test_edge_case_a_legitimate_ecourts_notice():
    """
    Edge Case A: A legitimate e-Courts virtual hearing notice under BNSS Section 530
    must NOT trigger PROC-IND-001 and must be classified as LOW RISK.
    """
    legit_court_notice = (
        "e-Courts Services Notice: Case CNR-DLHC01-004521-2025 (Civil Appeal) is listed before "
        "Bench 4, Delhi High Court on 15-Nov-2025 at 10:30 AM. "
        "Join video conference proceedings via official Cisco Webex link: "
        "https://delhihighcourt.webex.com/meet/court4 as per Section 530 BNSS. "
        "Please adhere to standard court decorum."
    )
    violations = evaluate_procedural_fallacies(legit_court_notice)
    assert len(violations) == 0, "Legitimate e-Courts notice must not trigger any procedural fallacy"

    risk_class, score, confidence, summary, v, ind, lim, actions = analyze_text_communication(legit_court_notice)
    assert risk_class == RiskClassification.LOW_RISK
    assert score <= 34


def test_edge_case_b_legitimate_bank_notification():
    """
    Edge Case B: A standard bank debit notification with a fraud helpline
    must be classified as LOW RISK and zero procedural violations.
    """
    bank_sms = (
        "HDFC Bank Alert: Rs 4,200.00 debited from A/C **8765 on 07-Nov-26 at 14:22:10 via UPI. "
        "Info: Swiggy Order. If not done by you, immediately call 1800-202-6161 or SMS BLOCK to 5676712. "
        "Never share OTP or PIN."
    )
    violations = evaluate_procedural_fallacies(bank_sms)
    assert len(violations) == 0

    risk_class, score, confidence, summary, v, ind, lim, actions = analyze_text_communication(bank_sms)
    assert risk_class == RiskClassification.LOW_RISK
    assert score <= 34


def test_edge_case_c_hinglish_digital_arrest_scam():
    """
    Edge Case C: Scammers using Hinglish phrasing ('digital giraftari', 'thana', 'video call par giraftari').
    Must be detected as HIGH RISK with score >= 85.
    """
    hinglish_text = (
        "Crime branch police thane se ACP Vikram bol raha hoon. "
        "Aapke naam par digital giraftari warrant issue hua hai money laundering case me. "
        "Video call par giraftari me raho aur turant 200000 rupees rbi verification account me transfer karo."
    )
    violations = evaluate_procedural_fallacies(hinglish_text)
    codes = [v.code for v in violations]
    assert "PROC-IND-001" in codes or "PROC-IND-002" in codes

    risk_class, score, confidence, summary, v, ind, lim, actions = analyze_text_communication(hinglish_text)
    assert risk_class == RiskClassification.HIGH_RISK
    assert score >= 85


def test_edge_case_d_spaced_and_obfuscated_scam_keywords():
    """
    Edge Case D: Scammers attempting evasion with spaces/delimiters ('d-i-g-i-t-a-l   a-r-r-e-s-t', 'r_b_i v_e_r_i_f_i_c_a_t_i_o_n').
    Must be detected as HIGH RISK with score >= 85.
    """
    obfuscated_text = (
        "Attention: You are placed under d-i-g-i-t-a-l   a-r-r-e-s-t by CBI. "
        "Transfer Rs 150000 to r_b_i  v_e_r_i_f_i_c_a_t_i_o_n account within 15 minutes to clear your name."
    )
    violations = evaluate_procedural_fallacies(obfuscated_text)
    codes = [v.code for v in violations]
    assert "PROC-IND-001" in codes or "PROC-IND-002" in codes

    risk_class, score, confidence, summary, v, ind, lim, actions = analyze_text_communication(obfuscated_text)
    assert risk_class == RiskClassification.HIGH_RISK
    assert score >= 85


# ==============================================================================
# 3. SCORING BOUNDARIES, FLOORS & CEILINGS
# ==============================================================================

def test_critical_rule_score_floor_enforcement():
    """Any critical statutory rule (PROC-IND-001, 002, 004) must enforce score >= 85."""
    critical_violation = [
        ProceduralViolation(
            code="PROC-IND-001",
            official_norm="BNSS Section 530 / Chapter V",
            observed_violation="Digital arrest threat",
            jurisdiction="IN",
        )
    ]
    # Even with zero indicators, critical rule enforces >= 85
    classification, score, conf, summary, actions = synthesize_risk_score(critical_violation, [], 100)
    assert classification == RiskClassification.HIGH_RISK
    assert score >= 85


def test_score_never_exceeds_100():
    """Even with stacked critical violations and indicators, score must cap strictly at 100."""
    critical_violations = [
        ProceduralViolation(code="PROC-IND-001", official_norm="norm", observed_violation="v1", jurisdiction="IN"),
        ProceduralViolation(code="PROC-IND-002", official_norm="norm", observed_violation="v2", jurisdiction="IN"),
        ProceduralViolation(code="PROC-IND-004", official_norm="norm", observed_violation="v4", jurisdiction="IN"),
    ]
    many_indicators = [
        SuspiciousIndicator(category="Cat1", severity=IndicatorSeverity.CRITICAL, title="T1", description="D1"),
        SuspiciousIndicator(category="Cat2", severity=IndicatorSeverity.CRITICAL, title="T2", description="D2"),
        SuspiciousIndicator(category="Cat3", severity=IndicatorSeverity.HIGH, title="T3", description="D3"),
        SuspiciousIndicator(category="Cat4", severity=IndicatorSeverity.HIGH, title="T4", description="D4"),
        SuspiciousIndicator(category="Cat5", severity=IndicatorSeverity.HIGH, title="T5", description="D5"),
    ]
    classification, score, conf, summary, actions = synthesize_risk_score(critical_violations, many_indicators, 500)
    assert score == 100
    assert classification == RiskClassification.HIGH_RISK


def test_risk_score_boundary_34_low_risk():
    """Score <= 34 must be classified as LOW RISK."""
    # Single low/minor indicator gives score 25
    minor_indicator = [
        SuspiciousIndicator(category="Misc", severity=IndicatorSeverity.LOW, title="Title", description="Desc")
    ]
    classification, score, conf, summary, actions = synthesize_risk_score([], minor_indicator, 100)
    assert score == 25
    assert score <= 34
    assert classification == RiskClassification.LOW_RISK


def test_risk_score_boundary_35_needs_verification():
    """Score 35 must be classified as NEEDS VERIFICATION."""
    # Single high indicator gives score 35
    single_high = [
        SuspiciousIndicator(category="Auth", severity=IndicatorSeverity.HIGH, title="Title", description="Desc")
    ]
    classification, score, conf, summary, actions = synthesize_risk_score([], single_high, 100)
    assert score == 35
    assert classification == RiskClassification.NEEDS_VERIFICATION


def test_risk_score_boundary_69_needs_verification():
    """Scores up to 69 must remain in NEEDS VERIFICATION."""
    # 2 high indicators give score 64 (50 + 2*7 = 64)
    two_high = [
        SuspiciousIndicator(category="Auth", severity=IndicatorSeverity.HIGH, title="Title1", description="Desc1"),
        SuspiciousIndicator(category="Secrecy", severity=IndicatorSeverity.HIGH, title="Title2", description="Desc2"),
    ]
    classification, score, conf, summary, actions = synthesize_risk_score([], two_high, 100)
    assert 35 <= score <= 69
    assert classification == RiskClassification.NEEDS_VERIFICATION


def test_risk_score_boundary_70_high_risk():
    """Non-critical procedural violation (e.g. PROC-IND-003 or 005) starts at 70 (HIGH RISK)."""
    non_critical_v = [
        ProceduralViolation(code="PROC-IND-003", official_norm="norm", observed_violation="UPI fine", jurisdiction="IN")
    ]
    classification, score, conf, summary, actions = synthesize_risk_score(non_critical_v, [], 100)
    assert score >= 70
    assert classification == RiskClassification.HIGH_RISK


def test_duplicate_evidence_does_not_inflate_score():
    """Repeating the same keyword multiple times in text must not duplicate indicators."""
    repeated_text = "CBI officer calling. CBI officer calling. CBI officer calling. CBI officer calling."
    indicators = extract_threat_indicators(repeated_text)
    # Deduplication ensures only 1 indicator for Institutional Impersonation is returned
    assert len(indicators) == 1


# ==============================================================================
# 4. OFFLINE & ZERO-NETWORK PIPELINE VERIFICATION
# ==============================================================================

def test_pipeline_is_completely_offline(monkeypatch):
    """
    Verifies that analyze_text_communication executes 100% locally
    without attempting any network or socket operations.
    """
    def fail_on_socket_connect(*args, **kwargs):
        raise RuntimeError("Unexpected network socket connection attempted during local analysis!")

    monkeypatch.setattr(socket.socket, "connect", fail_on_socket_connect)

    sample_scam = "DCP Crime Branch. You are under digital arrest. Pay bail fine to officer@okhdfcbank."
    # Must complete cleanly without invoking socket.connect
    risk_class, score, conf, summary, violations, indicators, lim, actions = analyze_text_communication(sample_scam)
    assert risk_class == RiskClassification.HIGH_RISK
    assert score >= 85


# ==============================================================================
# 5. PHASE 3.2 SPECIFIC VERIFICATION TESTS
# ==============================================================================

def test_educational_discussion_of_digital_arrest():
    """Educational or awareness discussions must not trigger PROC-IND-001 or high risk."""
    edu_text = (
        "Join us for an online awareness seminar on digital arrest and cyber security best practices "
        "organized by the University Cyber Cell this Saturday."
    )
    violations = evaluate_procedural_fallacies(edu_text)
    assert len(violations) == 0, "Educational awareness text must not trigger PROC-IND-001"

    risk_class, score, conf, summary, v, ind, lim, actions = analyze_text_communication(edu_text)
    assert risk_class == RiskClassification.LOW_RISK
    assert score <= 34


def test_legitimate_tsp_billing_notice():
    """Legitimate telecom billing notification must not trigger PROC-IND-005."""
    tsp_bill = (
        "Dear Airtel customer, your bill of Rs 799 for mobile number 9876543210 is due on 15-Nov-2026. "
        "Please pay via Airtel Thanks App to continue enjoying uninterrupted plan benefits."
    )
    violations = evaluate_procedural_fallacies(tsp_bill)
    assert len(violations) == 0

    risk_class, score, conf, summary, v, ind, lim, actions = analyze_text_communication(tsp_bill)
    assert risk_class == RiskClassification.LOW_RISK
    assert score <= 34


def test_ncb_news_without_extortion_is_safe():
    """Mention of Narcotics Control Bureau in news/discussion without extortion must remain safe."""
    news_text = (
        "The Narcotics Control Bureau organized an international conference on synthetic drug "
        "interception and forensic profiling yesterday."
    )
    violations = evaluate_procedural_fallacies(news_text)
    assert len(violations) == 0

    risk_class, score, conf, summary, v, ind, lim, actions = analyze_text_communication(news_text)
    assert risk_class == RiskClassification.LOW_RISK
    assert score <= 34


def test_ncb_extortion_with_parcel_and_transfer_triggers_high_risk():
    """Coercive combination of parcel seizure, drugs, and fund transfer must trigger PROC-IND-006."""
    scam_text = (
        "Customs department and Narcotics Control Bureau have seized your parcel containing MDMA contraband. "
        "Transfer customs clearance fee of Rs 65,000 immediately or face immediate arrest warrant."
    )
    violations = evaluate_procedural_fallacies(scam_text)
    codes = [v.code for v in violations]
    assert "PROC-IND-006" in codes

    risk_class, score, conf, summary, v, ind, lim, actions = analyze_text_communication(scam_text)
    assert risk_class == RiskClassification.HIGH_RISK
    assert score >= 70
