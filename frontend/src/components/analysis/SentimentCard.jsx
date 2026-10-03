import React from 'react';
import { Smile, Meh, Frown, Split } from 'lucide-react';
import { Card } from '../common/Card';

export function SentimentCard({ sentiment }) {
  if (!sentiment) return null;

  const label = sentiment.label?.toLowerCase() || 'neutral';
  const scores = sentiment.scores || { positive: 0, neutral: 0, negative: 0 };

  const posPct = Math.round((scores.positive || 0) * 100);
  const neuPct = Math.round((scores.neutral || 0) * 100);
  const negPct = Math.round((scores.negative || 0) * 100);

  const sentimentConfig = {
    positive: { label: 'POSITIVE', color: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30', icon: Smile },
    negative: { label: 'NEGATIVE', color: 'bg-rose-500/10 text-rose-400 border-rose-500/30', icon: Frown },
    neutral: { label: 'NEUTRAL', color: 'bg-slate-500/10 text-slate-300 border-slate-500/30', icon: Meh },
    mixed: { label: 'MIXED SENTIMENT', color: 'bg-amber-500/10 text-amber-400 border-amber-500/30', icon: Split }
  };

  const current = sentimentConfig[label] || sentimentConfig.neutral;
  const Icon = current.icon;

  return (
    <Card
      title="Sentiment Analysis"
      subtitle="Transformer sentiment classification & distribution"
      icon={Icon}
    >
      <div className="space-y-4">
        {/* Dominant Label Badge */}
        <div className="flex justify-between items-center bg-slate-950 p-4 rounded-lg border border-slate-800">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
            Dominant Sentiment
          </span>
          <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold border ${current.color}`}>
            <Icon className="w-4 h-4 shrink-0" />
            {current.label}
          </span>
        </div>

        {/* Probability Breakdown Bar */}
        <div className="space-y-2">
          <div className="flex justify-between text-xs text-slate-400 font-medium px-1">
            <span>Positive: <strong className="text-emerald-400">{posPct}%</strong></span>
            <span>Neutral: <strong className="text-slate-300">{neuPct}%</strong></span>
            <span>Negative: <strong className="text-rose-400">{negPct}%</strong></span>
          </div>

          <div className="h-3 w-full bg-slate-950 rounded-full overflow-hidden flex border border-slate-800">
            <div className="bg-emerald-500 transition-all duration-500" style={{ width: `${posPct}%` }} title={`Positive ${posPct}%`} />
            <div className="bg-slate-500 transition-all duration-500" style={{ width: `${neuPct}%` }} title={`Neutral ${neuPct}%`} />
            <div className="bg-rose-500 transition-all duration-500" style={{ width: `${negPct}%` }} title={`Negative ${negPct}%`} />
          </div>
        </div>
      </div>
    </Card>
  );
}

export default SentimentCard;
