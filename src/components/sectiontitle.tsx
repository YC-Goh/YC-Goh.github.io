import StandardTitle from "./standardtitle"

export default function SectionTitleLeftColumm({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <StandardTitle sizevalue="3" alignment="right">
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
        <StandardTitle sizevalue="3" alignment="left">
            {children}
        </StandardTitle>
    )
}