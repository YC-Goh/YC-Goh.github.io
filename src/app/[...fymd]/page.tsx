import React from "react"
import ContentTemplate from "../../components/page/contenttemplate"
import generateStaticParamsGenerator from "../../components/functions/generateStaticParams"
import generateFileTreeGenerator from "../../components/functions/generateFileTree"

export const generateStaticParams = generateStaticParamsGenerator("src/code")

export default async function Page({
    params, 
}: {
    params: Promise<{ fymd: Array<string> }>
}) {
    const { fymd } = await params
    const [ freq,  ..._ ] = fymd
    const page_path = fymd.join("/")

    let Post: React.FC
    try {
        ({ default: Post} = await import(`/src/code/${page_path}.mdx`))
    } catch (e) {
        ({ default: Post} = await import(`/src/code/${page_path}.md`))
    }

    const filetree = await generateFileTreeGenerator("src/code", freq)()

    return (
        <ContentTemplate>
            {[
                filetree, 
                <Post key={2} />, 
            ]}
        </ContentTemplate>
    )
}