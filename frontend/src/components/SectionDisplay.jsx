// src/components/SectionDisplay.jsx
import React from 'react';
import SyntaxHighlighter from 'react-syntax-highlighter';
import { atomOneDark } from 'react-syntax-highlighter/dist/esm/styles/hljs';

const syntaxTheme = {
  ...atomOneDark,
  hljs: {
    ...atomOneDark.hljs,
    background: '#1a1d2a',
    color: '#e2e8f0',
  },
};

export default function SectionDisplay({ title, data }) {
  if (!data || (Array.isArray(data) && data.length === 0) || (typeof data === 'object' && !Array.isArray(data) && Object.keys(data).length === 0)) {
    return (
      <section className="bg-industrial-800 rounded-xl p-10 border border-industrial-700">
        <h3 className="text-2xl font-bold text-industrial-accent mb-4 font-display">{title}</h3>
        <p className="text-industrial-500 italic">No data available.</p>
      </section>
    );
  }

  // Object: features_by_module
  if (typeof data === 'object' && !Array.isArray(data)) {
    return (
      <section className="bg-industrial-800 rounded-xl p-10 border border-industrial-700">
        <h3 className="text-2xl font-bold text-industrial-accent mb-8 font-display">{title}</h3>
        <div className="space-y-10">
          {Object.entries(data).map(([moduleName, features]) => (
            <div key={moduleName} className="bg-industrial-900 rounded-lg p-6 border border-industrial-600">
              <h4 className="text-xl font-bold text-cyan-300 mb-4 font-mono">{moduleName}</h4>
              <ul className="space-y-3">
                {features.map((feature, i) => (
                  <li key={i} className="flex items-start">
                    <span className="text-industrial-accent mr-3 mt-1">▸</span>
                    <span className="text-industrial-300">{feature}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </section>
    );
  }

  // Array of objects → API endpoints, DB schema
  if (Array.isArray(data) && data[0] && typeof data[0] === 'object') {
    return (
      <section className="bg-industrial-800 rounded-xl p-10 border border-industrial-700">
        <h3 className="text-2xl font-bold text-industrial-accent mb-8 font-display">{title}</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {data.map((item, index) => (
            <div
              key={index}
              className="bg-industrial-900 rounded-lg overflow-hidden border border-industrial-700 shadow-lg"
            >
              <SyntaxHighlighter
                language="json"
                style={syntaxTheme}
                customStyle={{ margin: 0, padding: '1.5rem', fontSize: '0.9rem' }}
                showLineNumbers
              >
                {JSON.stringify(item, null, 2)}
              </SyntaxHighlighter>
            </div>
          ))}
        </div>
      </section>
    );
  }

  // Simple string array → modules, stories, questions
  return (
    <section className="bg-industrial-800 rounded-xl p-10 border border-industrial-700">
      <h3 className="text-2xl font-bold text-industrial-accent mb-8 font-display">{title}</h3>
      <ol className="space-y-4">
        {data.map((item, index) => (
          <li
            key={index}
            className="bg-industrial-900 px-8 py-5 rounded-lg border border-industrial-700 text-industrial-300 leading-relaxed flex items-start"
          >
            <span className="text-industrial-accent font-bold mr-4 mt-0.5">{index + 1}.</span>
            <span>{item}</span>
          </li>
        ))}
      </ol>
    </section>
  );
}