import StandardTextBox from "../standard/standardtextbox"

export default function SectionTextBoxLeftColumn({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <StandardTextBox text_size_class="text-sm md:text-base" text_alignment_class="text-right" reference_class="section-textbox-left-col">
            {children}
        </StandardTextBox>
    )
}

export function SectionTextBoxRightColumn({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <StandardTextBox text_size_class="text-sm md:text-base" text_alignment_class="text-left" reference_class="section-textbox-right-col">
            {children}
        </StandardTextBox>
    )
}