import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Activity, ShieldCheck, Cpu, Database } from 'lucide-react';

function App() {
  const [backendStatus, setBackendStatus] = useState({ status: 'checking', message: 'Connecting to backend...' });

  useEffect(() => {
    axios.get('/api/health')
      .then((res) => {
        setBackendStatus({ status: 'online', message: 'FastAPI Backend Connected', data: res.data });
      })
      .catch((err) => {
        // Direct call fallback if proxy path differs in dev test
        axios.get('http://127.0.0.1:8000/api/health')
          .then((res) => {
            setBackendStatus({ status: 'online', message: 'FastAPI Backend Connected (Direct)', data: res.data });
          })
          .catch(() => {
            setBackendStatus({ status: 'offline', message: 'Backend Offline or Initializing' });
          });
      });
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col justify-center items-center p-6">
      <div className="max-w-2xl w-full bg-slate-900 border border-slate-800 rounded-xl p-8 shadow-2xl space-y-6">
        <div className="flex items-center space-x-3 border-b border-slate-800 pb-4">
          <Cpu className="w-8 h-8 text-indigo-400" />
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight">CodeCrafter</h1>
            <p className="text-sm text-slate-400">Student Academic Experience & Emotion Analyzer</p>
          </div>
        </div>

        <div className="space-y-4">
          <div className="flex justify-between items-center bg-slate-950 p-4 rounded-lg border border-slate-800">
            <span className="text-sm text-slate-400 flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-emerald-400" /> Institution:
            </span>
            <span className="font-medium text-slate-200">Institute of Engineering and Management</span>
          </div>

          <div className="flex justify-between items-center bg-slate-950 p-4 rounded-lg border border-slate-800">
            <span className="text-sm text-slate-400 flex items-center gap-2">
              <Activity className="w-4 h-4 text-indigo-400" /> Team Leader:
            </span>
            <span className="font-medium text-slate-200">Makinur Rahaman</span>
          </div>

          <div className="flex justify-between items-center bg-slate-950 p-4 rounded-lg border border-slate-800">
            <span className="text-sm text-slate-400 flex items-center gap-2">
              <Database className="w-4 h-4 text-cyan-400" /> Backend Status:
            </span>
            <span className={`px-3 py-1 text-xs font-semibold rounded-full ${
              backendStatus.status === 'online' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
            }`}>
              {backendStatus.message}
            </span>
          </div>
        </div>

        <div className="text-center text-xs text-slate-500 pt-2">
          Step 1 Scaffolding Complete &bull; Frontend & Backend Integration Initialized
        </div>
      </div>
    </div>
  );
}

export default App;
