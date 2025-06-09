import StandardLink from "../standard/standardlink"

export default function SectionLink({
    children, 
    href, 
}: {
    children: React.ReactNode, 
    href: string, 
}) {
    return (
        <StandardLink padding_class="px-0" text_size_class="text-sm md:text-base" text_alignment_class="text-left" href={ href } reference_class="section-link">
            {children}
        </StandardLink>
    )
}