"""
Procedural Fallacy Knowledge Base.
Codifies verified legal and institutional procedural standards for India and international fraud defense.

Primary Statutory & Institutional Authorities:
- Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS) [Act No. 46 of 2023, effective 1 July 2024; India Code: https://www.indiacode.nic.in/indiacode/handle/123456789/20099?view_type=browse]
- Code of Criminal Procedure, 1973 (CrPC) [Predecessor statute saved under BNSS Section 531(2)(a) strictly for pending appeals, applications, trials, inquiries, or investigations commenced prior to 1 July 2024]
- Constitution of India [Article 22(1) - Fundamental right to legal counsel & to be informed of grounds of arrest]
- Ministry of Home Affairs (MHA) / PIB - Parliamentary Response: 'STEPS TAKEN TO ADDRESS THE ISSUE OF DIGITAL ARREST SCAMS' (12 March 2025; https://www.pib.gov.in/PressReleasePage.aspx?PRID=2110809)
- Reserve Bank of India (RBI) - Public Caution: 'RBI Cautions Public on Frauds in the Name of KYC Updation / Digital Arrest / Verification Accounts' (https://rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=58595)
- Telecom Regulatory Authority of India (TRAI) - Press Release No. 55/2024 (https://www.trai.gov.in/sites/default/files/2024-10/PR_No.55of2024.pdf)
- Central Board of Indirect Taxes and Customs (CBIC) - Circulars on Document Identification Number (DIN) System (Circular No. 19/2019-Customs)
- Narcotics Drugs and Psychotropic Substances Act, 1985 (NDPS Act) [Section 67; India Code: https://www.indiacode.nic.in/indiacode/handle/123456789/1791]

Product: SCANNAI | Team: ROCKERZ
"""

import re
from typing import List, Dict, Any, Optional
from app.models.schemas import ProceduralViolation, IndicatorSeverity


class ProceduralRule:
    """Represents a single deterministic procedural rule based on verified statutory and institutional norms."""

    def __init__(
        self,
        code: str,
        title: str,
        official_norm: str,
        observed_violation: str,
        jurisdiction: str,
        patterns: List[str],
        severity: IndicatorSeverity,
        authority_reference: str,
        exclusion_patterns: Optional[List[str]] = None,
    ):
        self.code = code
        self.title = title
        self.official_norm = official_norm
        self.observed_violation = observed_violation
        self.jurisdiction = jurisdiction
        self.patterns = [re.compile(p, re.IGNORECASE) for p in patterns]
        self.exclusion_patterns = [re.compile(p, re.IGNORECASE) for p in (exclusion_patterns or [])]
        self.severity = severity
        self.authority_reference = authority_reference

    def matches(self, text: str) -> Optional[str]:
        """
        Returns the matched substring if any pattern matches and no exclusion pattern is met, else None.
        """
        # If an exclusion pattern matches (e.g. legitimate e-Courts listing, educational seminar, or TSP bill), skip
        for excl in self.exclusion_patterns:
            if excl.search(text):
                return None

        for pattern in self.patterns:
            match = pattern.search(text)
            if match:
                return match.group(0)
        return None


