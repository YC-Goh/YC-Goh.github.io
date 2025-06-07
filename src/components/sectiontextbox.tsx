import StandardTextBox from "./standardtextbox"

export default function SectionTextBoxLeftColumn({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <StandardTextBox text_alignment_class="text-right" reference_class="section-textbox-left-col">
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
        <StandardTextBox text_alignment_class="text-left" reference_class="section-textbox-right-col">
            {children}
        </StandardTextBox>
    )
}