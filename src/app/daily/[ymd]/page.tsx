import PageTemplate from "../../../components/pagetemplate"
import { SectionTextBoxRightColumm } from "../../../components/sectiontextbox"

export async function generateStaticParams() {
  return [{ ymd: 'test' }, ]
}

export default async function Page({
    params, 
}: {
    params: Promise<{ ymd: string }>
}) {
    const { ymd } = await params
    const { default: Post } = await import(`/src/code/daily/${ymd}.mdx`)
    
    return (
        <PageTemplate pagetitle="No Commentary">
            <Post />
        </PageTemplate>
    )
}