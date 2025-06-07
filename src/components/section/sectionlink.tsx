import StandardLink from "../standard/standardlink"

export default function SectionLink({
    children, 
    href, 
}: {
    children: React.ReactNode, 
    href: string, 
}) {
    return (
        <StandardLink href={`${href}`} padding_class="px-0" text_alignment_class="text-left" reference_class="section-link">
            {children}
        </StandardLink>
    )
}