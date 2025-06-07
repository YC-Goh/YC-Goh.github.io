import StandardLink from "../standard/standardlink"

export default function HeaderLink({
    children, 
    href, 
}: {
    children: React.ReactNode, 
    href: string, 
}) {
    return (
        <StandardLink href={`${href}`} padding_class="px-4" text_alignment_class="text-center" reference_class="header-link">
            {children}
        </StandardLink>
    )
}