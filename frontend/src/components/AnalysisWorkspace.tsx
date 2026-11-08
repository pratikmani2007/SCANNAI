import React, { useState } from 'react';
import { EvidenceUpload } from './EvidenceUpload';
import { ScenarioButtons } from './ScenarioButtons';
import { DemoScenario } from '../data/scenarios';
import { Search, RotateCcw, AlertCircle, ShieldCheck, Sparkles, Loader2 } from 'lucide-react';

interface AnalysisWorkspaceProps {
  onAnalyze: (text: string, file: File | null) => Promise<void>;
  isLoading: boolean;
  error: string | null;
}

const MAX_CHARS = 50000;

export const AnalysisWorkspace: React.FC<AnalysisWorkspaceProps> = ({
  onAnalyze,
  isLoading,
  error,
}) => {
  const [messageText, setMessageText] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [activeScenarioId, setActiveScenarioId] = useState<string | undefined>();
  const [validationWarning, setValidationWarning] = useState<string | null>(null);

  const handleScenarioSelect = (scenario: DemoScenario) => {
    setMessageText(scenario.messageText);
    setActiveScenarioId(scenario.id);
    setValidationWarning(null);
  };

  const handleClear = () => {
    setMessageText('');
    setSelectedFile(null);
    setActiveScenarioId(undefined);
    setValidationWarning(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setValidationWarning(null);

    const hasText = Boolean(messageText && messageText.trim());
    const hasFile = Boolean(selectedFile);

    if (!hasText && !hasFile) {
      setValidationWarning('Please provide suspicious communication text or upload an evidence document to analyze.');
      return;
    }

    await onAnalyze(messageText, selectedFile);
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 mt-4">
      {/* 1. Quick Presets Bar */}
      <ScenarioButtons
        onSelectScenario={handleScenarioSelect}
        activeScenarioId={activeScenarioId}
        disabled={isLoading}
      />

      {/* 2. Main Analysis Card */}
      <div className="glass-panel-elevated rounded-2xl p-5 sm:p-6 border border-cyber-cardBorder shadow-2xl relative overflow-hidden">
        {/* Subtle cyan corner ambient glow */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-cyan-500/5 rounded-full blur-3xl pointer-events-none" />

        <form onSubmit={handleSubmit} className="space-y-4 relative z-10">
          {/* Card Title & Instructions */}
          <div className="flex items-center justify-between">
            <label
              htmlFor="suspicious-input"
              className="text-xs font-mono font-semibold text-slate-200 uppercase tracking-wider flex items-center space-x-2"
            >
              <Search className="w-4 h-4 text-cyan-400" />
              <span>Suspicious Communication Ingestion</span>
            </label>

            {messageText.length > 0 && (
              <button
                type="button"
                onClick={handleClear}
                disabled={isLoading}
                className="text-xs text-slate-400 hover:text-rose-400 font-mono transition-colors flex items-center space-x-1"
                title="Clear all inputs"
              >
                <RotateCcw className="w-3.5 h-3.5" />
                <span>Clear</span>
              </button>
            )}
          </div>

          {/* Large Text Area */}
          <div className="relative">
            <textarea
              id="suspicious-input"
              rows={6}
              value={messageText}
              onChange={(e) => {
                setMessageText(e.target.value);
                setValidationWarning(null);
                if (activeScenarioId) setActiveScenarioId(undefined);
              }}
              placeholder="Paste a suspicious message, SMS, email, WhatsApp conversation, video call transcript, or payment demand here..."
              maxLength={MAX_CHARS}
              disabled={isLoading}
              className="w-full bg-slate-950/90 text-slate-100 placeholder-slate-500 rounded-xl p-4 pb-8 border border-slate-800 focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 outline-none text-sm font-sans transition-all resize-y min-h-[140px]"
            />

            {/* Character Counter */}
            <div className="absolute bottom-3 right-3 text-[10px] font-mono text-slate-500 bg-slate-900/90 px-2 py-0.5 rounded border border-slate-800 pointer-events-none">
              {messageText.length.toLocaleString()} / {MAX_CHARS.toLocaleString()} chars
            </div>
          </div>

          {/* Evidence Upload Section */}
          <EvidenceUpload
            selectedFile={selectedFile}
            onFileSelect={(file) => {
              setSelectedFile(file);
              setValidationWarning(null);
            }}
            disabled={isLoading}
          />

          {/* Validation Warning */}
          {validationWarning && (
            <div className="p-3 rounded-lg bg-amber-950/70 border border-amber-800/60 flex items-center space-x-2 text-xs text-amber-300">
              <AlertCircle className="w-4 h-4 text-amber-400 flex-shrink-0" />
              <span>{validationWarning}</span>
            </div>
          )}

          {/* Backend Error Display */}
          {error && (
            <div className="p-3 rounded-lg bg-rose-950/80 border border-rose-800 flex items-center space-x-2 text-xs text-rose-300">
              <AlertCircle className="w-4 h-4 text-rose-400 flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {/* Action Row */}
          <div className="pt-2 flex flex-col sm:flex-row items-center justify-between gap-3">
            <div className="text-[11px] text-slate-400 flex items-center space-x-1.5 font-mono">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              <span>100% Deterministic Engine • Sub-15ms local response</span>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className={`w-full sm:w-auto px-6 py-3 rounded-xl font-mono text-xs font-bold uppercase tracking-wider transition-all duration-200 flex items-center justify-center space-x-2 shadow-lg ${
                isLoading
                  ? 'bg-slate-800 text-slate-500 cursor-wait'
                  : 'bg-gradient-to-r from-cyan-500 to-teal-500 hover:from-cyan-400 hover:to-teal-400 text-slate-950 shadow-cyan-500/25 hover:shadow-cyan-500/40 cursor-pointer active:scale-[0.98]'
              }`}
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin text-cyan-400" />
                  <span>EXECUTING FORENSIC RULES...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4 text-slate-950" />
                  <span>ANALYZE TRUST & PROCEDURE</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
