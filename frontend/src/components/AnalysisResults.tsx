import React from 'react';
import { AnalysisResponse } from '../types/analysis';
import { RiskIndicator } from './RiskIndicator';
import {
  ShieldAlert,
  Scale,
  ExternalLink,
  PhoneCall,
  CheckCircle2,
  FileCheck,
  Info,
  Clock,
  Hash,
  Copy,
} from 'lucide-react';

interface AnalysisResultsProps {
  response: AnalysisResponse;
}

export const AnalysisResults: React.FC<AnalysisResultsProps> = ({ response }) => {
  const [copied, setCopied] = React.useState(false);

  const copyCaseId = () => {
    navigator.clipboard.writeText(response.case_id);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getSeverityBadge = (severity: string) => {
    switch (severity) {
      case 'CRITICAL':
        return 'bg-rose-950 text-rose-300 border-rose-800';
      case 'HIGH':
        return 'bg-orange-950 text-orange-300 border-orange-800';
      case 'MEDIUM':
        return 'bg-amber-950 text-amber-300 border-amber-800';
      default:
        return 'bg-slate-800 text-slate-300 border-slate-700';
    }
  };

  const formattedDate = new Date(response.timestamp).toLocaleString('en-IN', {
    dateStyle: 'medium',
    timeStyle: 'medium',
  });

  return (
    <div id="results-dashboard" className="mt-8 space-y-6">
      {/* Header bar: Case ID & Timestamp */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between p-3 rounded-lg bg-cyber-surface/90 border border-slate-800 text-xs font-mono text-slate-400 gap-2">
        <div className="flex items-center space-x-2">
          <Hash className="w-3.5 h-3.5 text-cyan-400" />
          <span className="text-slate-300 font-semibold">Case Reference:</span>
          <span className="text-cyan-300 bg-slate-900 px-2 py-0.5 rounded border border-slate-800">
            {response.case_id}
          </span>
          <button
            onClick={copyCaseId}
            className="hover:text-cyan-400 transition-colors p-1"
            title="Copy Case Reference ID"
          >
            {copied ? (
              <span className="text-[10px] text-emerald-400 font-sans">Copied!</span>
            ) : (
              <Copy className="w-3.5 h-3.5" />
            )}
          </button>
        </div>

        <div className="flex items-center space-x-2">
          <Clock className="w-3.5 h-3.5 text-slate-500" />
          <span>Analyzed: {formattedDate}</span>
          <span className="text-slate-600">•</span>
          <span className="text-emerald-400">100% Offline Engine</span>
        </div>
      </div>

      {/* 1. Risk Score Gauge Component */}
      <RiskIndicator
        score={response.risk_score}
        classification={response.risk_classification}
        confidence={response.confidence_level}
      />

      {/* 2. Executive Summary */}
      <div className="p-4 rounded-xl bg-cyber-surface/80 border border-slate-800">
        <h4 className="text-xs font-mono font-semibold text-cyan-400 uppercase tracking-wider mb-2 flex items-center space-x-1.5">
          <Info className="w-4 h-4" />
          <span>Forensic Executive Summary</span>
        </h4>
        <p className="text-sm text-slate-200 leading-relaxed font-sans">
          {response.executive_summary}
        </p>
      </div>

      {/* 3. Procedural Fallacies / Statutory Violations */}
      {response.procedural_violations.length > 0 && (
        <div className="p-5 rounded-xl bg-slate-900/90 border border-rose-900/60 shadow-lg shadow-rose-950/20">
          <div className="flex items-center justify-between mb-3">
            <h4 className="text-sm font-semibold text-rose-300 flex items-center space-x-2">
              <Scale className="w-4 h-4 text-rose-400" />
              <span>Statutory Procedural Violations Identified ({response.procedural_violations.length})</span>
            </h4>
            <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-rose-950 text-rose-400 border border-rose-800">
              Direct Legal Fallacies
            </span>
          </div>

          <div className="space-y-3">
            {response.procedural_violations.map((violation, idx) => (
              <div
                key={idx}
                className="p-3.5 rounded-lg bg-cyber-bg/80 border border-slate-800/90 hover:border-rose-800/50 transition-colors"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-mono font-bold text-rose-400 bg-rose-950/80 px-2 py-0.5 rounded border border-rose-900">
                    {violation.code}
                  </span>
                  <span className="text-[11px] text-slate-500 font-mono">
                    Jurisdiction: {violation.jurisdiction}
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-2 text-xs">
                  {/* Official Statutory Norm */}
                  <div className="p-2.5 rounded bg-slate-900/60 border border-slate-800">
                    <span className="text-[10px] font-mono font-semibold text-emerald-400 uppercase tracking-wider block mb-1">
                      Official Legal Procedure:
                    </span>
                    <p className="text-slate-300 leading-snug">
                      {violation.official_norm}
                    </p>
                  </div>

                  {/* Observed Coercive Violation */}
                  <div className="p-2.5 rounded bg-rose-950/30 border border-rose-900/40">
                    <span className="text-[10px] font-mono font-semibold text-rose-400 uppercase tracking-wider block mb-1">
                      Observed Fraudulent Deviation:
                    </span>
                    <p className="text-slate-300 leading-snug">
                      {violation.observed_violation}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 4. Threat Vectors & Detected Indicators */}
      {response.detected_indicators.length > 0 && (
        <div className="p-5 rounded-xl bg-cyber-surface/80 border border-slate-800">
          <h4 className="text-sm font-semibold text-slate-200 mb-3 flex items-center space-x-2">
            <ShieldAlert className="w-4 h-4 text-cyan-400" />
            <span>Threat Vector Breakdown & Behavioral Markers</span>
          </h4>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {response.detected_indicators.map((indicator, idx) => (
              <div
                key={idx}
                className="p-3 rounded-lg bg-slate-900/70 border border-slate-800 flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-xs font-semibold text-white">
                      {indicator.title}
                    </span>
                    <span
                      className={`text-[9px] font-mono font-semibold px-1.5 py-0.5 rounded border uppercase ${getSeverityBadge(
                        indicator.severity
                      )}`}
                    >
                      {indicator.severity}
                    </span>
                  </div>
                  <p className="text-xs text-slate-300 leading-snug">
                    {indicator.description}
                  </p>
                </div>

                {indicator.evidence_citation && (
                  <div className="mt-2 pt-2 border-t border-slate-800/80">
                    <span className="text-[10px] font-mono text-slate-500 block mb-0.5">
                      Matched Pattern Citation:
                    </span>
                    <p className="text-[11px] font-mono text-cyan-300/90 bg-slate-950 p-1.5 rounded border border-slate-800 break-words">
                      "{indicator.evidence_citation}"
                    </p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 5. Evidence Files Ingested (if any) */}
      {response.evidence_items && response.evidence_items.length > 0 && (
        <div className="p-4 rounded-xl bg-cyber-surface/60 border border-slate-800 text-xs">
          <h4 className="text-xs font-mono font-semibold text-slate-300 uppercase tracking-wider mb-2 flex items-center space-x-1.5">
            <FileCheck className="w-4 h-4 text-cyan-400" />
            <span>Ingested Evidence Artifacts ({response.evidence_items.length})</span>
          </h4>
          <div className="space-y-2">
            {response.evidence_items.map((item, idx) => (
              <div
                key={idx}
                className="p-2.5 rounded bg-slate-900/80 border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-1 text-[11px] font-mono"
              >
                <div className="flex items-center space-x-2 truncate">
                  <span className="text-cyan-400 font-semibold">{item.evidence_type}</span>
                  {item.original_filename && (
                    <span className="text-slate-200 truncate">({item.original_filename})</span>
                  )}
                </div>
                <div className="flex items-center space-x-3 text-slate-400 text-[10px]">
                  {item.file_size_bytes !== null && item.file_size_bytes !== undefined && (
                    <span>{(item.file_size_bytes / 1024).toFixed(1)} KB</span>
                  )}
                  {item.mime_type && <span>{item.mime_type}</span>}
                  {item.sha256_hash && (
                    <span className="text-slate-500" title={`SHA256: ${item.sha256_hash}`}>
                      SHA: {item.sha256_hash.substring(0, 12)}...
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 6. Recommended Action Plan */}
      <div className="p-5 rounded-xl bg-slate-900/90 border border-slate-800">
        <h4 className="text-sm font-semibold text-white mb-3 flex items-center space-x-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          <span>Prescribed Citizen Response Protocol</span>
        </h4>

        <div className="space-y-2.5">
          {response.recommended_actions.map((action, idx) => (
            <div
              key={idx}
              className="p-3 rounded-lg bg-cyber-bg/80 border border-slate-800/90 flex flex-col sm:flex-row sm:items-center justify-between gap-2"
            >
              <div className="flex items-start space-x-3">
                <span className="flex-shrink-0 w-5 h-5 rounded-full bg-cyan-950 border border-cyan-700 text-cyan-300 font-mono text-xs flex items-center justify-center font-bold">
                  {action.priority}
                </span>
                <div>
                  <span className="text-[10px] font-mono text-cyan-400/90 uppercase tracking-wider font-semibold block">
                    {action.category}
                  </span>
                  <p className="text-xs text-slate-200 mt-0.5 leading-snug">
                    {action.action_text}
                  </p>
                </div>
              </div>

              {action.helpline_or_portal && (
                <div className="flex-shrink-0 sm:ml-4">
                  {action.helpline_or_portal.startsWith('http') ? (
                    <a
                      href={action.helpline_or_portal}
                      target="_blank"
                      rel="noreferrer"
                      className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-md bg-cyan-950/80 hover:bg-cyan-900 border border-cyan-700/60 text-cyan-300 text-xs font-mono font-medium transition-colors"
                    >
                      <span>Report Portal</span>
                      <ExternalLink className="w-3.5 h-3.5" />
                    </a>
                  ) : (
                    <div className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-md bg-rose-950/80 border border-rose-700/60 text-rose-300 text-xs font-mono font-medium">
                      <PhoneCall className="w-3.5 h-3.5 text-rose-400" />
                      <span>{action.helpline_or_portal}</span>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* 7. Confidence Limitations & Caveats */}
      {response.confidence_limitations.length > 0 && (
        <div className="p-3.5 rounded-lg bg-cyber-surface/40 border border-slate-800/60 text-xs text-slate-400 font-sans space-y-1">
          <span className="font-mono font-semibold text-slate-300 block text-[11px]">
            Forensic Scope & Technical Limitations:
          </span>
          <ul className="list-disc list-inside space-y-0.5 text-[11px] text-slate-400">
            {response.confidence_limitations.map((limitation, idx) => (
              <li key={idx}>{limitation}</li>
            ))}
          </ul>
        </div>
      )}

      {/* 8. Mandatory Prototype Disclaimer */}
      <div className="p-3.5 rounded-lg bg-slate-900/40 border border-slate-800 text-center text-xs text-slate-500 font-sans leading-relaxed">
        <p>
          <strong className="text-slate-400">Disclaimer:</strong> SCANNAI is an educational cybercrime-awareness and decision-support prototype. Its results are indicative and are not an official determination of criminal activity, legal status or government verification.
        </p>
      </div>
    </div>
  );
};
