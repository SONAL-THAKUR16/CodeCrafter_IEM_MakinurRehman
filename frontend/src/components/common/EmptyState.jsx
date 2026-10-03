import React from 'react';
import { Inbox } from 'lucide-react';

export function EmptyState({
  title = 'No Data Available',
  description = 'Analyze your first student response to begin.',
  icon: Icon = Inbox,
  action,
}) {
  return (
    <div className="flex flex-col items-center justify-center p-8 text-center bg-slate-900/50 border border-dashed border-slate-800 rounded-xl">
      <div className="p-3 bg-slate-800/80 rounded-full mb-3 text-slate-400">
        <Icon className="w-6 h-6" />
      </div>
      <h4 className="text-sm font-semibold text-slate-200">{title}</h4>
      <p className="text-xs text-slate-400 max-w-sm mt-1 mb-4 leading-relaxed">{description}</p>
      {action}
    </div>
  );
}

export default EmptyState;
