import type { MDXComponents } from 'mdx/types'
import StandardTitle from './src/components/standard/standardtitle'
import StandardTextBox from './src/components/standard/standardtextbox'
import StandardUnsortedList from './src/components/standard/standardunsortedlist'

export function useMDXComponents(components: MDXComponents): MDXComponents {
    return {
        h1: ({ children }) => (
            <StandardTitle margin_class="my-2" text_size_class="text-3xl" text_alignment_class="text-center" reference_class="mdx-title">
                { children }
            </StandardTitle>
        ), 
        h2: ({ children }) => (
            <StandardTitle margin_class="my-2" text_size_class="text-2xl" text_alignment_class="text-left" reference_class="mdx-subtitle">
                { children }
            </StandardTitle>
        ), 
        p: ({ children }) => (
            <StandardTextBox text_alignment_class="text-left" reference_class="mdx-text-element">
                { children }
            </StandardTextBox>
        ), 
        ul: ({ children }) => (
            <StandardUnsortedList text_alignment_class="text-left" reference_class="mdx-unsorted-list">
                { children }
            </StandardUnsortedList>
        ), 
        ...components,
    }
}