function StudentAnalysis() {
  return (
    <div>
      <h1 className="text-3xl font-bold text-slate-800">
        Student Analysis
      </h1>

      <p className="text-slate-500 mt-1 mb-6">
        View individual student emotional and academic analysis.
      </p>

      <div className="bg-white border rounded-xl p-6">
        <h2 className="text-xl font-semibold mb-4">
          Student Overview
        </h2>

        <div className="grid md:grid-cols-3 gap-4">
          <div className="p-4 bg-blue-50 rounded-lg">
            <p className="text-sm text-slate-500">Stress</p>
            <p className="text-2xl font-bold">68%</p>
          </div>

          <div className="p-4 bg-yellow-50 rounded-lg">
            <p className="text-sm text-slate-500">Overload</p>
            <p className="text-2xl font-bold">74%</p>
          </div>

          <div className="p-4 bg-green-50 rounded-lg">
            <p className="text-sm text-slate-500">Engagement</p>
            <p className="text-2xl font-bold">81%</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default StudentAnalysis;