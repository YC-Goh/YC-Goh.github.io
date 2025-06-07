import Link from "next/link"

export default function StandardLink({
    children, 
    href, 
    padding_class, 
    text_alignment_class, 
    reference_class = "standard-title", 
}: {
    children: React.ReactNode, 
    href: string, 
    padding_class: string, 
    text_alignment_class: string, 
    reference_class?: string, 
}) {
    return (
        <Link className={`${padding_class} text-sm sm:text-base font-normal ${text_alignment_class} text-slate-200 ${reference_class}`} href={`${href}`}>
            {children}
        </Link>
    )
}