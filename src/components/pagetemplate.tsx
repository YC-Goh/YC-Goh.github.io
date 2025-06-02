import PageTitle from "../components/pagetitle"
import HeaderLink from "./headerlink"

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
            <div className="p-2 flex flex-row justify-center border-b-2 border-sky-100 divide-x-1 divide-sky-100">
                <HeaderLink href="/">
                    Home
                </HeaderLink>
                <HeaderLink href="/daily">
                    Daily
                </HeaderLink>
                <HeaderLink href="/weekly">
                    Weekly
                </HeaderLink>
                <HeaderLink href="/monthly">
                    Monthly
                </HeaderLink>
                <HeaderLink href="https://github.com/yc-goh/yc-goh.github.io">
                    Repo
                </HeaderLink>
            </div>
            <div className="flex flex-row flex-wrap justify-center">
                {children}
            </div>
        </div>
    )
}