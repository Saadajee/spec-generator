/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/specs/:path*',
        destination: 'https://your-username-your-space.huggingface.space/specs/:path*', // ← Replace with your actual HF Space URL
      },
    ];
  },
};

export default nextConfig;
