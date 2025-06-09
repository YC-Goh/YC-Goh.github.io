import type { MDXComponents } from 'mdx/types'
import StandardTitle, { StandardHeading, StandardSubheading, StandardSubtitle } from './src/components/standard/standardtitle'
import StandardTextBox from './src/components/standard/standardtextbox'
import StandardList from './src/components/standard/standardlist'
import StandardLink from './src/components/standard/standardlink'

export function useMDXComponents(components: MDXComponents): MDXComponents {
    return {
        h1: ({ children }) => (
            <StandardTitle margin_class="my-2" text_size_class="text-2xl md:text-3xl" text_alignment_class="text-center" reference_class="mdx-title">
                { children }
            </StandardTitle>
        ), 
        h2: ({ children }) => (
            <StandardSubtitle margin_class="my-2" text_size_class="text-1xl md:text-2xl" text_alignment_class="text-left" reference_class="mdx-subtitle">
                { children }
            </StandardSubtitle>
        ), 
        h3: ({ children }) => (
            <StandardHeading margin_class="my-2" text_size_class="text-sm md:text-base" text_alignment_class="text-left" reference_class="mdx-heading">
                { children }
            </StandardHeading>
        ), 
        h4: ({ children }) => (
            <StandardSubheading margin_class="my-2" text_size_class="text-sm md:text-base" text_alignment_class="text-left" reference_class="mdx-subheading">
                { children }
            </StandardSubheading>
        ), 
        p: ({ children }) => (
            <StandardTextBox text_size_class="text-sm md:text-base" text_alignment_class="text-left" reference_class="mdx-text-element">
                { children }
            </StandardTextBox>
        ), 
        a: ({ children, href }) => (
            <StandardLink padding_class="" text_size_class="text-xs md:text-sm" text_alignment_class="text-left" href={ href } reference_class="mdx-text-element">
                { children }
            </StandardLink>
        ), 
        ul: ({ children }) => (
            <StandardList text_alignment_class="text-left" list_type="list-disc" reference_class="mdx-unsorted-list">
                { children }
            </StandardList>
        ), 
        ol: ({ children }) => (
            <StandardList text_alignment_class="text-left" list_type="list-decimal" reference_class="mdx-sorted-list">
                { children }
            </StandardList>
        ), 
        ...components,
    }
}