export default function StandardTextBox({
    children,
    alignment
}: {
    children: React.ReactNode,
    alignment: string
}) {
    return (
        <h1 className={`px-1 text-base font-normal text-${alignment} text-slate-200`}>
            {children}
        </h1>
    )
}