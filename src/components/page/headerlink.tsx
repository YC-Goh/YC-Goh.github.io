import StandardLink from "../standard/standardlink"

export default function HeaderLink({
    children, 
    href, 
}: {
    children: React.ReactNode, 
    href: string, 
}) {
    return (
        <StandardLink padding_class="px-4" text_size_class="text-sm md:text-base" text_alignment_class="text-center" href={ href } reference_class="header-link">
            {children}
        </StandardLink>
    )
}