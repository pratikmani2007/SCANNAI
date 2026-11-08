import React from 'react';
import { Shield, ExternalLink, PhoneCall } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="mt-16 border-t border-slate-800 bg-cyber-surface/90 py-8 px-4 sm:px-6 lg:px-8 text-xs text-slate-400 font-sans">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
        {/* Brand & Team */}
        <div className="flex items-center space-x-3 text-center md:text-left">
          <div className="p-2 rounded bg-slate-900 border border-slate-800 text-cyan-400">
            <Shield className="w-5 h-5" />
          </div>
          <div>
            <div className="text-white font-mono font-bold tracking-wider">
              SCANNAI <span className="text-cyan-400 text-xs font-normal">| Team ROCKERZ</span>
            </div>
            <p className="text-[11px] text-slate-500 mt-0.5">
              AI-Powered Financial Communication Trust-Verification System
            </p>
          </div>
        </div>

        {/* Emergency Resources Quick Links */}
        <div className="flex flex-wrap items-center justify-center gap-3 font-mono text-[11px]">
          <a
            href="https://cybercrime.gov.in"
            target="_blank"
            rel="noreferrer"
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded bg-slate-900 border border-slate-800 hover:border-cyan-500 text-slate-300 hover:text-cyan-300 transition-colors"
          >
            <span>National Cybercrime Portal</span>
            <ExternalLink className="w-3 h-3" />
          </a>

          <a
            href="tel:1930"
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded bg-rose-950/60 border border-rose-800/60 text-rose-300 hover:border-rose-600 transition-colors"
          >
            <PhoneCall className="w-3 h-3 text-rose-400" />
            <span>National Helpline: 1930</span>
          </a>

          <a
            href="https://sancharsaathi.gov.in"
            target="_blank"
            rel="noreferrer"
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded bg-slate-900 border border-slate-800 hover:border-cyan-500 text-slate-300 hover:text-cyan-300 transition-colors"
          >
            <span>DoT Sanchar Saathi</span>
            <ExternalLink className="w-3 h-3" />
          </a>
        </div>
      </div>

      <div className="max-w-7xl mx-auto mt-6 pt-4 border-t border-slate-800/60 text-center text-[10px] text-slate-500 font-mono">
        Educational Cyber-Forensic Research Prototype • Built for Preliminary Inter-College Selection Round • 100% Offline Rule Engine
      </div>
    </footer>
  );
};
