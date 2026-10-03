import React, { useState, useEffect, useRef } from 'react';
import { api } from '../services/api';
import { Navbar } from '../components/layout/Navbar';
import { AnalysisInput } from '../components/analysis/AnalysisInput';
import { AnalysisResult } from '../components/analysis/AnalysisResult';
import { SummaryCards } from '../components/dashboard/SummaryCards';
import { SeverityChart } from '../components/dashboard/SeverityChart';
import { SignalChart } from '../components/dashboard/SignalChart';
import { TrendChart } from '../components/dashboard/TrendChart';
import { RecentAnalyses } from '../components/dashboard/RecentAnalyses';
import { ErrorMessage } from '../components/common/ErrorMessage';
import { Loader } from '../components/common/Loader';
import { RefreshCw } from 'lucide-react';

export function Dashboard() {
  const [inputText, setInputText] = useState('');
  const [healthStatus, setHealthStatus] = useState('checking');
  const [analysisResult, setAnalysisResult] = useState(null);
  const [analysisId, setAnalysisId] = useState(null);
  
  // Loading states
  const [loadingAnalysis, setLoadingAnalysis] = useState(false);
  const [loadingHistory, setLoadingHistory] = useState(false);
  const [loadingDashboard, setLoadingDashboard] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);

  // Dashboard Data
  const [historyItems, setHistoryItems] = useState([]);
  const [summaryData, setSummaryData] = useState(null);
  const [trendData, setTrendData] = useState([]);

  const resultsRef = useRef(null);

  // Check health and load initial dashboard data on mount
  useEffect(() => {
    checkHealth();
    fetchDashboardData();
  }, []);

  const checkHealth = async () => {
    const res = await api.healthCheck();
    if (res.success && res.data?.status === 'ok') {
      setHealthStatus('online');
    } else {
      setHealthStatus('offline');
    }
  };

  const fetchDashboardData = async () => {
    setLoadingHistory(true);
    setLoadingDashboard(true);

    const [histRes, sumRes, trendRes] = await Promise.all([
      api.getHistory(10),
      api.getDashboardSummary(),
      api.getDashboardTrends(10)
    ]);

    if (histRes.success) {
      setHistoryItems(histRes.data?.items || histRes.data?.history || []);
    }
    setLoadingHistory(false);

    if (sumRes.success) {
      setSummaryData(sumRes.data?.summary || null);
    }

    if (trendRes.success) {
      setTrendData(trendRes.data?.trends || []);
    }
    setLoadingDashboard(false);
  };

  const handleAnalyze = async () => {
    if (!inputText.trim()) return;

    setLoadingAnalysis(true);
    setErrorMessage(null);

    const res = await api.analyzeText(inputText);

    if (res.success && res.data?.analysis) {
      setAnalysisResult(res.data.analysis);
      setAnalysisId(res.data.analysis_id);
      
      // Refresh history and aggregate stats after new analysis
      fetchDashboardData();

      // Smooth scroll to results
      setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 100);
    } else {
      setErrorMessage(res.error || 'Failed to complete analysis.');
    }

    setLoadingAnalysis(false);
  };

  const handleSelectHistoryItem = async (id) => {
    setLoadingAnalysis(true);
    setErrorMessage(null);

    const res = await api.getAnalysis(id);

    if (res.success && res.data?.analysis) {
      setAnalysisResult(res.data.analysis);
      setAnalysisId(res.data.analysis_id || id);

      // Smooth scroll to results
      setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 100);
    } else {
      setErrorMessage(res.error || 'Unable to retrieve stored analysis.');
    }

    setLoadingAnalysis(false);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-indigo-500 selection:text-white">
      {/* Header */}
      <Navbar healthStatus={healthStatus} />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 lg:px-8 py-8 space-y-8">
        {/* Error Alert Banner */}
        {errorMessage && (
          <ErrorMessage
            message={errorMessage}
            onRetry={() => {
              setErrorMessage(null);
              checkHealth();
              fetchDashboardData();
            }}
          />
        )}

        {/* Input Section */}
        <section>
          <AnalysisInput
            text={inputText}
            setText={setInputText}
            onAnalyze={handleAnalyze}
            loading={loadingAnalysis}
            disabled={healthStatus === 'offline'}
          />
        </section>

        {/* Loading Spinner for Analysis */}
        {loadingAnalysis && (
          <div className="py-8 bg-slate-900/50 rounded-xl border border-slate-800">
            <Loader text="Analyzing academic feedback with context-aware NLP engine..." />
          </div>
        )}

        {/* Analysis Results View */}
        <section ref={resultsRef}>
          {analysisResult && (
            <AnalysisResult result={analysisResult} analysisId={analysisId} />
          )}
        </section>

        {/* Aggregate Dashboard Metrics & Charts Section */}
        <section className="space-y-6 pt-4 border-t border-slate-800/80">
          <div className="flex justify-between items-center">
            <div>
              <h2 className="text-xl font-bold text-white tracking-tight">Institutional Dashboard Analytics</h2>
              <p className="text-xs text-slate-400">Aggregate statistics and trends calculated from student feedback</p>
            </div>
            <button
              type="button"
              onClick={fetchDashboardData}
              disabled={loadingDashboard}
              className="text-xs text-slate-400 hover:text-white flex items-center gap-1.5 bg-slate-900 hover:bg-slate-800 px-3 py-1.5 rounded-lg border border-slate-800 transition-colors cursor-pointer"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${loadingDashboard ? 'animate-spin' : ''}`} />
              Refresh
            </button>
          </div>

          {/* Metric Summary Cards */}
          <SummaryCards summary={summaryData} />

          {/* Charts Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <SeverityChart distribution={summaryData?.severity_distribution} />
            <SignalChart summary={summaryData} />
            <TrendChart trends={trendData} />
          </div>

          {/* Recent Analysis History List */}
          <RecentAnalyses
            items={historyItems}
            onSelectAnalysis={handleSelectHistoryItem}
            loading={loadingHistory}
          />
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-slate-950 border-t border-slate-800/80 py-6 mt-12 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row justify-between items-center gap-3">
          <div>
            <span className="font-semibold text-slate-400">EduSense AI</span> &bull; CodeCrafter Hackathon MVP &bull; Institute of Engineering and Management
          </div>
          <div>
            Team Leader: <span className="text-slate-300 font-medium">Makinur Rahaman</span>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default Dashboard;
