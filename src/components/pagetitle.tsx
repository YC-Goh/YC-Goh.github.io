import StandardTitle from "./standardtitle"

export default function PageTitle({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <StandardTitle text_size_class="text-5xl" text_alignment_class="text-center">
            {children}
        </StandardTitle>
    )
}