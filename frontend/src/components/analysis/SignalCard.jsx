import React from 'react';
import { Activity, Gauge, Brain, Flame, UserX, BookOpen, Clock, ListFilter } from 'lucide-react';
import { Card } from '../common/Card';

const SIGNAL_METADATA = [
  { key: 'stress', label: 'Stress', icon: Gauge, color: 'bg-rose-500', textColor: 'text-rose-400' },
  { key: 'cognitive_overload', label: 'Cognitive Overload', icon: Brain, color: 'bg-indigo-500', textColor: 'text-indigo-400' },
  { key: 'workload_difficulty', label: 'Workload Difficulty', icon: BookOpen, color: 'bg-cyan-500', textColor: 'text-cyan-400' },
  { key: 'time_pressure', label: 'Time Pressure', icon: Clock, color: 'bg-amber-500', textColor: 'text-amber-400' },
  { key: 'choice_overload', label: 'Choice / Priority Difficulty', icon: ListFilter, color: 'bg-purple-500', textColor: 'text-purple-400' },
  { key: 'frustration', label: 'Frustration', icon: Flame, color: 'bg-orange-500', textColor: 'text-orange-400' },
  { key: 'disengagement', label: 'Disengagement', icon: UserX, color: 'bg-slate-500', textColor: 'text-slate-400' },
];

export function SignalCard({ signals = {} }) {
  return (
    <Card
      title="Academic Experience Signals"
      subtitle="Contextual distress and workload dimensions normalized between 0% and 100%."
      icon={Activity}
    >
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {SIGNAL_METADATA.map((sig) => {
          const rawScore = signals[sig.key] || 0.0;
          const percentage = Math.round(rawScore * 100);
          const Icon = sig.icon;

          return (
            <div
              key={sig.key}
              className="bg-slate-950 p-4 rounded-lg border border-slate-800/80 space-y-2 hover:border-slate-700 transition-colors"
            >
              <div className="flex justify-between items-center text-xs">
                <span className="font-semibold text-slate-200 flex items-center gap-2">
                  <Icon className={`w-4 h-4 ${sig.textColor}`} /> {sig.label}
                </span>
                <span className={`font-bold ${sig.textColor}`}>{percentage}%</span>
              </div>

              {/* Accessible Progress Bar */}
              <div
                className="w-full bg-slate-800 rounded-full h-2 overflow-hidden"
                role="progressbar"
                aria-valuenow={percentage}
                aria-valuemin={0}
                aria-valuemax={100}
                aria-label={`${sig.label} level ${percentage}%`}
              >
                <div
                  className={`h-full ${sig.color} transition-all duration-500 rounded-full`}
                  style={{ width: `${percentage}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </Card>
  );
}

export default SignalCard;
