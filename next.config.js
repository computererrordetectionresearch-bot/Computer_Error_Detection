/** @type {import('next').NextConfig} */
const nextConfig = {
  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        'webworker-threads': false,
      };
    }
    return config;
  },
};

module.exports = nextConfig;

