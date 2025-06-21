import PageTitle from "./pagetitle"
import HeaderLink from "./headerlink"

export default function PageTemplate({
    children, 
    pagetitle, 
}:{
    children: React.ReactNode, 
    pagetitle: string, 
}) {
    return (
        <div className="w-1/1 lg:w-9/10 flex flex-col justify-center">
            <div className="p-2 border-b-2 border-sky-100">
                <PageTitle>
                    { pagetitle }
                </PageTitle>
            </div>
            <div className="p-2 flex flex-row justify-center border-b-2 border-sky-100 divide-x-1 divide-sky-100">
                <HeaderLink href="/">Home</HeaderLink>
                <HeaderLink href="/narratives">Narratives</HeaderLink>
                <HeaderLink href="/rants">Rants</HeaderLink>
                <HeaderLink href="/reads">Reads</HeaderLink>
                <HeaderLink href="/data">Data</HeaderLink>
                <HeaderLink href="https://github.com/yc-goh/yc-goh.github.io">Repo</HeaderLink>
            </div>
            <div className="flex flex-row flex-wrap justify-center">
                { children }
            </div>
        </div>
    )
}