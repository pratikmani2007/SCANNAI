"""
Text & Threat Vector Analyzer.
Performs deterministic threat extraction, urgency classification, authority impersonation detection,
and explainable risk scoring.

Phase 3.2 Refined:
- Enforces strict scoring ranges: LOW RISK (0-34), NEEDS VERIFICATION (35-69), HIGH RISK (70-100).
- Enforces minimum score floor of 85 for critical procedural fallacies.
- Deduplicates evidence citations to avoid artificial score inflation.
- Supports Hinglish terminology and handles obfuscated keywords.
- Context-aware exclusions for educational discussions, legitimate bank alerts, and news mentions.

Product: SCANNAI | Team: ROCKERZ
"""

import re
from typing import List, Dict, Any, Tuple, Set
from app.models.schemas import (
    RiskClassification,
    ConfidenceLevel,
    IndicatorSeverity,
    SuspiciousIndicator,
    RecommendedAction,
    ProceduralViolation,
)
from app.services.procedural_rules import evaluate_procedural_fallacies


# Threat Pattern Categories & Definitions
THREAT_VECTORS: Dict[str, Dict[str, Any]] = {
    "IMPERSONATION_AUTHORITY": {
        "title": "Institutional & Law Enforcement Impersonation",
        "severity": IndicatorSeverity.HIGH,
        "patterns": [
            r"\b(cbi|central\s+bureau\s+of\s+investigation)\b",
            r"\b(enforcement\s+directorate|ed\s+officer)\b",
            r"\b(cyber\s+crime\s+branch|cyber\s+cell|crime\s+branch)\b",
            r"\b(supreme\s+court|high\s+court)\s+(order|warrant|notice)\b",
            r"\b(dcp|acp|ips|inspector|sp)\s+[a-z\s]+\b",
            r"\bnarcotics\s+control\s+bureau|ncb\b",
            r"\breserve\s+bank\s+of\s+india|rbi\s+officer\b",
            r"\bmumbai\s+police|delhi\s+police|state\s+police\b",
            r"\bcustoms\s+(department|officer|commissioner)\b",
            r"\b(police\s+thana|thane\s+se)\b",
        ],
    },
    "URGENCY_INTIMIDATION": {
        "title": "Manufactured Urgency & Coercive Deadline",
        "severity": IndicatorSeverity.CRITICAL,
        "patterns": [
            r"\bwithin\s+(\d+|fifteen|thirty|ten)\s+minutes\b",
            r"\bimmediate(ly)?\s+(arrest|action|consequences|transfer|giraftari)\b",
            r"\bdo\s+not\s+(disconnect|cut|hang\s+up)\b",
            r"\bnon-bailable\s+warrant\b",
            r"\bpolice\s+(team\s+is\s+coming|is\s+outside|at\s+your\s+house)\b",
            r"\barrest\s+you\s+(within|immediately|today)\b",
            r"\bgiraftari\s+warrant\b",
            r"\blast\s+and\s+final\s+warning\b",
        ],
    },
    "FINANCIAL_EXTORTION": {
        "title": "Coercive Fund Transfer & Verification Escrow Demand",
        "severity": IndicatorSeverity.CRITICAL,
        "patterns": [
            r"\btransfer\s+(amount|money|funds|rs\.?|inr)\s+to\s+(clear|verify|unfreeze|avoid\s+arrest)\b",
            r"\btransfer\s+(verification|security|clearance)\s+(deposit|fee|account)\b",
            r"\bsecurity\s+deposit\s+for\s+(bail|clearance|unfreeze)\b",
            r"\brefundable\s+(deposit|amount|verification\s+fee)\b",
            r"\brtgs|neft|imps\s+transfer\s+immediately\s+to\s+(avoid|clear)\b",
            r"\bpay\s+(\d+|rs\.?|inr)\s+immediately\s+to\s+(avoid\s+arrest|clear)\b",
            r"\bunfreeze\s+(your\s+)?account\s+by\s+paying\b",
            r"\brbi\s+verification\s+account\b",
            r"\br_?b_?i\s+v_?e_?r_?i_?f_?i_?c_?a_?t_?i_?o_?n\b",
        ],
    },
    "ISOLATION_SECRECY": {
        "title": "Psychological Isolation & Coercive Secrecy",
        "severity": IndicatorSeverity.HIGH,
        "patterns": [
            r"\bdo\s+not\s+(tell|inform|share\s+with)\s+(anyone|family|spouse|parents|lawyer|advocate)\b",
            r"\bgo\s+to\s+a\s+(quiet|private|isolated)\s+room\b",
            r"\block\s+the\s+door\b",
            r"\bconfidential\s+investigation\s+do\s+not\s+disclose\b",
            r"\bif\s+you\s+tell\s+anyone.*arrest\b",
            r"\bmaintain\s+absolute\s+secrecy\b",
        ],
    },
    "LEGAL_FALLACY_TERMS": {
        "title": "Fictitious Legal & Judicial Terminology",
        "severity": IndicatorSeverity.CRITICAL,
        "patterns": [
            r"\bdigital\s+arrest\b",
            r"\bd[\s\.\-_]*i[\s\.\-_]*g[\s\.\-_]*i[\s\.\-_]*t[\s\.\-_]*a[\s\.\-_]*l[\s\.\-_]+a[\s\.\-_]*r[\s\.\-_]*r[\s\.\-_]*e[\s\.\-_]*s[\s\.\-_]*t\b",
            r"\bonline\s+arrest\b",
            r"\bdigital\s+giraftari\b",
            r"\bvirtual\s+court\s+bail\b",
            r"\bskype\s+investigation\b",
            r"\brbi\s+clearance\s+account\b",
        ],
    },
}


