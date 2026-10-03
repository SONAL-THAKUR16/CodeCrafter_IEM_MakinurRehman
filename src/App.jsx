import { BrowserRouter, Routes, Route } from "react-router-dom";

import Sidebar from "./components/Sidebar.jsx";
import Navbar from "./components/Navbar.jsx";

import Dashboard from "./pages/Dashboard.jsx";
import UploadFeedback from "./pages/UploadFeedback.jsx";
import PasteText from "./pages/PasteText.jsx";
import StudentAnalysis from "./pages/StudentAnalysis.jsx";
import TrendAnalysis from "./pages/TrendAnalysis.jsx";
import Reports from "./pages/Reports.jsx";

function App() {
  return (
    <BrowserRouter>
      <div className="flex min-h-screen bg-slate-100">
        <Sidebar />

        <div className="flex-1">
          <Navbar />

          <main className="p-6">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/upload" element={<UploadFeedback />} />
              <Route path="/paste" element={<PasteText />} />
              <Route
                path="/student-analysis"
                element={<StudentAnalysis />}
              />
              <Route path="/trends" element={<TrendAnalysis />} />
              <Route path="/reports" element={<Reports />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;