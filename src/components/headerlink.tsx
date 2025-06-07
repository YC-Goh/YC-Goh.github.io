import StandardLink from "./standardlink"

export default function HeaderLink({
    children, 
    href, 
}: {
    children: React.ReactNode, 
    href: string, 
}) {
    return (
        <StandardLink href={`${href}`} padding="px-4" reference_class="header-link">
            {children}
        </StandardLink>
    )
}