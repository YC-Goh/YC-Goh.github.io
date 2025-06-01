import StandardTitle from "./standardtitle"

export default function PageTitle({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <StandardTitle sizevalue="5" alignment="center">
            {children}
        </StandardTitle>
    )
}