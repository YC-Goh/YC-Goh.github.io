export default function StandardUnsortedList({
    children, 
    text_alignment_class, 
    list_type = "list-disc", 
    reference_class = "standard-title", 
}: {
    children: React.ReactNode, 
    text_alignment_class: string, 
    list_type?: string, 
    reference_class?: string, 
}) {
    return (
        <ul className={`ml-4 text-sm sm:text-base font-normal ${text_alignment_class} ${list_type} text-slate-200 ${reference_class}`}>
            {children}
        </ul>
    )
}