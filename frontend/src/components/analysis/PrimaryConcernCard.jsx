import React from 'react';
import { Target, Lightbulb, Info } from 'lucide-react';
import { SeverityBadge } from './SeverityBadge';

export function PrimaryConcernCard({
  overallSeverity,
  severityReason,
  primaryConcern,
  studentInsight,
  disclaimer
}) {
  const concernLabel = primaryConcern?.label
    ? primaryConcern.label.replace(/_/g, ' ').toUpperCase()
    : 'NONE';

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-lg space-y-6">
      {/* Severity & Primary Concern Row */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 pb-5 border-b border-slate-800">
        <div>
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1">
            Overall Experience Rating
          </span>
          <SeverityBadge severity={overallSeverity} size="lg" />
        </div>

        <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 md:text-right w-full md:w-auto min-w-[220px]">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center md:justify-end gap-1.5 mb-1">
            <Target className="w-3.5 h-3.5 text-indigo-400" /> Primary Concern
          </span>
          <div className="text-base font-bold text-white tracking-wide">
            {concernLabel}
          </div>
          {primaryConcern?.score > 0 && (
            <span className="text-xs text-indigo-400 font-medium">
              Signal Score: {Math.round(primaryConcern.score * 100)}%
            </span>
          )}
        </div>
      </div>

      {/* Severity Reason & Student Insight */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {severityReason && (
          <div className="bg-slate-950/70 p-4 rounded-lg border border-slate-800/80">
            <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5 mb-1.5">
              <Info className="w-3.5 h-3.5 text-cyan-400" /> Severity Assessment
            </h4>
            <p className="text-xs text-slate-300 leading-relaxed">{severityReason}</p>
          </div>
        )}

        {studentInsight && (
          <div className="bg-slate-950/70 p-4 rounded-lg border border-slate-800/80">
            <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5 mb-1.5">
              <Lightbulb className="w-3.5 h-3.5 text-amber-400" /> Student Insight
            </h4>
            <p className="text-xs text-slate-300 leading-relaxed">{studentInsight}</p>
          </div>
        )}
      </div>

      {/* Medical Disclaimer */}
      {disclaimer && (
        <div className="text-[11px] text-slate-500 bg-slate-950/50 p-3 rounded-md border border-slate-800/50 italic text-center">
          {disclaimer}
        </div>
      )}
    </div>
  );
}

export default PrimaryConcernCard;
