import React from 'react';
import { Layers, CheckCircle2, XCircle } from 'lucide-react';
import { Card } from '../common/Card';

const CATEGORY_MAP = [
  { key: 'workload_pressure', label: 'Workload Pressure' },
  { key: 'time_pressure', label: 'Time Pressure' },
  { key: 'cognitive_load', label: 'Cognitive Load' },
  { key: 'choice_difficulty', label: 'Choice / Priority Difficulty' },
  { key: 'frustration', label: 'Frustration' },
  { key: 'disengagement', label: 'Disengagement' },
];

export function AcademicContext({ academicContext = {} }) {
  return (
    <Card
      title="Academic Context Dimensions"
      subtitle="Detected structural academic indicators"
      icon={Layers}
    >
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
        {CATEGORY_MAP.map((cat) => {
          const isActive = Boolean(academicContext[cat.key]);
          return (
            <div
              key={cat.key}
              className={`p-3 rounded-lg border flex items-center justify-between text-xs font-medium transition-all ${
                isActive
                  ? 'bg-indigo-500/10 text-indigo-300 border-indigo-500/30 font-semibold'
                  : 'bg-slate-950 text-slate-500 border-slate-800 opacity-60'
              }`}
            >
              <span>{cat.label}</span>
              {isActive ? (
                <CheckCircle2 className="w-4 h-4 text-indigo-400 shrink-0 ml-1.5" />
              ) : (
                <XCircle className="w-4 h-4 text-slate-600 shrink-0 ml-1.5" />
              )}
            </div>
          );
        })}
      </div>
    </Card>
  );
}

export default AcademicContext;
