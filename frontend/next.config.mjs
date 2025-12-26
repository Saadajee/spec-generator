// next.config.mjs (or next.config.js)

/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/specs/:path*',
        destination: 'http://localhost:8000/specs/:path*', // Only used in local dev
      },
    ];
  },
};

export default nextConfig;
