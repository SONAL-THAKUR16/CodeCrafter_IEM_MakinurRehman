import {
  Users,
  Brain,
  AlertTriangle,
  Activity,
} from "lucide-react";

import StatCard from "../components/StatCard";
import EmotionChart from "../components/EmotionChart";

function Dashboard() {
  return (
    <div>
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-slate-800">
          Dashboard
        </h1>

        <p className="text-slate-500 mt-1">
          Overview of student emotions and academic workload
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-5">
        <StatCard
          title="Students Analyzed"
          value="1,482"
          description="Total feedback analyzed"
          icon={Users}
        />

        <StatCard
          title="Average Stress"
          value="68%"
          description="Current average level"
          icon={Brain}
        />

        <StatCard
          title="Overload Level"
          value="74%"
          description="Academic overload"
          icon={AlertTriangle}
        />

        <StatCard
          title="Active Cohorts"
          value="18"
          description="Currently monitored"
          icon={Activity}
        />
      </div>

      <div className="mt-6">
        <EmotionChart />
      </div>
    </div>
  );
}

export default Dashboard;