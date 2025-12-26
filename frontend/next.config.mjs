/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/specs/:path*',
        destination: 'http://localhost:8000/specs/:path*', // Proxy to your backend
      },
    ];
  },
  // Other configs like env variables or image optimization can go here
};

export default nextConfig;