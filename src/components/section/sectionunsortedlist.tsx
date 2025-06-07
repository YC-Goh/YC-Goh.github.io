import StandardUnsortedList from "../standard/standardunsortedlist"

export default function SectionUnsortedList({
    children, 
}: {
    children: React.ReactNode, 
}) {
    return (
        <StandardUnsortedList text_alignment_class="text-left" reference_class="section-unsorted-list">
            {children}
        </StandardUnsortedList>
    )
}