import StandardTitle from "./standardtitle"

export default function SectionTitleLeftColumm({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <StandardTitle text_size_class="text-3xl" text_alignment_class="text-right">
            {children}
        </StandardTitle>
    )
}

export function SectionTitleRightColumm({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <StandardTitle text_size_class="text-3xl" text_alignment_class="text-left">
            {children}
        </StandardTitle>
    )
}