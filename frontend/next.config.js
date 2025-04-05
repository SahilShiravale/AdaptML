/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  
  // Enable image optimization
  images: {
    domains: ['localhost', 'api.ai-recommendation.com'],
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
    minimumCacheTTL: 60,
  },
  
  // Server-side rendering settings
  experimental: {
    // Enable concurrent features for better performance
    concurrentFeatures: true,
    // Server components for improved SSR
    serverComponents: true,
    // Optimize font loading
    optimizeFonts: true,
  },
  
  // Code splitting optimization
  webpack: (config, { isServer }) => {
    // Keep the chunks small for better loading
    config.optimization.splitChunks = {
      chunks: 'all',
      cacheGroups: {
        commons: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          chunks: 'all',
        },
        // Separate large dependencies into their own chunks
        bigVendors: {
          test: /[\\/]node_modules[\\/](react|react-dom|next)[\\/]/,
          name: 'big-vendors',
          chunks: 'all',
          priority: 10,
        },
      },
    };
    
    return config;
  },
  
  // Environment variables configuration
  env: {
    API_URL: process.env.API_URL || 'http://localhost:8000',
    WEBSOCKET_URL: process.env.WEBSOCKET_URL || 'ws://localhost:8000/ws',
    RECOMMENDATION_ENDPOINT: process.env.RECOMMENDATION_ENDPOINT || '/api/recommendations',
    COURSES_ENDPOINT: process.env.COURSES_ENDPOINT || '/api/courses',
    AUTH_ENDPOINT: process.env.AUTH_ENDPOINT || '/api/auth',
  },
  
  // Additional performance optimizations
  compress: true,
  poweredByHeader: false,
  
  // Configure headers for better caching
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=3600, s-maxage=86400',
          },
        ],
      },
      {
        source: '/api/(.*)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'no-cache, no-store, must-revalidate',
          },
        ],
      },
      {
        source: '/_next/static/(.*)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
    ];
  },
  
  // Configure redirects for better SEO
  async redirects() {
    return [
      {
        source: '/home',
        destination: '/',
        permanent: true,
      },
    ];
  },
};

module.exports = nextConfig;