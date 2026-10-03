import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

const data = [
  { name: "Mon", stress: 65, overload: 72 },
  { name: "Tue", stress: 70, overload: 78 },
  { name: "Wed", stress: 55, overload: 62 },
  { name: "Thu", stress: 75, overload: 80 },
  { name: "Fri", stress: 68, overload: 74 },
  { name: "Sat", stress: 45, overload: 50 },
  { name: "Sun", stress: 40, overload: 44 },
];

function EmotionChart() {
  return (
    <div className="bg-white rounded-xl shadow-sm border p-5">
      <h3 className="text-lg font-semibold text-slate-800 mb-1">
        Emotional & Academic Stress
      </h3>

      <p className="text-sm text-slate-500 mb-5">
        Weekly student feedback analysis
      </p>

      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />

            <Bar
              dataKey="stress"
              name="Stress"
              fill="#ef4444"
              radius={[5, 5, 0, 0]}
            />

            <Bar
              dataKey="overload"
              name="Overload"
              fill="#3b82f6"
              radius={[5, 5, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default EmotionChart;