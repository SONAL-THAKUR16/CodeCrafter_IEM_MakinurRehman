function Navbar() {
  return (
    <header className="h-16 bg-white border-b flex items-center justify-between px-6">
      <div>
        <h2 className="text-xl font-semibold text-slate-800">
          Student Emotional & Academic Analysis
        </h2>

        <p className="text-sm text-slate-500">
          Monitor student feedback and academic stress
        </p>
      </div>

      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center font-semibold text-blue-600">
          ST
        </div>
      </div>
    </header>
  );
}

export default Navbar;