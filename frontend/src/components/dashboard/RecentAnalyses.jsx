import React from 'react';
import { History, ArrowRight, Clock, Target } from 'lucide-react';
import { Card } from '../common/Card';
import { SeverityBadge } from '../analysis/SeverityBadge';

export function RecentAnalyses({ items = [], onSelectAnalysis, loading }) {
  if (loading) {
    return (
      <Card title="Recent Analysis History" subtitle="Fetching recent feedback sessions..." icon={History}>
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="animate-pulse bg-slate-950 p-4 rounded-lg border border-slate-800 h-16" />
          ))}
        </div>
      </Card>
    );
  }

  if (!items || items.length === 0) {
    return (
      <Card title="Recent Analysis History" subtitle="Stored student feedback analysis history" icon={History}>
        <p className="text-xs text-slate-500 italic text-center py-6">
          No analysis history found. Submit student feedback to populate history.
        </p>
      </Card>
    );
  }

  return (
    <Card
      title="Recent Analysis History"
      subtitle={`Showing ${items.length} recent student feedback sessions (Click any session to inspect details)`}
      icon={History}
    >
      <div className="space-y-3">
        {items.map((item) => {
          const formattedTime = item.created_at
            ? new Date(item.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            : 'Recent';

          const formattedDate = item.created_at
            ? new Date(item.created_at).toLocaleDateString([], { month: 'short', day: 'numeric' })
            : '';

          return (
            <button
              key={item.analysis_id}
              type="button"
              onClick={() => onSelectAnalysis(item.analysis_id)}
              className="w-full text-left bg-slate-950 hover:bg-slate-800/80 p-4 rounded-lg border border-slate-800/80 hover:border-indigo-500/50 transition-all flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 group cursor-pointer"
            >
              <div className="space-y-1 min-w-0 flex-1">
                <div className="flex items-center gap-2">
                  <span className="text-xs text-slate-400 font-mono flex items-center gap-1">
                    <Clock className="w-3 h-3 text-slate-500" /> {formattedDate} {formattedTime}
                  </span>
                  <span className="text-slate-600">&bull;</span>
                  <span className="text-xs text-indigo-300 font-medium flex items-center gap-1">
                    <Target className="w-3 h-3 text-indigo-400" />
                    {(item.primary_concern || 'none').replace(/_/g, ' ')}
                  </span>
                </div>
                <p className="text-sm font-medium text-slate-200 group-hover:text-indigo-200 transition-colors truncate">
                  "{item.text_snippet || 'Student academic feedback'}"
                </p>
              </div>

              <div className="flex items-center gap-3 shrink-0 self-end sm:self-auto">
                <div className="text-right text-xs text-slate-400 hidden sm:block">
                  <div>Stress: <strong className="text-slate-200">{Math.round((item.stress || 0) * 100)}%</strong></div>
                  <div>Workload: <strong className="text-slate-200">{Math.round((item.workload_difficulty || 0) * 100)}%</strong></div>
                </div>
                <SeverityBadge severity={item.overall_severity} size="sm" />
                <ArrowRight className="w-4 h-4 text-slate-500 group-hover:text-indigo-400 group-hover:translate-x-1 transition-all" />
              </div>
            </button>
          );
        })}
      </div>
    </Card>
  );
}

export default RecentAnalyses;
