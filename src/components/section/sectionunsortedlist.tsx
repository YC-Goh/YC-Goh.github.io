import StandardList from "../standard/standardlist"

export default function SectionUnsortedList({
    children, 
}: {
    children: React.ReactNode, 
}) {
    return (
        <StandardList text_alignment_class="text-left" list_type="list-disc" reference_class="section-unsorted-list">
            {children}
        </StandardList>
    )
}