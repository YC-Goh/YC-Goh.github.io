import { StandardCaptionedTable } from "../standard/standardtableelems"

export default function SectionTextTable({
    children, 
    headers, 
    data, 
}: {
    children: React.ReactNode, 
    headers: Array<[number, string, string|number|boolean]>, 
    data: Array<Array<string|number|boolean>>, 
}) {
    return (
        <StandardCaptionedTable headers={ headers } data={ data }>{ children }</StandardCaptionedTable>
    )
}