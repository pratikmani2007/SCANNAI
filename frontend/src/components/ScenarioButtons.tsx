import React from 'react';
import { DEMO_SCENARIOS, DemoScenario } from '../data/scenarios';
import { ShieldAlert, Scale, CreditCard, ShoppingBag, PackageX, Play } from 'lucide-react';

interface ScenarioButtonsProps {
  onSelectScenario: (scenario: DemoScenario) => void;
  activeScenarioId?: string;
  disabled?: boolean;
}

export const ScenarioButtons: React.FC<ScenarioButtonsProps> = ({
  onSelectScenario,
  activeScenarioId,
  disabled = false,
}) => {
  const getIcon = (id: string) => {
    switch (id) {
      case 'digital-arrest':
        return <ShieldAlert className="w-4 h-4 text-rose-400" />;
      case 'legitimate-ecourts':
        return <Scale className="w-4 h-4 text-emerald-400" />;
      case 'fraudulent-upi-clearance':
        return <CreditCard className="w-4 h-4 text-amber-400" />;
      case 'legitimate-commercial-upi':
        return <ShoppingBag className="w-4 h-4 text-emerald-400" />;
      case 'customs-ncb-extortion':
        return <PackageX className="w-4 h-4 text-rose-400" />;
      default:
        return <Play className="w-4 h-4 text-cyan-400" />;
    }
  };

  const getBadgeStyle = (category: DemoScenario['category']) => {
    switch (category) {
      case 'EXTORTION':
        return 'bg-rose-950/70 text-rose-300 border-rose-800/60';
      case 'BANKING':
        return 'bg-amber-950/70 text-amber-300 border-amber-800/60';
      case 'OFFICIAL':
      case 'COMMERCIAL':
        return 'bg-emerald-950/70 text-emerald-300 border-emerald-800/60';
    }
  };

  return (
    <div className="mb-6">
      <div className="flex items-center justify-between mb-2.5">
        <div className="flex items-center space-x-2">
          <span className="text-xs font-mono font-semibold text-slate-300 uppercase tracking-wider">
            Quick Demonstration Presets (1-Click Test Cases)
          </span>
          <span className="text-[11px] text-slate-500 hidden sm:inline">
            — Loads authentic test scenarios directly into the analyzer
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-2.5">
        {DEMO_SCENARIOS.map((scenario) => {
          const isActive = activeScenarioId === scenario.id;
          return (
            <button
              key={scenario.id}
              onClick={() => onSelectScenario(scenario)}
              disabled={disabled}
              className={`p-3 rounded-lg border text-left transition-all duration-200 relative group flex flex-col justify-between ${
                isActive
                  ? 'bg-slate-800/90 border-cyan-500/80 shadow-md shadow-cyan-950/40 ring-1 ring-cyan-500/50'
                  : 'bg-cyber-surface/70 border-slate-800 hover:border-slate-700 hover:bg-slate-800/50'
              } ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
            >
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <div className="p-1 rounded bg-slate-900 border border-slate-800">
                    {getIcon(scenario.id)}
                  </div>
                  <span
                    className={`text-[9px] font-mono px-1.5 py-0.5 rounded border uppercase font-medium ${getBadgeStyle(
                      scenario.category
                    )}`}
                  >
                    {scenario.category}
                  </span>
                </div>
                <h4 className="text-xs font-semibold text-white tracking-tight group-hover:text-cyan-300 transition-colors break-words">
                  {scenario.title}
                </h4>
                <p className="text-[11px] text-slate-400 mt-0.5 line-clamp-2 leading-tight break-words">
                  {scenario.subtitle}
                </p>
              </div>

              <div className="mt-2.5 pt-2 border-t border-slate-800/60 flex items-center justify-between text-[10px] text-slate-400 font-mono">
                <span className="text-cyan-400/90 font-medium flex items-center space-x-1 group-hover:translate-x-0.5 transition-transform">
                  <span>Load Preset</span>
                  <span>→</span>
                </span>
                {isActive && (
                  <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-pulse" />
                )}
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
};
