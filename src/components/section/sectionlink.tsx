import StandardLink from "../standard/standardlink"

export default function SectionLink({
    children, 
    href, 
}: {
    children: React.ReactNode, 
    href: string, 
}) {
    return (
        <StandardLink href={`${href}`} padding="px-0" reference_class="section-link">
            {children}
        </StandardLink>
    )
}