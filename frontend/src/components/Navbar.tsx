import React from 'react';
import { Shield, ShieldAlert, Cpu, ExternalLink } from 'lucide-react';
import { HealthResponse } from '../types/analysis';

interface NavbarProps {
  health: HealthResponse | null;
  healthLoading: boolean;
  healthError: string | null;
  onRefreshHealth: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  health,
  healthLoading,
  healthError,
  onRefreshHealth,
}) => {
  const isOnline = health?.status === 'healthy';
  const apiBase = import.meta.env.VITE_API_BASE_URL || '';
  const docsUrl = apiBase ? `${apiBase.replace(/\/$/, '')}/docs` : '/docs';

  return (
    <header className="border-b border-cyber-cardBorder bg-cyber-surface/80 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Product Identity */}
          <div className="flex items-center space-x-3">
            <div className="relative flex items-center justify-center w-10 h-10 rounded-lg bg-cyber-card border border-cyan-500/30 text-cyan-400 shadow-lg shadow-cyan-500/10">
              <Shield className="w-6 h-6 text-cyan-400" />
              <div className="absolute inset-0 rounded-lg bg-cyan-400/10 blur-sm pointer-events-none" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-xl font-bold tracking-wider text-white font-mono">
                  SCANNAI
                </span>
                <span className="text-[10px] uppercase tracking-widest px-1.5 py-0.5 rounded font-mono font-semibold bg-cyan-950/80 text-cyan-300 border border-cyan-800/60">
                  v0.1.0-DEMO
                </span>
              </div>
              <p className="text-xs text-cyber-muted hidden sm:block">
                Cybercrime & Scam Awareness Intelligence • <span className="text-cyan-400/90 font-medium">Team ROCKERZ</span>
              </p>
            </div>
          </div>

          {/* Right Status Group */}
          <div className="flex items-center space-x-3">
            {/* System Online / Connection Error Indicator */}
            <button
              onClick={onRefreshHealth}
              title="Click to re-verify backend engine connection"
              className={`flex items-center space-x-2 px-3 py-1.5 rounded-full text-xs font-mono font-medium border transition-all duration-200 ${
                healthLoading
                  ? 'bg-slate-900 border-slate-700 text-slate-400'
                  : isOnline
                  ? 'bg-emerald-950/60 border-emerald-700/50 text-emerald-300 shadow-sm shadow-emerald-900/30 hover:border-emerald-500'
                  : 'bg-rose-950/60 border-rose-700/50 text-rose-300 shadow-sm shadow-rose-900/30 hover:border-rose-500'
              }`}
            >
              {healthLoading ? (
                <>
                  <div className="w-2 h-2 rounded-full bg-slate-400 animate-ping" />
                  <span>PROBING ENGINE...</span>
                </>
              ) : isOnline ? (
                <>
                  <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                  <span className="tracking-wide">SYSTEM ONLINE</span>
                  <span className="text-[10px] text-emerald-400/70 hidden md:inline">
                    (DETERMINISTIC)
                  </span>
                </>
              ) : (
                <>
                  <ShieldAlert className="w-3.5 h-3.5 text-rose-400" />
                  <span className="tracking-wide">CONNECTION ERROR</span>
                </>
              )}
            </button>

            {/* Offline Engine Badge */}
            <div className="hidden lg:flex items-center space-x-1 px-2.5 py-1 rounded bg-slate-900/90 border border-slate-800 text-[11px] font-mono text-slate-300">
              <Cpu className="w-3 h-3 text-cyan-400" />
              <span>DETERMINISTIC KNOWLEDGE BASE</span>
            </div>

            {/* OpenAPI Docs Link */}
            <a
              href={docsUrl}
              target="_blank"
              rel="noreferrer"
              className="text-slate-400 hover:text-cyan-300 transition-colors p-1.5 rounded hover:bg-slate-800/60 flex items-center text-xs space-x-1"
              title="Open OpenAPI/Swagger Documentation"
            >
              <span className="hidden sm:inline font-mono">API Docs</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </div>
        </div>
      </div>
      {/* If error, display prominent warning bar */}
      {healthError && (
        <div className="bg-rose-950/90 border-t border-rose-800/60 px-4 py-1.5 text-center text-xs text-rose-300 flex items-center justify-center space-x-2">
          <ShieldAlert className="w-3.5 h-3.5 text-rose-400" />
          <span>Backend not reachable{apiBase ? ` at ${apiBase}` : ''}. Please ensure the SCANNAI backend service is running.</span>
        </div>
      )}
    </header>
  );
};
