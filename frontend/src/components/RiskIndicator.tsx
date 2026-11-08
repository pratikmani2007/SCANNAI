import React from 'react';
import { RiskClassification, ConfidenceLevel } from '../types/analysis';
import { ShieldCheck, AlertTriangle, ShieldAlert } from 'lucide-react';

interface RiskIndicatorProps {
  score: number;
  classification: RiskClassification;
  confidence: ConfidenceLevel;
}

export const RiskIndicator: React.FC<RiskIndicatorProps> = ({
  score,
  classification,
  confidence,
}) => {
  // Clamp score cleanly between 0 and 100
  const normalizedScore = Math.max(0, Math.min(100, score));

  // Determine color and styling based strictly on classification
  const getTheme = () => {
    switch (classification) {
      case 'LOW RISK':
        return {
          textColor: 'text-emerald-400',
          bgColor: 'bg-emerald-950/50',
          borderColor: 'border-emerald-700/60',
          glowClass: 'glow-green',
          progressColor: 'bg-emerald-500',
          ringColor: '#10b981',
          icon: <ShieldCheck className="w-6 h-6 text-emerald-400" />,
          badgeBg: 'bg-emerald-950 text-emerald-300 border-emerald-700',
        };
      case 'NEEDS VERIFICATION':
        return {
          textColor: 'text-amber-400',
          bgColor: 'bg-amber-950/50',
          borderColor: 'border-amber-700/60',
          glowClass: 'glow-amber',
          progressColor: 'bg-amber-500',
          ringColor: '#f59e0b',
          icon: <AlertTriangle className="w-6 h-6 text-amber-400" />,
          badgeBg: 'bg-amber-950 text-amber-300 border-amber-700',
        };
      case 'HIGH RISK':
      default:
        return {
          textColor: 'text-rose-400',
          bgColor: 'bg-rose-950/50',
          borderColor: 'border-rose-700/60',
          glowClass: 'glow-red',
          progressColor: 'bg-rose-500',
          ringColor: '#ef4444',
          icon: <ShieldAlert className="w-6 h-6 text-rose-400" />,
          badgeBg: 'bg-rose-950 text-rose-300 border-rose-700',
        };
    }
  };

  const theme = getTheme();

  // SVG Circular Gauge calculation
  const radius = 42;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (normalizedScore / 100) * circumference;

  return (
    <div
      className={`p-5 rounded-xl border ${theme.bgColor} ${theme.borderColor} ${theme.glowClass} transition-all duration-300`}
    >
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
        {/* Left: Circular Score Gauge */}
        <div className="flex items-center space-x-4">
          <div className="relative w-24 h-24 flex items-center justify-center flex-shrink-0">
            <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
              {/* Background circle */}
              <circle
                cx="50"
                cy="50"
                r={radius}
                className="stroke-slate-800"
                strokeWidth="8"
                fill="transparent"
              />
              {/* Animated Progress Circle */}
              <circle
                cx="50"
                cy="50"
                r={radius}
                stroke={theme.ringColor}
                strokeWidth="8"
                strokeDasharray={circumference}
                strokeDashoffset={strokeDashoffset}
                strokeLinecap="round"
                fill="transparent"
                className="transition-all duration-700 ease-out"
              />
            </svg>

            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className={`text-2xl font-mono font-extrabold ${theme.textColor}`}>
                {normalizedScore}
              </span>
              <span className="text-[10px] text-slate-400 font-mono -mt-1">/ 100</span>
            </div>
          </div>

          <div>
            <div className="flex items-center space-x-2">
              <div className="p-1 rounded bg-slate-900/80 border border-slate-800">
                {theme.icon}
              </div>
              <h3 className={`text-xl font-bold tracking-tight ${theme.textColor}`}>
                {classification}
              </h3>
            </div>
            <p className="text-xs text-slate-300 mt-1 max-w-sm">
              {classification === 'HIGH RISK' &&
                'Procedural coercion or statutory fallacies detected. Strong indications of fraudulent extortion.'}
              {classification === 'NEEDS VERIFICATION' &&
                'Unverified claims or isolated urgency markers detected. Independent verification required.'}
              {classification === 'LOW RISK' &&
                'Standard communication patterns observed. No recognized procedural fallacy triggers.'}
            </p>
          </div>
        </div>

        {/* Right: Confidence Badge & Scale Overview */}
        <div className="flex flex-col items-center sm:items-end justify-center space-y-2 w-full sm:w-auto text-center sm:text-right">
          <div className="flex items-center space-x-2">
            <span className="text-xs text-slate-400 font-mono">Confidence:</span>
            <span
              className={`text-xs font-mono font-semibold px-2 py-0.5 rounded border ${theme.badgeBg}`}
            >
              {confidence} CONFIDENCE
            </span>
          </div>

          {/* Scale Legend */}
          <div className="w-full sm:w-48 bg-slate-900/90 rounded-md p-2 border border-slate-800 text-[10px] font-mono space-y-1">
            <div className="flex justify-between text-slate-400">
              <span>Risk Thresholds:</span>
            </div>
            <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden flex">
              <div className="w-[34%] bg-emerald-500" title="Low Risk: 0-34" />
              <div className="w-[35%] bg-amber-500" title="Needs Verification: 35-69" />
              <div className="w-[31%] bg-rose-500" title="High Risk: 70-100" />
            </div>
            <div className="flex justify-between text-[9px] text-slate-500">
              <span className="text-emerald-400">0–34</span>
              <span className="text-amber-400">35–69</span>
              <span className="text-rose-400">70–100</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
