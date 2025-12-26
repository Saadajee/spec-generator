const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/specs/:path*',
        destination: `${backendUrl}/specs/:path*`,
      },
    ];
  },
};

export default nextConfig;
