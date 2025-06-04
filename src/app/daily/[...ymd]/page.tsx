import React from "react"
import PageTemplate from "../../../components/pagetemplate"
import { readdir } from "fs/promises"

export async function generateStaticParams() {
    const codeLocationDaily = "src/code/daily/"
    const files = await readdir(codeLocationDaily, { recursive: true, withFileTypes: true }).then(
        (fileList) => fileList.filter(
            (file) => file.isFile()
        ).filter(
            (file) => /\.mdx?$/i.test(file.name)
        ).map(
            (file) => ({ ymd : [...file.parentPath.replace(codeLocationDaily, "").split("/"), file.name.replace(/\.mdx?$/i, "")] })
        )
    )
    return files
}

export default async function Page({
    params, 
}: {
    params: Promise<{ ymd: Array<string> }>
}) {
    const { ymd } = await params
    const [ yyyy, mm, dd ] = ymd
    let Post: React.FC
    try {
        ({ default: Post} = await import(`/src/code/daily/${yyyy}/${mm}/${dd}.mdx`))
    } catch (e) {
        ({ default: Post} = await import(`/src/code/daily/${yyyy}/${mm}/${dd}.md`))
    }
    
    return (
        <PageTemplate pagetitle="No Commentary">
            <Post />
        </PageTemplate>
    )
}