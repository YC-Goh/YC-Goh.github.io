import StandardTable from "../standard/standardtableelems"

export default function SectionTextTable({
    children, 
    headers, 
    data, 
}: {
    children: React.ReactNode, 
    headers: Array<[number, string|number|boolean]>, 
    data: Array<Array<string|number|boolean>>, 
}) {
    return (
        <StandardTable headers={ headers } data={ data }>{ children }</StandardTable>
    )
}