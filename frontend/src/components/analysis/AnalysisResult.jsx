import React from 'react';
import { PrimaryConcernCard } from './PrimaryConcernCard';
import { SignalCard } from './SignalCard';
import { SentimentCard } from './SentimentCard';
import { EmotionList } from './EmotionList';
import { AcademicContext } from './AcademicContext';
import { EvidenceList } from './EvidenceList';

export function AnalysisResult({ result, analysisId }) {
  if (!result) return null;

  const {
    sentiment,
    emotions,
    signals,
    academic_context: academicContext,
    primary_concern: primaryConcern,
    overall_severity: overallSeverity,
    severity_reason: severityReason,
    evidence,
    explanation,
    student_insight: studentInsight,
    disclaimer
  } = result;

  return (
    <div className="space-y-6 animate-fadeIn">
      <div className="flex justify-between items-center px-1">
        <h2 className="text-xl font-bold text-white tracking-tight">Analysis Results</h2>
        {analysisId && (
          <span className="text-xs font-mono text-slate-400 bg-slate-900 px-3 py-1 rounded-full border border-slate-800">
            ID: {analysisId}
          </span>
        )}
      </div>

      {/* Primary Concern & Overall Severity */}
      <PrimaryConcernCard
        overallSeverity={overallSeverity}
        severityReason={severityReason}
        primaryConcern={primaryConcern}
        studentInsight={studentInsight}
        disclaimer={disclaimer}
      />

      {/* Signal Scores */}
      <SignalCard signals={signals} />

      {/* Sentiment & Emotion Section Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <SentimentCard sentiment={sentiment} />
        <EmotionList emotions={emotions} />
      </div>

      {/* Academic Context Dimension Flags */}
      <AcademicContext academicContext={academicContext} />

      {/* Evidence & Explanation */}
      <EvidenceList evidence={evidence} explanation={explanation} />
    </div>
  );
}

export default AnalysisResult;
