export default function StandardTextBox({
    children, 
    text_alignment_class, 
    reference_class = "standard-title", 
}: {
    children: React.ReactNode, 
    text_alignment_class: string, 
    reference_class?: string, 
}) {
    return (
        <p className={`px-1 text-base font-normal ${text_alignment_class} text-slate-200 ${reference_class}`}>
            {children}
        </p>
    )
}