import React from 'react';
import { AlertCircle, RefreshCw } from 'lucide-react';
import { Button } from './Button';

export function ErrorMessage({ message, onRetry, title = 'Analysis Error' }) {
  return (
    <div className="bg-rose-500/10 border border-rose-500/20 rounded-xl p-5 text-slate-200 flex items-start gap-4">
      <AlertCircle className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
      <div className="flex-1 min-w-0">
        <h4 className="text-sm font-semibold text-rose-300">{title}</h4>
        <p className="text-xs text-rose-200/80 mt-1 leading-relaxed">{message}</p>
        {onRetry && (
          <div className="mt-3">
            <Button size="sm" variant="outline" icon={RefreshCw} onClick={onRetry}>
              Try Again
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}

export default ErrorMessage;