# Verified Statutory & Banking Procedural Rules (Phase 3.2 Refined)
PROCEDURAL_RULES_REGISTRY: List[ProceduralRule] = [
    ProceduralRule(
        code="PROC-IND-001",
        title="Fictitious 'Digital Arrest' via Video or Messaging Platform",
        official_norm=(
            "Indian statutory law does not establish or recognize any standalone procedure called 'digital arrest' through which "
            "police or investigative agencies can arrest, detain, or hold an individual in custody via private video calls. "
            "Under Chapter V of the Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS) [specifically Sections 35 to 62], arrest requires "
            "physical custody, formal documentation, and mandatory production before a Judicial Magistrate within 24 hours. "
            "The statutory framework for electronic communication and summons under the BNSS distinguishes distinct procedural stages: "
            "(1) Section 35(3) governs police notices of appearance where arrest is not mandatory, directing the person to appear before "
            "the police officer or at such other place as may be specified in the notice, without implying that every notice requires physical "
            "attendance or that every electronic communication is invalid; "
            "(2) Section 63 prescribes the formal form of court summons (in writing, in duplicate, signed by the presiding officer or bearing "
            "the image of the Court's seal or digital signature); "
            "(3) Section 64 provides that summons should, where practicable, be served personally by delivering or tendering a duplicate, "
            "while the proviso permits electronic service of summons bearing the image of the Court's seal, in such form and manner as the "
            "State Government may provide by rules; "
            "(4) Section 179 empowers a police officer investigating a case to require the attendance of witnesses by written order, subject to "
            "the statutory safeguards that five specified categories of persons—(i) male persons under fifteen years of age, (ii) persons above "
            "sixty years of age, (iii) women, (iv) mentally or physically disabled persons, and (v) persons with acute illness—cannot be required "
            "to attend at any place other than their residence, though the second proviso permits them to attend the police station voluntarily "
            "if they are willing; and "
            "(5) Section 530 permits all trials, inquiries, and criminal proceedings, including issuance, service, and execution of summons and "
            "warrants, to be held in electronic mode via official audio-video electronic systems (such as High Court and District Court Cisco Webex/NIC portals). "
            "Crucially, these provisions do not imply that an unsolicited WhatsApp message or video call from someone claiming to be police "
            "is an authentic legal notice. Legitimate notices direct appearance or provide verifiable official case coordinates and never mandate "
            "custodial confinement in a private room over commercial messaging apps (WhatsApp, Skype) or demand immediate money transfers. "
            "Furthermore, because electronic summons rules under Section 64 and High Court electronic filing rules vary by State jurisdiction, "
            "procedural service requirements must be evaluated against applicable local state rules. "
            "As confirmed by the Ministry of Home Affairs (MHA) Parliamentary Response dated 12 March 2025 (PIB PRID=2110809), 'digital arrest' "
            "is an organized cyber-fraud technique where fraudsters impersonate law enforcement to intimidate and extort citizens."
        ),
        observed_violation="Communication threatens or imposes a virtual arrest or continuous video detention under color of official authority.",
        jurisdiction="IN",
        patterns=[
            # Standard & Hinglish variants of Digital Arrest
            r"\b(digital|online|video\s+call\s+par)\s+(giraftari|girftari|arrest)\b",
            # Spaced and obfuscated variants (e.g., d-i-g-i-t-a-l   a-r-r-e-s-t)
            r"\bd[\s\.\-_]*i[\s\.\-_]*g[\s\.\-_]*i[\s\.\-_]*t[\s\.\-_]*a[\s\.\-_]*l[\s\.\-_]+a[\s\.\-_]*r[\s\.\-_]*r[\s\.\-_]*e[\s\.\-_]*s[\s\.\-_]*t\b",
            r"\bvideo\s+call\s+(custody|interrogation|arrest|surveillance)\b",
            r"\bremain\s+on\s+(video|skype|whatsapp)\s+call\s+(until|or\s+face|under\s+arrest|investigation)\b",
            r"\bdo\s+not\s+(disconnect|cut)\s+the\s+(video\s+)?call\s+(or\s+police|until\s+cleared)\b",
            r"\bvirtual\s+police\s+station\b",
        ],
        severity=IndicatorSeverity.CRITICAL,
        authority_reference="MHA Parliamentary Response (12 March 2025, PIB PRID=2110809) & BNSS Section 530 / Chapter V",
        exclusion_patterns=[
            # Distinguish legitimate e-Courts VC hearings without extortion/coercion
            r"(?=.*\b(ecourts|e-courts|cause\s+list|bench\s+\d+|delhihighcourt\.webex|highcourt|district\s+court)\b)(?!.*\b(transfer|pay\s+money|threat|giraftari|arrest)\b)",
            # Distinguish educational, seminar, academic, or advisory discussions about digital arrest
            r"\b(awareness|seminar|webinar|workshop|article|educational|advisory|guidance|lecture|understanding)\s+(on|about|regarding)\s+digital\s+arrest\b",
            r"\bcaution\s+(against|on)\s+digital\s+arrest\b",
        ],
    ),
    ProceduralRule(
        code="PROC-IND-002",
        title="Fictitious Verification / Clearance / Government Escrow Account Demand",
        official_norm=(
            "The Reserve Bank of India (RBI) does not maintain bank accounts in the names of individuals, companies, or trusts for safekeeping "
            "or disbursal of funds, nor does it ask individuals to deposit money into such accounts. As established by official RBI Public Caution "
            "Notices (PRID 58595), government and regulatory agencies never direct individuals to transfer funds to a 'security escrow', 'verification "
            "account', or 'clearance deposit' to verify innocence or unfreeze bank accounts. "
            "Under Indian law, statutory asset freezing follows distinct legal mechanisms: (1) police seizure/freezing under Section 107 of the BNSS, 2023 "
            "(formerly Section 102 CrPC) requires reporting forthwith to a Judicial Magistrate, and (2) attachment under Section 17 of the Prevention of "
            "Money Laundering Act, 2002 (PMLA) requires formal orders served directly on financial institutions with confirmation by the Adjudicating "
            "Authority. Neither statutory process involves voluntary fund transfers by the accused into third-party clearance accounts. "
            "(Note: Legitimate commercial escrow agreements in corporate or property transactions are recognized; this fallacy strictly targets "
            "fraudulent claims of regulatory, police, or government verification accounts)."
        ),
        observed_violation="Demand to transfer personal funds to a third-party account under the pretext of an official RBI or government verification clearance.",
        jurisdiction="IN",
        patterns=[
            # Specifically targets purported regulatory/government/police verification accounts
            r"\brbi\s+(verification|escrow|security\s+deposit|clearance)\b",
            r"\b(government|police|cbi|ed|court|customs)\s+(reserve|verification|clearance|escrow)\s+(account|deposit)\b",
            r"\b(cbi|police|ed|court|rbi|government).*(transfer|pay).*(verification|security|clearance)\s+(deposit|account|fee)\b",
            r"\btransfer\s+(verification|security|clearance)\s+(deposit|fee|account)\b",
            r"\btransfer\s+(funds|money|amount|balance)\s+to\s+(verify|clear|unfreeze)\s+(your\s+)?(account|funds|innocence)\b",
            r"\brefundable\s+(security|clearance|verification)\s+deposit\s+to\s+(clear|police|rbi|court|unfreeze)\b",
            r"\bverify\s+your\s+bank\s+balance\s+by\s+transferring\b",
            r"\br_?b_?i\s+v_?e_?r_?i_?f_?i_?c_?a_?t_?i_?o_?n\b",
        ],
        severity=IndicatorSeverity.CRITICAL,
        authority_reference="RBI Public Caution Notice (PRID 58595) & BNSS Section 107 / PMLA Section 17",
    ),
    ProceduralRule(
        code="PROC-IND-003",
        title="Coercive Penal or Bail Payment Demand via Personal UPI Handle",
        official_norm=(
            "Statutory court bails, judicial fines, and police penalties must be paid through designated, authorized government treasury "
            "and judicial collection systems (e.g., e-Courts digital portal, Bharatkosh, State Treasury e-GRAS, State Police e-Challan systems) "
            "with a verified treasury receipt. Government payment channels are not restricted to any single universal portal; various authorized "
            "arrangements exist across central ministries and state governments. "
            "Crucially, beneficiary display names alone must never be relied upon to establish payment authenticity, as fraudsters can easily "
            "configure arbitrary display names (e.g., 'Cyber Crime Cell', 'Police Department', or 'Reserve Bank of India') on private accounts. "
            "Authentic government payment verification requires multi-factor evaluation: (1) access through an official government domain "
            "(.gov.in / .nic.in); (2) authorized payment gateway integration; (3) verified institutional beneficiary VPA/account identity; "
            "(4) traceable transaction reference linked to an official FIR, case, or challan number; and (5) legitimate statutory context. "
            "Conversely, unfamiliar state government payment portals must not be automatically assumed to be fraudulent without domain verification. "
            "Ordinary commercial or personal UPI transactions between individuals and registered merchants are lawful; this rule is triggered "
            "solely when a personal or private UPI transfer is demanded under fabricated police or court authority for bail, fines, or case clearance."
        ),
        observed_violation="Demanding statutory penalties, bail money, or case clearance fees through personal UPI handles or unverified beneficiary accounts.",
        jurisdiction="IN",
        patterns=[
            # Contextual coupling: Must combine penal/case demand with UPI handle or payment
            r"\b(bail|penalty|fine|challan|clearance\s+fee|case\s+fee)\b.*@[\w\.\-]+",
            r"\bpay\s+(bail|penalty|fine|challan|clearance\s+fee)\s+(via|through|to)\s+upi\b",
            r"\btransfer\s+(bail|penalty|fine|clearance\s+deposit)\s+to\s+[\w\.\-]+@(oksbi|okaxis|okicici|okhdfcbank|paytm|ybl|apl|upi)\b",
            r"\b(court|police|cbi|ed)\s+(fine|deposit|penalty)\s+on\s+upi\b",
        ],
        severity=IndicatorSeverity.HIGH,
        authority_reference="e-Courts Project Digital Payment Guidelines & Government Treasury Rules (Bharatkosh / e-GRAS)",
    ),
    ProceduralRule(
        code="PROC-IND-004",
        title="Unlawful Coercive Secrecy & Deprivation of Legal Counsel",
        official_norm=(
            "Article 22(1) of the Constitution of India guarantees that no person who is arrested shall be detained without being informed "
            "of the grounds of arrest, nor denied the right to consult and be defended by a legal practitioner of their choice. "
            "Section 38 of the BNSS, 2023 provides that when a person is arrested and interrogated by the police, they are entitled to meet "
            "an advocate of their choice during interrogation (though not throughout the entirety of interrogation). "
            "Furthermore, Section 48 of the BNSS places an obligation on the arresting officer to forthwith inform a nominated relative or friend "
            "regarding the arrest and place of custody. While legitimate confidentiality applies in specific statutory contexts (such as in-camera "
            "proceedings under BNSS Section 366 or the Official Secrets Act), coercive telephone orders demanding absolute isolation in a locked room "
            "and forbidding communication with legal counsel or family under threat of arrest are hallmarks of fraudulent extortion."
        ),
        observed_violation="Coercing the victim into absolute secrecy and forbidding them from consulting legal counsel or notifying family under threat of arrest.",
        jurisdiction="IN",
        patterns=[
            r"\bdo\s+not\s+(tell|inform|contact)\s+(anyone|family|lawyer|advocate|counsel|bank)\b",
            r"\b(sit|stay)\s+in\s+an?\s+isolated\s+room\s+and\s+do\s+not\s+(tell|talk)\b",
            r"\bclose\s+the\s+door\s+and\s+(stay|sit)\s+alone\s+(or|during)\b",
            r"\bif\s+you\s+(tell|inform)\s+(anyone|lawyer|family).*arrest\b",
            r"\bmaintain\s+(absolute\s+)?secrecy\s+or\s+face\s+(arrest|charges)\b",
        ],
        severity=IndicatorSeverity.CRITICAL,
        authority_reference="Constitution of India Article 22(1), BNSS Section 38, BNSS Section 48 & D.K. Basu v. State of West Bengal",
    ),
    ProceduralRule(
        code="PROC-IND-005",
        title="Fraudulent Telecom Disconnection Threat Impersonating Regulatory Authority",
        official_norm=(
            "As established by the Telecom Regulatory Authority of India (TRAI) in Press Release No. 55/2024, TRAI does not initiate communications "
            "to customers threatening mobile-number disconnection. Disconnection processes are governed by statutory licensing conditions and "
            "are executed strictly by the relevant Telecom Service Provider (TSP: Airtel, Jio, Vi, BSNL) for valid statutory causes such as billing "
            "default, failed re-verification/KYC compliance, or fraudulent misuse coordinated via the Department of Telecommunications (DoT) "
            "Sanchar Saathi / Chakshu portal. The urgent 'disconnection within 2 hours' ultimatum is an observed empirical scam-script indicator, "
            "not a statutory timeline. (Legitimate billing, plan expiry, or verified re-KYC service notices from TSPs do not constitute fraud)."
        ),
        observed_violation="Threatening immediate mobile number disconnection by impersonating TRAI or presenting an arbitrary 2-hour ultimatum without TSP due process.",
        jurisdiction="IN",
        patterns=[
            r"\bsim\s+(card\s+)?(will\s+be\s+)?(blocked|disconnected|suspended)\s+in\s+\d+\s+(hours?|minutes?)\b",
            r"\btrai\s+(disconnection|blocking|notice)\b",
            r"\ball\s+your\s+(mobile|phone)\s+numbers\s+will\s+be\s+blocked\s+by\s+(trai|telecom)\b",
            r"\btelecom\s+regulatory\s+authority\s+.*(disconnect|suspend)\b",
        ],
        severity=IndicatorSeverity.HIGH,
        authority_reference="TRAI Press Release No. 55/2024 & DoT Sanchar Saathi / Chakshu Advisory",
        exclusion_patterns=[
            # Distinguish legitimate TSP billing or service notices
            r"(?=.*\b(airtel|jio|vodafone|vi|bsnl)\b)(?=.*\b(bill|invoice|plan|recharge|payment\s+due|statement)\b)(?!.*\b(police|cbi|trai\s+notice|arrest|illegal|crime|hours?)\b)",
        ],
    ),
    ProceduralRule(
        code="PROC-IND-006",
        title="Fraudulent Courier Contraband Extortion (Customs / NCB Impersonation)",
        official_norm=(
            "Distinct statutory and commercial procedures govern customs, narcotics investigations, and courier transit: "
            "(1) Central Board of Indirect Taxes and Customs (CBIC) implements the Document Identification Number (DIN) system "
            "(CBIC Circular No. 19/2019-Customs) for official search authorizations, summons, and communications; Indian Customs never "
            "demands payment of duties or penalties over personal telephone calls or to private personal UPI handles; "
            "(2) Narcotics Control Bureau (NCB) exercises powers under Section 67 of the NDPS Act, 1985 to call for information, require production "
            "of documents, and examine persons acquainted with relevant facts. Section 67 does not authorize on-the-spot financial settlement "
            "over telephone calls or demands for clearance fees to drop narcotics charges; "
            "(3) Commercial courier operators (FedEx, DHL, Blue Dart) follow established commercial customs brokerage and clearance procedures "
            "and do not possess police authority or threaten customers with immediate arrest. Extortion occurs when fraudsters impersonate "
            "these entities in a coercive combination involving fake parcel seizures, threats of arrest, and immediate demands for online money transfers."
        ),
        observed_violation="Claiming a courier parcel contains contraband or narcotics and demanding financial payment over the phone to clear the recipient.",
        jurisdiction="IN",
        patterns=[
            r"\b(fedex|dhl|india\s+post|bluedart)\s+(parcel|package|courier).*(narcotics|drugs|mdma|passports|contraband)\b",
            r"\b(parcel|package)\s+contains\s+(narcotics|drugs|mdma|contraband).*transfer\b",
            r"\bcustoms\s+(clearance\s+fee|settlement)\s+for\s+(parcel|package)\b",
            r"\bnarcotics\s+control\s+bureau|ncb\s+(case|clearance)\s+.*(transfer|pay|fee)\b",
            r"\bintercepted\s+by\s+customs\s+.*(transfer|pay|fee|deposit)\b",
        ],
        severity=IndicatorSeverity.HIGH,
        authority_reference="CBIC Circular No. 19/2019-Customs (DIN System), Section 67 NDPS Act, and FedEx/DHL Customer Fraud Advisories",
        exclusion_patterns=[
            # Distinguish general news, discussions, or genuine courier delivery updates without payment demands
            r"(?=.*\b(narcotics\s+control\s+bureau|ncb)\b)(?!.*\b(transfer|pay|money|deposit|fee|arrest|giraftari|warrant)\b)",
        ],
    ),
]


def evaluate_procedural_fallacies(text: str) -> List[ProceduralViolation]:
    """
    Evaluates text against the verified procedural rules registry.
    Returns a list of structured ProceduralViolation objects for every rule triggered.
    """
    violations: List[ProceduralViolation] = []
    if not text or not text.strip():
        return violations

    for rule in PROCEDURAL_RULES_REGISTRY:
        matched_snippet = rule.matches(text)
        if matched_snippet:
            violations.append(
                ProceduralViolation(
                    code=rule.code,
                    official_norm=rule.official_norm,
                    observed_violation=f"{rule.observed_violation} (Matched phrase: '{matched_snippet}')",
                    jurisdiction=rule.jurisdiction,
                )
            )

    return violations
