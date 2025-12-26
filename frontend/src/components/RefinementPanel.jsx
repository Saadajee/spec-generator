// src/components/RefinementPanel.jsx
import { useState } from 'react';

export default function RefinementPanel({ onRefine, isRefining }) {
  const [refinementText, setRefinementText] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (refinementText.trim() && !isRefining) {
      onRefine(refinementText.trim());
      setRefinementText('');
    }
  };

  return (
    <div className="mt-12 sm:mt-16 bg-industrial-800 border-2 border-industrial-600 rounded-lg p-6 sm:p-8 shadow-2xl">
      <h2 className="text-2xl sm:text-3xl font-bold text-industrial-accent mb-5 sm:mb-6 border-b border-industrial-700 pb-3">
        REFINE THE SPEC
      </h2>
      <p className="text-sm sm:text-base text-industrial-400 mb-5 sm:mb-6 font-mono leading-relaxed">
        Suggest improvements, add missing features, fix issues, or clarify open questions.
        <br className="hidden sm:block" />
        <span className="text-industrial-500">
          Examples: "Add JWT authentication to all endpoints", "Use UUIDs instead of integers", "Add pagination to list APIs"
        </span>
      </p>

      <form onSubmit={handleSubmit}>
        <textarea
          value={refinementText}
          onChange={(e) => setRefinementText(e.target.value)}
          placeholder="Describe how you'd like to improve the current specification..."
          className="w-full h-40 sm:h-48 bg-industrial-900 text-industrial-accent font-mono p-4 sm:p-6 rounded border border-industrial-700 focus:border-industrial-accent focus:outline-none resize-none text-sm sm:text-base transition"
          disabled={isRefining}
        />
        <button
          type="submit"
          disabled={isRefining || !refinementText.trim()}
          className="mt-6 w-full py-4 sm:py-5 bg-industrial-warning text-industrial-900 font-bold text-lg sm:text-xl rounded hover:bg-orange-500 transition disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-orange-600/50"
        >
          {isRefining ? "REFINING SPEC..." : "REFINE SPEC"}
        </button>
      </form>
    </div>
  );
}