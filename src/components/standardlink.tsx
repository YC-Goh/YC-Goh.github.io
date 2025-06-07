import Link from "next/link"

export default function StandardLink({
    children, 
    href, 
    padding, 
    reference_class = "standard-title", 
}: {
    children: React.ReactNode, 
    href: string, 
    padding: string, 
    reference_class?: string, 
}) {
    return (
        <Link className={`${padding} text-base font-normal text-center text-slate-200 ${reference_class}`} href={`${href}`}>
            {children}
        </Link>
    )
}