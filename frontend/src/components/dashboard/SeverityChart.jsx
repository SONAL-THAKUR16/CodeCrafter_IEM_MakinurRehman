import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { ShieldAlert } from 'lucide-react';
import { Card } from '../common/Card';

const COLORS = {
  LOW: '#10b981',      // Emerald-500
  MODERATE: '#f59e0b', // Amber-500
  HIGH: '#f43f5e'      // Rose-500
};

export function SeverityChart({ distribution = {} }) {
  const data = [
    { name: 'Low', value: distribution.LOW || 0, severity: 'LOW' },
    { name: 'Moderate', value: distribution.MODERATE || 0, severity: 'MODERATE' },
    { name: 'High', value: distribution.HIGH || 0, severity: 'HIGH' }
  ].filter(item => item.value > 0);

  const total = Object.values(distribution).reduce((a, b) => a + b, 0);

  return (
    <Card
      title="Severity Distribution"
      subtitle={`Overall academic distress distribution across ${total} records`}
      icon={ShieldAlert}
    >
      {total > 0 ? (
        <div className="h-[220px] w-full pt-2">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                innerRadius={50}
                outerRadius={80}
                paddingAngle={4}
                dataKey="value"
              >
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[entry.severity]} stroke="#0f172a" strokeWidth={2} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#f8fafc' }}
                formatter={(val) => [`${val} analyses`, 'Count']}
              />
              <Legend
                verticalAlign="bottom"
                height={36}
                formatter={(value) => <span className="text-xs text-slate-300 font-medium">{value}</span>}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
      ) : (
        <div className="h-[220px] flex items-center justify-center text-xs text-slate-500 italic">
          No severity data recorded yet.
        </div>
      )}
    </Card>
  );
}

export default SeverityChart;
