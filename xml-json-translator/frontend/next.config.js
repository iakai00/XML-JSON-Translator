/** @type {import('next').NextConfig} */
const nextConfig = {
    // Use "standalone" output for Docker deployments
    output: 'standalone',
    
    // Ignore ESLint errors during builds
    eslint: {
      ignoreDuringBuilds: true,
    },
    
    // Ignore TypeScript errors during builds
    typescript: {
      ignoreBuildErrors: true,
    },
    
    // Enable React strict mode for better error detection
    reactStrictMode: true,
    
    // Environment variables that will be available in the browser
    env: {
      NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
    },
    
    // Image optimization configuration
    images: {
      domains: ['localhost'],
      formats: ['image/webp'],
    },
    
    // Additional configurations
    experimental: {
      // Any experimental features can go here
    },
  };
  
  module.exports = nextConfig;