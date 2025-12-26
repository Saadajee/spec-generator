// frontend-next/src/pages/index.js
import { useState } from 'react';
import Header from '../components/Header';
import InputPanel from '../components/InputPanel';
import LoadingSpinner from '../components/LoadingSpinner';
import OutputTabs from '../components/OutputTabs';
import ExportButtons from '../components/ExportButtons';
import ErrorDisplay from '../components/ErrorDisplay';
import RefinementPanel from '../components/RefinementPanel';
import { generateSpec, refineSpec } from '../services/api';

export default function Home() {
  const [input, setInput] = useState('');
  const [spec, setSpec] = useState(null);
  const [traceId, setTraceId] = useState('');
  const [loading, setLoading] = useState(false);
  const [refining, setRefining] = useState(false);
  const [error, setError] = useState('');

  const handleGenerate = async () => {
    if (!input.trim()) return;
    setLoading(true);
    setError('');
    setSpec(null);
    setTraceId('');
    try {
      const result = await generateSpec(input);
      setSpec(result.spec);
      setTraceId(result.trace_id);
    } catch (err) {
      console.error('Generation error:', err);
      setError(err.message || 'Generation failed — please try again.');
      const tid = err.response?.data?.trace_id || err.response?.data?.traceId;
      if (tid) setTraceId(tid);
    } finally {
      setLoading(false);
    }
  };

  const handleRefine = async (refinementText) => {
    if (!refinementText.trim() || !spec || !traceId) return;
    setRefining(true);
    setError('');
    try {
      const result = await refineSpec(spec, refinementText, traceId);
      setSpec(result.spec);
    } catch (err) {
      console.error('Refinement error:', err);
      setError(err.message || 'Refinement failed — please try again.');
      const tid = err.response?.data?.trace_id || err.response?.data?.traceId || traceId;
      if (tid && tid !== traceId) setTraceId(tid);
    } finally {
      setRefining(false);
    }
  };

  return (
    <div className="min-h-screen bg-industrial-900">
      <Header />
      <main className="max-w-6xl mx-auto px-6 pt-12 pb-20">
        <div className="max-w-4xl mx-auto">
          <InputPanel
            value={input}
            onChange={setInput}
            onSubmit={handleGenerate}
            isLoading={loading}
          />
          {(loading || refining) && (
            <div className="mt-12">
              <LoadingSpinner />
            </div>
          )}
          {error && (
            <div className="mt-8">
              <ErrorDisplay error={error} traceId={traceId} />
            </div>
          )}
          {spec && !error && (
            <>
              <div className="mt-8">
                <ExportButtons spec={spec} traceId={traceId} />
              </div>
              <div className="mt-12">
                <OutputTabs spec={spec} />
              </div>
              <div className="mt-16">
                <RefinementPanel
                  onRefine={handleRefine}
                  isRefining={refining}
                />
              </div>
            </>
          )}
        </div>
      </main>
    </div>
  );
}