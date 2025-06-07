import PageTemplate from "../../components/page/pagetemplate"
import ContentTemplate from "../../components/page/contenttemplate"
import generateStaticParamsGenerator from "../../components/functions/generateStaticParams"

export const generateStaticParams = generateStaticParamsGenerator("src/code")

export default async function PageLayout({
    children, 
    params, 
}: {
    children: React.ReactNode, 
    params: Promise<{ fymd: Array<string> }>, 
}) {
    const { fymd } = await params
    const [ freq,  ..._ ] = fymd
    
    let page_title: string
    switch (freq) {
        case "daily":
            page_title = "No Comments"
            break;
        case "weekly":
            page_title = "Fun Observations"
            break;
        case "monthly":
            page_title = "Data Log"
            break;
        default:
            page_title = "Where Is This?"
    }

    return (
        <PageTemplate pagetitle={ page_title }>
            <ContentTemplate>
                { children }
            </ContentTemplate>
        </PageTemplate>
    )
}