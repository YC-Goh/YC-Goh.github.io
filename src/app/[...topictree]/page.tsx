import React from "react"
import ContentTemplate from "../../components/page/contenttemplate"
import generateStaticParamsGenerator from "../../components/functions/generateStaticParams"
import generateFileTreeGenerator from "../../components/functions/generateFileTree"

export const generateStaticParams = generateStaticParamsGenerator("topictree", "src/content")

export default async function Page({
    params, 
}: {
    params: Promise<{ topictree: Array<string> }>
}) {
    const { topictree } = await params
    const [ topic,  ..._ ] = topictree
    const page_path = topictree.join("/")

    let Post: React.FC
    try {
        ({ default: Post} = await import(`/src/content/${page_path}.mdx`))
    } catch (e) {
        ({ default: Post} = await import(`/src/content/${page_path}.md`))
    }

    const filetree = await generateFileTreeGenerator("src/content", topic)()

    return (
        <ContentTemplate>
            {[
                filetree, 
                <Post />, 
            ]}
        </ContentTemplate>
    )
}