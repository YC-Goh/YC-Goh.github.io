import StandardTextBox from "./standardtextbox"

export default function SectionTextBoxLeftColumm({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <StandardTextBox text_alignment_class="text-right">
            {children}
        </StandardTextBox>
    )
}

export function SectionTextBoxRightColumm({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <StandardTextBox text_alignment_class="text-left">
            {children}
        </StandardTextBox>
    )
}