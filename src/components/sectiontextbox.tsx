import StandardTextBox from "./standardtextbox"

export default function SectionTextBoxLeftColumm({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <StandardTextBox alignment="right">
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
        <StandardTextBox alignment="left">
            {children}
        </StandardTextBox>
    )
}