import type { MDXComponents } from 'mdx/types'
import StandardTitle from './src/components/standardtitle'
import StandardTextBox from './src/components/standardtextbox'

export function useMDXComponents(components: MDXComponents): MDXComponents {
    return {
        h1: ({ children }) => (
            <StandardTitle text_size_class="text-3xl" text_alignment_class="text-center">
                {children}
            </StandardTitle>
        ), 
        h2: ({ children }) => (
            <StandardTitle text_size_class="text-2xl" text_alignment_class="text-left">
                {children}
            </StandardTitle>
        ), 
        p: ({ children }) => (
            <StandardTextBox text_alignment_class="text-left">
                {children}
            </StandardTextBox>
        ), 
        ...components,
    }
}