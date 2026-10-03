import React from 'react';

export function Card({ children, className = '', title, subtitle, icon: Icon, action }) {
  return (
    <div className={`bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-lg text-slate-100 ${className}`}>
      {(title || subtitle || Icon || action) && (
        <div className="flex justify-between items-start mb-4 pb-3 border-b border-slate-800/80">
          <div className="flex items-center gap-3">
            {Icon && <Icon className="w-5 h-5 text-indigo-400 shrink-0" />}
            <div>
              {title && <h3 className="text-lg font-semibold text-white tracking-tight">{title}</h3>}
              {subtitle && <p className="text-xs text-slate-400 mt-0.5">{subtitle}</p>}
            </div>
          </div>
          {action && <div>{action}</div>}
        </div>
      )}
      {children}
    </div>
  );
}

export default Card;
