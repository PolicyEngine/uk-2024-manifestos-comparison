import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  transpilePackages: ['@mantine/core', '@mantine/hooks'],
  turbopack: {
    root: process.cwd(),
  },
};

export default nextConfig;
