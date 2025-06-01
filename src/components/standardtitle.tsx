export default function StandardTitle({
    children,
    sizevalue,
    alignment
}: {
    children: React.ReactNode,
    sizevalue: string,
    alignment: string
}) {
    return (
        <h1 className={`text-${sizevalue}xl font-medium text-${alignment} text-sky-200`}>
            {children}
        </h1>
    )
}