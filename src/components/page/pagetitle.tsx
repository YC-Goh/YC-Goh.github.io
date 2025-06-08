import StandardTitle from "../standard/standardtitle"

export default function PageTitle({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <StandardTitle margin_class="" text_size_class="text-4xl md:text-5xl" text_alignment_class="text-center" reference_class="page-title">
            {children}
        </StandardTitle>
    )
}