export default function StandardTextBox({
    children,
    text_alignment_class
}: {
    children: React.ReactNode,
    text_alignment_class: string
}) {
    return (
        <p className={`px-1 text-base font-normal ${text_alignment_class} text-slate-200`}>
            {children}
        </p>
    )
}