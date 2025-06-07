import React from "react"
import generateStaticParamsGenerator from "../../components/functions/generateStaticParams"

export const generateStaticParams = generateStaticParamsGenerator("src/code")

export default async function Page({
    params, 
}: {
    params: Promise<{ fymd: Array<string> }>
}) {
    const { fymd } = await params
    const page_path = fymd.join("/")
    
    let Post: React.FC
    try {
        ({ default: Post} = await import(`/src/code/${page_path}.mdx`))
    } catch (e) {
        ({ default: Post} = await import(`/src/code/${page_path}.md`))
    }

    return (
        <Post />
    )
}