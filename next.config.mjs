// @ts-check
import createMDX from '@next/mdx'

export default (phase, { defaultConfig }) => {
  /**
   * @type {import('next').NextConfig}
   */
  const nextConfig = {
    // Configure `pageExtensions` to include markdown and MDX files
    pageExtensions: ['js', 'jsx', 'md', 'mdx', 'ts', 'tsx'], 
    /* config options here */
    output: 'export', 
    basePath: process.env.PAGES_BASE_PATH, 
  }

  const withMDX = createMDX({
    extension: /\.(md|mdx)$/,
    // Add markdown plugins here, as desired
  })

  return withMDX(nextConfig)
}