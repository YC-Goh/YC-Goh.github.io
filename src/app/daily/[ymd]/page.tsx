import PageTemplate from "../../../components/pagetemplate"
import { SectionTextBoxRightColumm } from "../../../components/sectiontextbox"

export async function generateStaticParams() {
  return [{ ymd: '1' }, { ymd: '2' }, { ymd: '3' }]
}

export default async function Page({
    params, 
}: {
    params: Promise<{ ymd: string }>
}) {
    const { ymd } = await params
    return (
        <PageTemplate pagetitle="No Commentary">
            <SectionTextBoxRightColumm>
                {ymd}
            </SectionTextBoxRightColumm>
        </PageTemplate>
    )
}