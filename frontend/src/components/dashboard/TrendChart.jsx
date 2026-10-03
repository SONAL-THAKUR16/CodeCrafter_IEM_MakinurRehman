import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { TrendingUp } from 'lucide-react';
import { Card } from '../common/Card';

export function TrendChart({ trends = [] }) {
  if (!trends || trends.length === 0) {
    return (
      <Card title="Distress Trends Over Time" subtitle="Time-series tracking of student feedback signals" icon={TrendingUp}>
        <div className="h-[220px] flex items-center justify-center text-xs text-slate-500 italic">
          No historical trend points recorded yet.
        </div>
      </Card>
    );
  }

  const chartData = trends.map((t, idx) => ({
    time: `T${idx + 1}`,
    Stress: Math.round((t.stress || 0) * 100),
    Workload: Math.round((t.workload_difficulty || 0) * 100),
    CognitiveOverload: Math.round((t.cognitive_overload || 0) * 100)
  }));

  return (
    <Card
      title="Distress Trends Over Time"
      subtitle="Time-series progression of stress, workload, and cognitive overload"
      icon={TrendingUp}
    >
      <div className="h-[220px] w-full pt-2">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <XAxis dataKey="time" tick={{ fill: '#94a3b8', fontSize: 11 }} />
            <YAxis domain={[0, 100]} tick={{ fill: '#94a3b8', fontSize: 11 }} unit="%" />
            <Tooltip
              contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#f8fafc' }}
              formatter={(val) => [`${val}%`]}
            />
            <Legend
              verticalAlign="top"
              height={36}
              formatter={(value) => <span className="text-xs text-slate-300 font-medium">{value}</span>}
            />
            <Line type="monotone" dataKey="Stress" stroke="#f43f5e" strokeWidth={2} dot={{ r: 3 }} />
            <Line type="monotone" dataKey="Workload" stroke="#06b6d4" strokeWidth={2} dot={{ r: 3 }} />
            <Line type="monotone" dataKey="CognitiveOverload" stroke="#6366f1" strokeWidth={2} dot={{ r: 3 }} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}

export default TrendChart;
