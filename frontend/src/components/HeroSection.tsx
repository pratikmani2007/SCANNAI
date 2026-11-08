import React from 'react';
import { Lock, FileCheck, ShieldCheck } from 'lucide-react';

export const HeroSection: React.FC = () => {
  return (
    <section className="relative pt-8 pb-6 px-4 sm:px-6 lg:px-8 text-center max-w-4xl mx-auto">
      {/* Small Badge */}
      <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-cyan-950/70 border border-cyan-700/60 text-cyan-300 text-xs font-mono font-medium tracking-wide mb-4 shadow-sm shadow-cyan-950">
        <Lock className="w-3.5 h-3.5 text-cyan-400" />
        <span>DETERMINISTIC • OFFLINE ANALYSIS</span>
      </div>

      {/* Main Heading */}
      <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-white tracking-tight mb-4">
        Think Before You <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-teal-300 to-cyan-500">Trust.</span>
      </h1>

      {/* Supporting Text */}
      <p className="text-base sm:text-lg text-slate-300 max-w-2xl mx-auto leading-relaxed mb-6">
        Analyze suspicious messages, identify procedural red flags, and understand your next steps before responding to potential scams.
      </p>

      {/* Value Pillars */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 max-w-3xl mx-auto text-left">
        <div className="p-3 rounded-lg bg-cyber-surface/60 border border-slate-800/80 backdrop-blur-sm">
          <div className="flex items-center space-x-2 text-cyan-400 text-xs font-mono font-semibold mb-1">
            <FileCheck className="w-3.5 h-3.5" />
            <span>STATUTORY CITATIONS</span>
          </div>
          <p className="text-[12px] text-slate-400 leading-snug">
            Evaluated against official BNSS 2023, RBI, TRAI, and CBIC procedural safeguards.
          </p>
        </div>

        <div className="p-3 rounded-lg bg-cyber-surface/60 border border-slate-800/80 backdrop-blur-sm">
          <div className="flex items-center space-x-2 text-emerald-400 text-xs font-mono font-semibold mb-1">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>FALSE-POSITIVE SHIELD</span>
          </div>
          <p className="text-[12px] text-slate-400 leading-snug">
            Contextual filtering shields legitimate e-Courts notices, bank OTPs, and everyday billing.
          </p>
        </div>

        <div className="p-3 rounded-lg bg-cyber-surface/60 border border-slate-800/80 backdrop-blur-sm">
          <div className="flex items-center space-x-2 text-teal-400 text-xs font-mono font-semibold mb-1">
            <Lock className="w-3.5 h-3.5" />
            <span>ZERO CLOUD LEAKAGE</span>
          </div>
          <p className="text-[12px] text-slate-400 leading-snug">
            No cloud APIs or third-party servers. All evidence analyzed strictly in local memory.
          </p>
        </div>
      </div>
    </section>
  );
};
