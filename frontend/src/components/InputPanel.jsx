// src/components/InputPanel.jsx
export default function InputPanel({ value, onChange, onSubmit, isLoading }) {
  return (
    <div className="bg-industrial-800 border-2 border-industrial-600 rounded-lg p-6 sm:p-8 shadow-2xl">
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Paste your messy product requirements here..."
        className="w-full h-64 sm:h-80 bg-industrial-900 text-industrial-accent font-mono p-4 sm:p-6 rounded border border-industrial-700 focus:border-industrial-accent focus:outline-none resize-none text-sm sm:text-base"
        disabled={isLoading}
      />
      <button
        onClick={onSubmit}
        disabled={isLoading || !value.trim()}
        className="mt-6 w-full py-4 sm:py-5 bg-industrial-accent text-industrial-900 font-bold text-lg sm:text-xl rounded hover:bg-cyan-400 transition disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-cyan-500/50"
      >
        {isLoading ? "GENERATING SPEC..." : "GENERATE SPEC"}
      </button>
    </div>
  );
}