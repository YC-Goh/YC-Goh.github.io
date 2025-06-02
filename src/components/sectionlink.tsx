import StandardLink from "./standardlink"

export default function SectionLink({
    children, 
    href, 
}: {
    children: React.ReactNode, 
    href: string, 
}) {
    return (
        <StandardLink href={`${href}`} padding="px-0">
            {children}
        </StandardLink>
    )
}