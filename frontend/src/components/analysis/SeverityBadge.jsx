import React from 'react';
import { ShieldCheck, AlertTriangle, AlertOctagon } from 'lucide-react';

export function SeverityBadge({ severity = 'LOW', showIcon = true, size = 'md' }) {
  const configs = {
    LOW: {
      label: 'LOW SEVERITY',
      bg: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
      icon: ShieldCheck,
      desc: 'Minimal distress signals detected'
    },
    MODERATE: {
      label: 'MODERATE SEVERITY',
      bg: 'bg-amber-500/10 text-amber-400 border-amber-500/30',
      icon: AlertTriangle,
      desc: 'Moderate academic friction detected'
    },
    HIGH: {
      label: 'HIGH SEVERITY',
      bg: 'bg-rose-500/10 text-rose-400 border-rose-500/30',
      icon: AlertOctagon,
      desc: 'Significant academic distress detected'
    }
  };

  const config = configs[severity.toUpperCase()] || configs.LOW;
  const Icon = config.icon;

  const sizeClasses = {
    sm: 'px-2.5 py-1 text-xs gap-1.5',
    md: 'px-3.5 py-1.5 text-sm gap-2',
    lg: 'px-4 py-2 text-base gap-2.5 font-bold',
  };

  return (
    <span className={`inline-flex items-center rounded-full font-semibold border ${config.bg} ${sizeClasses[size]}`}>
      {showIcon && <Icon className="w-4 h-4 shrink-0" />}
      <span>{config.label}</span>
    </span>
  );
}

export default SeverityBadge;
