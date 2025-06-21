import PageTemplate from "../../components/page/pagetemplate"
import generateStaticParamsGenerator from "../../components/functions/generateStaticParams"

export const generateStaticParams = generateStaticParamsGenerator("topictree", "src/code")

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
        case "narratives":
            page_title = "Narratives About the World"
            break;
        case "rants":
            page_title = "Assorted Rants"
            break;
        case "reads":
            page_title = "Fun Reads"
            break;
        case "data":
            page_title = "Data Log"
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