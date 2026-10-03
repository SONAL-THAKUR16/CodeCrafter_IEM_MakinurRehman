import React from 'react';
import { Database, Gauge, Brain, BookOpen, Target } from 'lucide-react';

export function SummaryCards({ summary }) {
  if (!summary) return null;

  const cards = [
    {
      label: 'Total Analyses',
      value: summary.total_analyses || 0,
      icon: Database,
      textColor: 'text-indigo-400',
      bgColor: 'bg-indigo-500/10'
    },
    {
      label: 'Average Stress',
      value: `${Math.round((summary.average_stress || 0) * 100)}%`,
      icon: Gauge,
      textColor: 'text-rose-400',
      bgColor: 'bg-rose-500/10'
    },
    {
      label: 'Average Cognitive Overload',
      value: `${Math.round((summary.average_cognitive_overload || 0) * 100)}%`,
      icon: Brain,
      textColor: 'text-indigo-400',
      bgColor: 'bg-indigo-500/10'
    },
    {
      label: 'Average Workload Difficulty',
      value: `${Math.round((summary.average_workload_difficulty || 0) * 100)}%`,
      icon: BookOpen,
      textColor: 'text-cyan-400',
      bgColor: 'bg-cyan-500/10'
    },
    {
      label: 'Most Common Concern',
      value: (summary.most_common_concern || 'none').replace(/_/g, ' ').toUpperCase(),
      icon: Target,
      textColor: 'text-amber-400',
      bgColor: 'bg-amber-500/10'
    }
  ];

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
      {cards.map((card, idx) => {
        const Icon = card.icon;
        return (
          <div
            key={idx}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col justify-between space-y-2 hover:border-slate-700 transition-colors shadow-md"
          >
            <div className="flex justify-between items-center text-xs text-slate-400 font-medium">
              <span>{card.label}</span>
              <div className={`p-1.5 rounded-lg ${card.bgColor} ${card.textColor}`}>
                <Icon className="w-4 h-4" />
              </div>
            </div>
            <div className={`text-xl font-bold ${card.textColor} tracking-tight`}>
              {card.value}
            </div>
          </div>
        );
      })}
    </div>
  );
}

export default SummaryCards;
