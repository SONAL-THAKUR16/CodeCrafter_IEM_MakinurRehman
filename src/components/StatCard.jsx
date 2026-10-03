function StatCard({ title, value, description, icon: Icon }) {
  return (
    <div className="bg-white rounded-xl shadow-sm border p-5">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-slate-500">{title}</p>

          <h3 className="text-3xl font-bold text-slate-800 mt-2">
            {value}
          </h3>

          <p className="text-xs text-slate-500 mt-2">
            {description}
          </p>
        </div>

        {Icon && (
          <div className="p-3 bg-blue-100 text-blue-600 rounded-lg">
            <Icon size={24} />
          </div>
        )}
      </div>
    </div>
  );
}

export default StatCard;