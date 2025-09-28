import PageTemplate from "../../components/page/pagetemplate"
import generateStaticParamsGenerator from "../../components/functions/generateStaticParams"

export const generateStaticParams = generateStaticParamsGenerator("topictree", "src/content")

export default async function PageLayout({
    children, 
    params, 
}: {
    children: React.ReactNode, 
    params: Promise<{ topictree: Array<string> }>, 
}) {
    const { topictree } = await params
    const [ topic,  ..._ ] = topictree
    
    let page_title: string
    switch (topic) {
        case "reads":
            page_title = "Fun Reads"
            break;
        case "projects":
            page_title = "Projects"
            break;
        default:
            page_title = "Where Is This?"
    }

    return (
        <PageTemplate pagetitle={ page_title }>
            { children }
        </PageTemplate>
    )
}