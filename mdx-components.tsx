import type { MDXComponents } from 'mdx/types'
import StandardTitle, { StandardHeading, StandardSubheading, StandardSubtitle } from './src/components/standard/standardtitle'
import StandardTextBox from './src/components/standard/standardtextbox'
import StandardList from './src/components/standard/standardlist'
import StandardLink from './src/components/standard/standardlink'
import StandardTable, { StandardTableBody, StandardTableDataCell, StandardTableHead, StandardTableHeaderCell, StandardTableRow } from './src/components/standard/standardtableelems'

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
            <StandardLink padding_class="" text_size_class="" text_alignment_class="text-left" href={ href } reference_class="mdx-text-element">
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
        table: ({ children }) => (
            <StandardTable border_class="border-y-2 border-sky-200" reference_class="mdx-table">
                { children }
            </StandardTable>
        ), 
        thead: ({ children }) => (
            <StandardTableHead border_class="border-y-2 border-sky-200" reference_class="mdx-table-head">
                { children }
            </StandardTableHead>
        ), 
        tbody: ({ children }) => (
            <StandardTableBody border_class="border-y-2 border-sky-200" reference_class="mdx-table-head">
                { children }
            </StandardTableBody>
        ), 
        tr: ({ children }) => (
            <StandardTableRow reference_class="mdx-table-row">
                { children }
            </StandardTableRow>
        ), 
        th: ({ children }) => {
            let column_width_class: string
            column_width_class = ""
            if (typeof children == "string") {
                if (/^\{(?:[a-z]+:)?w-.+?\}/i.test(children)) {
                    column_width_class = /^\{((?:[a-z]+:)?w-.+?)\}/i.exec(children)[1]
                    children = children.replace(/^\{(?:[a-z]+:)?w-.+?\}/i, "")
                }
            }
            { <div className="w-1/3 w-1/4 w-1/6 w-1/8 w-1/10 w-1/12 w-fit w-auto"></div> }
            { <div className="md:w-1/3 md:w-1/4 md:w-1/6 md:w-1/8 md:w-1/10 md:w-1/12 md:w-fit md:w-auto"></div> }
            return (
                <StandardTableHeaderCell colspan={ 1 } text_alignment_class="text-left" column_width_class={ column_width_class } reference_class="mdx-table-row">
                    { children }
                </StandardTableHeaderCell>
            )
        }, 
        td: ({ children }) => (
            <StandardTableDataCell text_alignment_class="text-left" reference_class="mdx-table-row">
                { children }
            </StandardTableDataCell>
        ), 
        ...components,
    }
}