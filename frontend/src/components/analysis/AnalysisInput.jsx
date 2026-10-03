import React from 'react';
import { Sparkles, Trash2, Send, MessageSquareQuote } from 'lucide-react';
import { Card } from '../common/Card';
import { Button } from '../common/Button';

const PRESET_EXAMPLES = [
  {
    label: "High Workload & Overload",
    text: "I have three assignments due this week and I cannot concentrate."
  },
  {
    label: "Positive Engagement",
    text: "I enjoy the course and I feel confident about the assignments."
  },
  {
    label: "Negation Case",
    text: "I am not stressed about the upcoming exam."
  },
  {
    label: "Mixed Sentiment",
    text: "I really enjoy the subject, but the workload is becoming overwhelming."
  }
];

export function AnalysisInput({
  text,
  setText,
  onAnalyze,
  loading,
  disabled
}) {
  const charCount = text.length;
  const maxChars = 5000;
  const isOverLimit = charCount > maxChars;
  const isSubmitDisabled = !text.trim() || isOverLimit || loading || disabled;

  const handleSelectExample = (exampleText) => {
    setText(exampleText);
  };

  const handleClear = () => {
    setText('');
  };

  return (
    <Card
      title="Analyze Student Feedback"
      subtitle="Paste academic feedback to identify emotional, workload, and cognitive distress signals."
      icon={Sparkles}
    >
      <div className="space-y-4">
        <div className="relative">
          <textarea
            id="feedback-input"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Example: I have three assignments due this week and I am struggling to keep up with the workload..."
            rows={5}
            maxLength={maxChars + 100}
            className="w-[#100%] w-full bg-slate-950 border border-slate-800 rounded-lg p-4 text-sm text-slate-100 placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all resize-y min-h-[120px]"
            aria-label="Student feedback input text"
          />
          <div className="flex justify-between items-center text-xs text-slate-500 mt-1.5 px-1">
            <span>Anonymous analysis (No student PII required)</span>
            <span className={isOverLimit ? 'text-rose-400 font-semibold' : ''}>
              {charCount} / {maxChars} characters
            </span>
          </div>
        </div>

        {/* Preset Example Buttons */}
        <div className="pt-2 border-t border-slate-800/60">
          <div className="flex items-center gap-1.5 text-xs text-slate-400 mb-2 font-medium">
            <MessageSquareQuote className="w-3.5 h-3.5 text-indigo-400" />
            <span>Try an example sentence:</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {PRESET_EXAMPLES.map((ex, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => handleSelectExample(ex.text)}
                className="text-xs px-3 py-1.5 rounded-lg bg-slate-800/70 hover:bg-slate-800 text-slate-300 hover:text-white border border-slate-700/60 transition-all text-left truncate max-w-xs cursor-pointer"
                title={ex.text}
              >
                <span className="font-medium text-indigo-300 mr-1">{ex.label}:</span>
                <span className="opacity-80">"{ex.text.slice(0, 35)}..."</span>
              </button>
            ))}
          </div>
        </div>

        {/* Form Actions */}
        <div className="flex justify-between items-center pt-2">
          <Button
            variant="outline"
            size="sm"
            icon={Trash2}
            onClick={handleClear}
            disabled={!text || loading}
          >
            Clear Text
          </Button>

          <Button
            variant="primary"
            size="md"
            icon={Send}
            onClick={onAnalyze}
            loading={loading}
            disabled={isSubmitDisabled}
          >
            {loading ? 'Analyzing Feedback...' : 'Analyze Feedback'}
          </Button>
        </div>
      </div>
    </Card>
  );
}

export default AnalysisInput;