def extract_threat_indicators(text: str) -> List[SuspiciousIndicator]:
    """
    Extracts behavioral, linguistic, and financial threat vectors from raw communication text.
    Applies deduplication and contextual filtering for educational and legitimate institutional references.
    """
    indicators: List[SuspiciousIndicator] = []
    if not text:
        return indicators

    # Contextual check: Educational/awareness discussions do not trigger fraudulent fallacy terms
    is_educational = bool(
        re.search(
            r"\b(awareness|seminar|webinar|workshop|article|educational|advisory|guidance|lecture|understanding)\s+(on|about|regarding)\s+digital\s+arrest\b",
            text,
            re.IGNORECASE,
        )
        or re.search(r"\bcaution\s+(against|on)\s+digital\s+arrest\b", text, re.IGNORECASE)
    )

    # Contextual check: Pure NCB/Police news mentions without threats/extortion
    is_pure_ncb_news = bool(
        re.search(
            r"(?=.*\b(narcotics\s+control\s+bureau|ncb)\b)(?!.*\b(transfer|pay|money|deposit|fee|arrest|giraftari|warrant|seized|parcel|customs)\b)",
            text,
            re.IGNORECASE,
        )
    )

    seen_citations: Set[str] = set()

    for category_key, category_data in THREAT_VECTORS.items():
        # In educational/awareness contexts, terms like "digital arrest" and institutional references like "University Cyber Cell" are educational
        if is_educational and category_key in ["LEGAL_FALLACY_TERMS", "IMPERSONATION_AUTHORITY"]:
            continue

        if category_key == "IMPERSONATION_AUTHORITY" and is_pure_ncb_news:
            continue

        for pattern_str in category_data["patterns"]:
            match = re.search(pattern_str, text, re.IGNORECASE)
            if match:
                matched_snippet = match.group(0).strip().lower()
                # Deduplication check: Avoid counting identical evidence snippets
                if matched_snippet in seen_citations:
                    continue

                seen_citations.add(matched_snippet)
                indicators.append(
                    SuspiciousIndicator(
                        category=category_data["title"],
                        severity=category_data["severity"],
                        title=f"Detected {category_data['title']}",
                        description=f"Communication contains language characteristic of coercive fraud: '{match.group(0)}'",
                        evidence_citation=match.group(0),
                    )
                )
                # Max 1 match per category to prevent keyword stuffing from inflating category count
                break

    return indicators


