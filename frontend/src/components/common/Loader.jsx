import React from 'react';
import { Loader2 } from 'lucide-react';

export function Loader({ text = 'Analyzing academic feedback...', className = '' }) {
  return (
    <div className={`flex flex-col items-center justify-center p-8 text-center ${className}`}>
      <div className="relative mb-3">
        <div className="w-12 h-12 rounded-full border-2 border-indigo-500/20 border-t-indigo-500 animate-spin" />
        <Loader2 className="w-6 h-6 text-indigo-400 animate-spin absolute inset-0 m-auto" />
      </div>
      <p className="text-sm font-medium text-slate-300 animate-pulse">{text}</p>
      <p className="text-xs text-slate-500 mt-1">Executing context-aware NLP pipeline</p>
    </div>
  );
}

export function Skeleton({ className = '' }) {
  return <div className={`animate-pulse bg-slate-800 rounded-md ${className}`} />;
}

export default Loader;
