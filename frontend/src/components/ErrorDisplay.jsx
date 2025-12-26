// src/components/ErrorDisplay.jsx
export default function ErrorDisplay({ error, traceId }) {
  return (
    <div className="bg-red-900/20 border-2 border-red-500 rounded-lg p-6 sm:p-8">
      <h3 className="text-xl sm:text-2xl font-bold text-red-400 mb-4">Generation Failed</h3>
      <div className="text-sm sm:text-base text-industrial-200 mb-6 leading-relaxed whitespace-pre-wrap">
        {error}
      </div>
      {traceId && (
        <p className="text-xs sm:text-sm font-mono text-industrial-500">
          Trace ID: <span className="text-industrial-accent font-bold">{traceId}</span>
        </p>
      )}
    </div>
  );
}