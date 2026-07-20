import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Minimal production image for the Dockerfile — see docs/app/guides/self-hosting.
  output: "standalone",
};

export default nextConfig;
