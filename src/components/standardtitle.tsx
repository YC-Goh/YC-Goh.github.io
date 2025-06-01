export default function StandardTitle({
    children,
    text_size_class,
    text_alignment_class
}: {
    children: React.ReactNode,
    text_size_class: string,
    text_alignment_class: string
}) {
    return (
        <h1 className={`${text_size_class} font-medium ${text_alignment_class} text-sky-200`}>
            {children}
        </h1>
    )
}