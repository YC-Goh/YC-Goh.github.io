import Link from "next/link"

export default function StandardLink({
    children, 
    href, 
    padding_class, 
    text_size_class, 
    text_alignment_class, 
    reference_class = "standard-title", 
}: {
    children: React.ReactNode, 
    href: string, 
    padding_class: string, 
    text_size_class: string, 
    text_alignment_class: string, 
    reference_class?: string, 
}) {
    return (
        <Link className={ `${ padding_class } ${ text_size_class } font-normal ${ text_alignment_class } text-slate-200 hover:text-sky-100 ${ reference_class }`} href={`${ href }` }>
            { children }
        </Link>
    )
}