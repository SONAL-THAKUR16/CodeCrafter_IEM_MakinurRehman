import React from 'react';
import { Brain, Activity, Code2, School } from 'lucide-react';

export function Navbar({ healthStatus = 'checking' }) {
  const getStatusBadge = () => {
    if (healthStatus === 'online') {
      return (
        <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          Analysis Engine Online
        </span>
      );
    } else if (healthStatus === 'offline') {
      return (
        <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-rose-500/10 text-rose-400 border border-rose-500/20">
          <span className="w-2 h-2 rounded-full bg-rose-400" />
          Engine Offline (Check Backend)
        </span>
      );
    }
    return (
      <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-amber-500/10 text-amber-400 border border-amber-500/20">
        <span className="w-2 h-2 rounded-full bg-amber-400 animate-ping" />
        Connecting Engine...
      </span>
    );
  };

  return (
    <header className="sticky top-0 z-40 bg-slate-950/90 backdrop-blur-md border-b border-slate-800/80 px-4 lg:px-8 py-3.5">
      <div className="max-w-7xl mx-auto flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-gradient-to-br from-indigo-600 to-indigo-800 rounded-xl shadow-lg shadow-indigo-500/20 border border-indigo-500/30">
            <Brain className="w-6 h-6 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold tracking-tight text-white">EduSense AI</h1>
              <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 uppercase tracking-wide">
                Hackathon MVP
              </span>
            </div>
            <p className="text-xs text-slate-400">Context-aware analysis of student academic experiences</p>
          </div>
        </div>

        <div className="flex items-center gap-4 text-xs text-slate-400 shrink-0">
          <div className="hidden md:flex items-center gap-3 border-r border-slate-800 pr-4">
            <span className="flex items-center gap-1.5 text-slate-300">
              <Code2 className="w-3.5 h-3.5 text-indigo-400" /> CodeCrafter
            </span>
            <span className="flex items-center gap-1.5 text-slate-400">
              <School className="w-3.5 h-3.5 text-cyan-400" /> IEM
            </span>
          </div>
          {getStatusBadge()}
        </div>
      </div>
    </header>
  );
}

export default Navbar;
