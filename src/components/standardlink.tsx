import Link from "next/link"

export default function StandardLink({
    children, 
    href, 
    padding, 
}: {
    children: React.ReactNode, 
    href: string, 
    padding: string, 
}) {
    return (
        <Link className={`${padding} text-base font-normal text-center text-slate-200`} href={`${href}`}>
            {children}
        </Link>
    )
}