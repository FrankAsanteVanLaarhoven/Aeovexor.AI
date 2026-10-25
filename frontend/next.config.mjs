import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  outputFileTracingRoot: __dirname,
  async rewrites() {
    return [
      {
        source: '/api/fastapi/:path*',
        destination: 'http://127.0.0.1:8765/api/:path*',
      },
      {
        source: '/api/telemetry/:path*',
        destination: 'http://127.0.0.1:8766/api/:path*',
      },
      {
        source: '/events',
        destination: 'http://127.0.0.1:8766/events',
      },
    ];
  },
};

export default nextConfig;

