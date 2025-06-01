// @ts-check
 
export default (phase, { defaultConfig }) => {
  /**
   * @type {import('next').NextConfig}
   */
  const nextConfig = {
    /* config options here */
    output: 'export', 
    basePath: process.env.PAGES_BASE_PATH, 
  }
  return nextConfig
}