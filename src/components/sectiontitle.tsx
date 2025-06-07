import StandardTitle from "./standardtitle"

export default function SectionTitleLeftColumn({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <StandardTitle text_size_class="text-3xl" text_alignment_class="text-right" reference_class="section-title-left-col">
            {children}
        </StandardTitle>
    )
}

export function SectionTitleRightColumn({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <StandardTitle text_size_class="text-3xl" text_alignment_class="text-left" reference_class="section-title-right-col">
            {children}
        </StandardTitle>
    )
}