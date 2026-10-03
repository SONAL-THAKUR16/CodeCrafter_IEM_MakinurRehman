import React from 'react';
import { Heart, Sparkles } from 'lucide-react';
import { Card } from '../common/Card';

export function EmotionList({ emotions = [] }) {
  if (!emotions || emotions.length === 0) {
    return (
      <Card title="Detected Emotions" subtitle="Fine-grained emotion classification" icon={Heart}>
        <p className="text-xs text-slate-500 italic text-center py-4">No specific emotional peaks detected.</p>
      </Card>
    );
  }

  // Display top 4 emotions
  const topEmotions = emotions.slice(0, 4);

  return (
    <Card
      title="Detected Emotions"
      subtitle="Hugging Face transformer emotion classification scores"
      icon={Heart}
    >
      <div className="space-y-3">
        {topEmotions.map((emo, idx) => {
          const scorePct = Math.round(emo.score * 100);
          return (
            <div key={idx} className="bg-slate-950 p-3 rounded-lg border border-slate-800 space-y-1.5">
              <div className="flex justify-between items-center text-xs">
                <span className="font-semibold text-slate-200 capitalize flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5 text-indigo-400" /> {emo.label}
                </span>
                <span className="font-bold text-indigo-400">{scorePct}%</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                <div
                  className="bg-indigo-500 h-full rounded-full transition-all duration-500"
                  style={{ width: `${scorePct}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </Card>
  );
}

export default EmotionList;
