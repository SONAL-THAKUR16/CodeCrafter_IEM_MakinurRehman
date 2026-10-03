import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { BarChart3 } from 'lucide-react';
import { Card } from '../common/Card';

export function SignalChart({ summary }) {
  if (!summary) return null;

  const data = [
    { category: 'Workload', score: Math.round((summary.average_workload_difficulty || 0) * 100), fill: '#06b6d4' },
    { category: 'Stress', score: Math.round((summary.average_stress || 0) * 100), fill: '#f43f5e' },
    { category: 'Overload', score: Math.round((summary.average_cognitive_overload || 0) * 100), fill: '#6366f1' },
    { category: 'Time', score: Math.round((summary.average_time_pressure || 0) * 100), fill: '#f59e0b' },
    { category: 'Choice', score: Math.round((summary.average_choice_overload || 0) * 100), fill: '#a855f7' },
    { category: 'Frustration', score: Math.round((summary.average_frustration || 0) * 100), fill: '#f97316' },
    { category: 'Disengage', score: Math.round((summary.average_disengagement || 0) * 100), fill: '#64748b' }
  ];

  return (
    <Card
      title="Signal Comparison Averages"
      subtitle="Average score percentages across academic experience dimensions"
      icon={BarChart3}
    >
      <div className="h-[220px] w-full pt-2">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <XAxis dataKey="category" tick={{ fill: '#94a3b8', fontSize: 11 }} />
            <YAxis domain={[0, 100]} tick={{ fill: '#94a3b8', fontSize: 11 }} unit="%" />
            <Tooltip
              contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#f8fafc' }}
              formatter={(val) => [`${val}%`, 'Average Level']}
            />
            <Bar dataKey="score" radius={[4, 4, 0, 0]}>
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.fill} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}

export default SignalChart;
