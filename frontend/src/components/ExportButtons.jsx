// src/components/ExportButtons.jsx
export default function ExportButtons({ spec, traceId }) {
  const copyJson = () => {
    navigator.clipboard.writeText(JSON.stringify(spec, null, 2));
    alert('Full spec copied to clipboard!');
  };

  const downloadJson = () => {
    const dataStr = JSON.stringify(spec, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${traceId || 'spec'}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="flex flex-col sm:flex-row gap-4 mt-8">
      <button
        onClick={copyJson}
        className="px-6 py-4 bg-industrial-700 hover:bg-industrial-600 text-industrial-accent font-mono font-bold rounded transition text-base sm:text-lg shadow-md"
      >
        COPY JSON
      </button>
      <button
        onClick={downloadJson}
        className="px-6 py-4 bg-industrial-warning text-industrial-900 font-mono font-bold rounded hover:bg-orange-500 transition text-base sm:text-lg shadow-md"
      >
        DOWNLOAD JSON
      </button>
    </div>
  );
}