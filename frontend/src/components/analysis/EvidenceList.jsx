import React from 'react';
import { Search, Quote, AlertCircle, FileText } from 'lucide-react';
import { Card } from '../common/Card';

export function EvidenceList({ evidence = [], explanation = '' }) {
  const getImpactBadge = (impact = 'medium') => {
    switch (impact.toLowerCase()) {
      case 'high':
        return <span className="px-2 py-0.5 text-[10px] font-bold rounded bg-rose-500/10 text-rose-400 border border-rose-500/20 uppercase">High Impact</span>;
      case 'low':
        return <span className="px-2 py-0.5 text-[10px] font-semibold rounded bg-slate-500/10 text-slate-400 border border-slate-500/20 uppercase">Low Impact</span>;
      default:
        return <span className="px-2 py-0.5 text-[10px] font-semibold rounded bg-amber-500/10 text-amber-400 border border-amber-500/20 uppercase">Medium Impact</span>;
    }
  };

  return (
    <div className="space-y-6">
      {/* Evidence Snippet Section */}
      <Card
        title="Why the system detected this (Evidence Extraction)"
        subtitle="Interpretable phrase snippets extracted directly from student input text"
        icon={Search}
      >
        {evidence && evidence.length > 0 ? (
          <div className="space-y-3">
            {evidence.map((item, idx) => {
              const categoryLabel = (item.category || item.type || 'Signal').replace(/_/g, ' ').toUpperCase();
              return (
                <div
                  key={idx}
                  className="bg-slate-950 p-4 rounded-lg border border-slate-800 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3"
                >
                  <div className="space-y-1">
                    <span className="text-[10px] font-bold tracking-wider text-indigo-400 uppercase">
                      {categoryLabel}
                    </span>
                    <div className="flex items-center gap-2 text-sm text-slate-100 font-medium italic">
                      <Quote className="w-4 h-4 text-slate-500 shrink-0 rotate-180" />
                      <span>"{item.evidence}"</span>
                    </div>
                  </div>
                  <div className="shrink-0">{getImpactBadge(item.impact)}</div>
                </div>
              );
            })}
          </div>
        ) : (
          <p className="text-xs text-slate-500 italic text-center py-4">
            No explicit high-impact phrases extracted from input.
          </p>
        )}
      </Card>

      {/* Full NLP Explanation Card */}
      {explanation && (
        <Card
          title="Analysis Explanation"
          subtitle="System-generated explainable NLP summary"
          icon={FileText}
        >
          <div className="bg-slate-950 p-4 rounded-lg border border-slate-800/80 text-sm text-slate-300 leading-relaxed">
            {explanation}
          </div>
        </Card>
      )}
    </div>
  );
}

export default EvidenceList;