def synthesize_risk_score(
    procedural_violations: List[ProceduralViolation],
    indicators: List[SuspiciousIndicator],
    text_length: int,
) -> Tuple[RiskClassification, int, ConfidenceLevel, str, List[RecommendedAction]]:
    """
    Synthesizes detected procedural violations and threat indicators into a deterministic,
    scientifically justified 3-tier risk classification.

    Phase 3.2 Scoring Policy:
    - LOW RISK: 0 - 34
    - NEEDS VERIFICATION: 35 - 69
    - HIGH RISK: 70 - 100
    - Critical Rule Floor: Any confirmed critical statutory violation (PROC-IND-001, PROC-IND-002, PROC-IND-004)
      mandates a minimum final score of 85 and outputs HIGH RISK.
    - Non-critical combinations (e.g. PROC-IND-003, PROC-IND-005, PROC-IND-006 or multiple threat clusters)
      can score between 70 and 84 and also output HIGH RISK.
    - All scores are strictly bounded within [0, 100].
    """
    # 1. Critical vs Non-Critical Procedural Violations
    critical_rules = {"PROC-IND-001", "PROC-IND-002", "PROC-IND-004"}
    has_critical_procedure = any(v.code in critical_rules for v in procedural_violations)
    has_any_procedure = len(procedural_violations) > 0

    critical_indicators_count = sum(1 for ind in indicators if ind.severity == IndicatorSeverity.CRITICAL)
    high_indicators_count = sum(1 for ind in indicators if ind.severity == IndicatorSeverity.HIGH)

    # 2. Score Calculation
    if has_critical_procedure:
        # Mandatory score floor of 85 for critical statutory violations
        base_score = 85
        incremental = min(15, (critical_indicators_count * 5) + (high_indicators_count * 3))
        score = base_score + incremental

    elif has_any_procedure:
        # Non-critical procedural violation (PROC-IND-003, PROC-IND-005, PROC-IND-006)
        # Yields HIGH RISK in the 70 - 84 range
        base_score = 70
        incremental = min(14, (critical_indicators_count * 5) + (high_indicators_count * 3))
        score = base_score + incremental

    elif critical_indicators_count >= 1 and high_indicators_count >= 1:
        # Severe composite threat cluster without named statutory rule (e.g. urgency + extortion)
        score = 70 + min(10, (critical_indicators_count * 4) + (high_indicators_count * 2))

    elif critical_indicators_count >= 1 or high_indicators_count >= 2:
        # Suspicious combination requiring verification (range 50 - 65)
        score = 50 + min(19, (high_indicators_count * 7))

    elif high_indicators_count == 1:
        # Single high-severity indicator (e.g. isolated authority claim)
        score = 35

    elif len(indicators) > 0:
        # Minor or informational signals
        score = 25

    else:
        # Clean benign communication
        score = 10

    # Enforce strict mathematical bounds [0, 100]
    score = max(0, min(100, score))

    # 3. Categorization & Narrative (Strict 0-34, 35-69, 70-100 bands)
    if score >= 70:
        classification = RiskClassification.HIGH_RISK
        confidence = ConfidenceLevel.VERY_HIGH if has_critical_procedure else ConfidenceLevel.HIGH
        summary = (
            "CRITICAL ALERT: This communication exhibits characteristic hallmarks of an organized financial extortion "
            "or Digital Arrest impersonation scam. Multiple procedural violations and coercion markers were detected."
        )
        actions = [
            RecommendedAction(
                priority=1,
                category="IMMEDIATE_ACTION",
                action_text="IMMEDIATELY TERMINATE THE CALL OR CONVERSATION. Do not stay on video call or follow any instructions.",
                helpline_or_portal=None,
            ),
            RecommendedAction(
                priority=2,
                category="IMMEDIATE_ACTION",
                action_text="DO NOT TRANSFER ANY FUNDS. Police, CBI, ED, and courts never demand security deposits into clearing accounts.",
                helpline_or_portal=None,
            ),
            RecommendedAction(
                priority=3,
                category="REPORTING",
                action_text="Lodge an official cybercrime complaint immediately on the National Cybercrime Reporting Portal or call Helpline 1930.",
                helpline_or_portal="https://cybercrime.gov.in (Helpline: 1930)",
            ),
            RecommendedAction(
                priority=4,
                category="ADVISORY",
                action_text="Alert your bank if any financial or identity information was disclosed during the interaction.",
                helpline_or_portal="National Cybercrime Helpline: 1930",
            ),
        ]

    elif score >= 35:
        classification = RiskClassification.NEEDS_VERIFICATION
        confidence = ConfidenceLevel.MEDIUM
        summary = (
            "CAUTION ADVISED: The communication contains suspicious urgency, institutional claims, or unusual financial requests. "
            "Independent verification through official directory numbers is strongly recommended before taking any action."
        )
        actions = [
            RecommendedAction(
                priority=1,
                category="VERIFICATION",
                action_text="Do not respond or call back using the contact details provided in the message.",
                helpline_or_portal=None,
            ),
            RecommendedAction(
                priority=2,
                category="VERIFICATION",
                action_text="Verify the claimed organization's contact number independently from their official website.",
                helpline_or_portal="Official Department Portals",
            ),
            RecommendedAction(
                priority=3,
                category="ADVISORY",
                action_text="Never share OTPs, UPI PINs, or bank account credentials.",
                helpline_or_portal="RBI Sachet Portal: https://sachet.rbi.org.in",
            ),
        ]

    else:
        classification = RiskClassification.LOW_RISK
        confidence = ConfidenceLevel.HIGH if text_length > 30 else ConfidenceLevel.MEDIUM
        summary = (
            "LOW RISK: No recognized digital arrest patterns, coercive legal threats, or unauthorized payment requests "
            "were detected in the submitted text. Continue practicing standard digital hygiene."
        )
        actions = [
            RecommendedAction(
                priority=1,
                category="ADVISORY",
                action_text="Always confirm unexpected financial payment requests directly with the sender through a secondary channel.",
                helpline_or_portal=None,
            ),
            RecommendedAction(
                priority=2,
                category="ADVISORY",
                action_text="Never disclose banking OTPs, debit card PINs, or confidential credentials to anyone.",
                helpline_or_portal="https://cybercrime.gov.in",
            ),
        ]

    return classification, score, confidence, summary, actions


