/**
 * Data Contracts and Type Definitions for SCANNAI.
 * Strictly aligned with Backend Pydantic Schemas.
 * Product: SCANNAI | Team: ROCKERZ
 */

export type EvidenceType =
  | 'TEXT'
  | 'DOCUMENT_PDF'
  | 'SCREENSHOT_IMAGE'
  | 'AUDIO_RECORDING'
  | 'VIDEO_RECORDING';

export type RiskClassification = 'LOW RISK' | 'NEEDS VERIFICATION' | 'HIGH RISK';

export type ConfidenceLevel = 'LOW' | 'MEDIUM' | 'HIGH' | 'VERY HIGH';

export type IndicatorSeverity =
  | 'INFORMATIONAL'
  | 'LOW'
  | 'MEDIUM'
  | 'HIGH'
  | 'CRITICAL';

export interface SuspiciousIndicator {
  category: string;
  severity: IndicatorSeverity;
  title: string;
  description: string;
  evidence_citation?: string | null;
}

export interface ProceduralViolation {
  code: string;
  official_norm: string;
  observed_violation: string;
  jurisdiction: string;
}

export interface RecommendedAction {
  priority: number;
  category: 'IMMEDIATE_ACTION' | 'VERIFICATION' | 'REPORTING' | 'ADVISORY' | string;
  action_text: string;
  helpline_or_portal?: string | null;
}

export interface EvidenceMetadata {
  evidence_type: EvidenceType;
  original_filename?: string | null;
  file_size_bytes?: number | null;
  mime_type?: string | null;
  sha256_hash?: string | null;
  uploaded_at: string;
}

export interface AnalysisResponse {
  case_id: string;
  timestamp: string;
  risk_classification: RiskClassification;
  risk_score: number;
  confidence_level: ConfidenceLevel;
  executive_summary: string;
  procedural_violations: ProceduralViolation[];
  detected_indicators: SuspiciousIndicator[];
  confidence_limitations: string[];
  recommended_actions: RecommendedAction[];
  evidence_items: EvidenceMetadata[];
}

export interface HealthResponse {
  status: string;
  application: string;
  version: string;
  timestamp: string;
  environment: string;
  ingestion_status: {
    max_upload_size_mb: number;
    allowed_mime_types: string[];
    storage_path: string;
    storage_directories: Record<string, boolean>;
  };
}

export interface ApiError {
  error_code?: string;
  message: string;
  details?: Array<{ field?: string; message: string }>;
}
