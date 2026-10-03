import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Upload,
  FileText,
  UserSearch,
  TrendingUp,
  BarChart3,
} from "lucide-react";

function Sidebar() {
  const links = [
    {
      name: "Dashboard",
      path: "/",
      icon: LayoutDashboard,
    },
    {
      name: "Upload Feedback",
      path: "/upload",
      icon: Upload,
    },
    {
      name: "Paste Text",
      path: "/paste",
      icon: FileText,
    },
    {
      name: "Student Analysis",
      path: "/student-analysis",
      icon: UserSearch,
    },
    {
      name: "Trend Analysis",
      path: "/trends",
      icon: TrendingUp,
    },
    {
      name: "Reports",
      path: "/reports",
      icon: BarChart3,
    },
  ];

  return (
    <aside className="w-64 min-h-screen bg-slate-900 text-white p-5">
      <h1 className="text-2xl font-bold mb-2">AcademicSense</h1>

      <p className="text-sm text-slate-400 mb-8">
        Student Emotion Analysis
      </p>

      <nav className="space-y-2">
        {links.map((link) => {
          const Icon = link.icon;

          return (
            <NavLink
              key={link.path}
              to={link.path}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-3 rounded-lg transition ${
                  isActive
                    ? "bg-blue-600 text-white"
                    : "text-slate-300 hover:bg-slate-800"
                }`
              }
            >
              <Icon size={20} />
              <span>{link.name}</span>
            </NavLink>
          );
        })}
      </nav>
    </aside>
  );
}

export default Sidebar;