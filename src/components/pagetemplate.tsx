import PageTitle from "../components/pagetitle"
import StandardHeaderLink from "./standardlink"

export default function PageTemplate({
    children, 
    pagetitle, 
}:{
    children: React.ReactNode, 
    pagetitle: string, 
}) {
    return (
        <div className="w-9/10 flex flex-col justify-center">
            <div className="p-2 border-b-2 border-sky-100">
                <PageTitle>
                    {pagetitle}
                </PageTitle>
            </div>
            <div className="p-2 flex flex-row justify-center border-b-2 border-sky-100">
                <StandardHeaderLink href="/" padding="px-1">
                    Home
                </StandardHeaderLink>
                <StandardHeaderLink href="/daily" padding="px-1">
                    Daily
                </StandardHeaderLink>
                <StandardHeaderLink href="/weekly" padding="px-1">
                    Weekly
                </StandardHeaderLink>
                <StandardHeaderLink href="/monthly" padding="px-1">
                    Monthly
                </StandardHeaderLink>
            </div>
            <div className="flex flex-row flex-wrap justify-center">
                {children}
            </div>
        </div>
    )
}