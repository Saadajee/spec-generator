// src/components/LoadingSpinner.jsx
export default function LoadingSpinner() {
  return (
    <div className="flex flex-col items-center justify-center py-16 sm:py-20">
      <div className="relative w-20 h-20 sm:w-24 sm:h-24">
        <div className="absolute inset-0 border-8 border-industrial-700 rounded-full animate-spin-slow"></div>
        <div className="absolute inset-0 border-8 border-t-industrial-accent border-r-industrial-accent border-b-industrial-700 border-l-industrial-700 rounded-full animate-spin"></div>
        <div className="absolute top-3 left-3 sm:top-4 sm:left-4 w-14 h-14 sm:w-16 sm:h-16 border-4 border-industrial-accent rounded-full animate-pulse-glow"></div>
      </div>
      <p className="mt-6 sm:mt-8 text-lg sm:text-xl text-industrial-accent font-mono animate-pulse">
        Processing Requirements...
      </p>
    </div>
  );
}