def analyze_text_communication(
    text: str,
) -> Tuple[RiskClassification, int, ConfidenceLevel, str, List[ProceduralViolation], List[SuspiciousIndicator], List[str], List[RecommendedAction]]:
    """
    Orchestrates end-to-end communication analysis:
    1. Evaluates procedural legal fallacies.
    2. Extracts threat indicators with deduplication.
    3. Synthesizes risk score and explainable narrative.
    4. Compiles explicit confidence limitations.
    """
    clean_text = text.strip() if text else ""
    text_length = len(clean_text)

    # 1. Procedural Fallacies
    procedural_violations = evaluate_procedural_fallacies(clean_text)

    # 2. Threat Vector Extraction (Deduplicated & Context-Aware)
    detected_indicators = extract_threat_indicators(clean_text)

    # 3. Risk Synthesis (Strict 0-34, 35-69, 70-100 Policy)
    classification, score, confidence, summary, actions = synthesize_risk_score(
        procedural_violations, detected_indicators, text_length
    )

    # 4. Explicit Responsible AI Caveats
    limitations = [
        "Analysis is performed deterministically based on statutory procedures and known scam vectors.",
        "This evaluation analyzes communication patterns; it does not constitute a formal judicial judgment or legal advice.",
        "Scammers may evolve novel phrasing not captured by current behavioral rules. Always independently cross-verify unexpected demands.",
    ]

    return (
        classification,
        score,
        confidence,
        summary,
        procedural_violations,
        detected_indicators,
        limitations,
        actions,
    )
