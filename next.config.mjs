import createMDX from "@next/mdx"
import remarkMath from "remark-math"
import rehypeKatex from "rehype-katex"
import rehypeRaw from "rehype-raw"

/** @type {import('next').NextConfig} */
const nextConfig = {
    output: 'export',
    //  Configure `pageExtensions` to include MD, MDX files
    pageExtensions: ['js', 'jsx', 'ts', 'tsx', 'md', 'mdx'],
    basePath: ''
}

const withMDX = createMDX({
    //  Add plugins as necessary
    options: {
        remarkPlugins: [remarkMath],
        rehypePlugins: [rehypeKatex],
    },
    extension: /\.mdx$/
})

const withMarkdown = createMDX({
    //  Add plugins as necessary
    options: {
        remarkPlugins: [remarkMath],
        rehypePlugins: [rehypeKatex, rehypeRaw],
    },
    extension: /\.md$/
})

export default withMDX(withMarkdown(nextConfig))