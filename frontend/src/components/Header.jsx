// src/components/Header.jsx
export default function Header() {
  return (
    <header className="bg-industrial-900 border-b-4 border-industrial-accent py-6 mb-8">
      <div className="max-w-6xl mx-auto px-6">
        <h1 className="text-4xl sm:text-5xl font-bold text-industrial-accent animate-glitch tracking-wider">
          SPEC GENERATOR
        </h1>
        <p className="text-base sm:text-lg text-industrial-500 mt-2 font-mono">
          Requirement → Structured Specification Engine
        </p>
      </div>
    </header>
  );
}