export function StandardTableCaption({
    children, 
    text_alignment_class, 
    reference_class = "standard-table-caption", 
}: {
    children: React.ReactNode, 
    text_alignment_class: string, 
    reference_class?: string, 
}) {
    return (
        <caption className={ `text-xs md:text-sm text-bold ${ text_alignment_class } text-slate-200 ${ reference_class }` }>{ children }</caption>
    )
}

export function StandardTableDataCell({
    children, 
    text_alignment_class, 
    reference_class = "standard-table-data-cell", 
}: {
    children: React.ReactNode, 
    text_alignment_class: string, 
    reference_class?: string, 
}) {
    return (
        <td className={ `p-1 text-xs md:text-sm text-normal ${ text_alignment_class } align-top text-slate-200 ${ reference_class }` }>{ children }</td>
    )
}

export function StandardTableHeaderCell({
    children, 
    colspan, 
    text_alignment_class, 
    column_width_class, 
    reference_class = "standard-table-header-cell", 
}: {
    children: React.ReactNode, 
    colspan: number, 
    text_alignment_class: string, 
    column_width_class: string, 
    reference_class?: string, 
}) {
    return (
        <th colSpan={ colspan } className={ `p-1 text-xs md:text-sm text-bold ${ text_alignment_class } ${ column_width_class } text-slate-200 ${ reference_class }` }>{ children }</th>
    )
}

export function StandardTableRow({
    children, 
    border_class = "border-y-2 border-sky-200", 
    reference_class = "standard-table-row", 
}: {
    children: React.ReactNode, 
    border_class?: string, 
    reference_class?: string, 
}) {
    return (
        <tr className={ `${ border_class } ${ reference_class }` }>
            { children }
        </tr>
    )
}

export default function StandardTable({
    children, 
    headers, 
    data, 
    headers_alignment_class = "text-left", 
    data_alignment_class = "text-left", 
    border_class = "border-y-2 border-sky-200", 
    reference_class = "standard-table", 
}: {
    children: React.ReactNode, 
    headers: Array<[number, string, string|number|boolean]>, 
    data: Array<Array<string|number|boolean>>, 
    headers_alignment_class?: string, 
    data_alignment_class?: string, 
    border_class?: string, 
    reference_class?: string, 
}) {

    const header_nodes = headers.map(
        (value, colnum, arr) => (<StandardTableHeaderCell colspan={ value[0] } text_alignment_class={ headers_alignment_class } column_width_class={ value[1] } key={ `header-${ colnum }` }>{ value[2] }</StandardTableHeaderCell>)
    )

    const data_nodes = data.map(
        (values, rownum, _) => {
            const values_nodes = values.map(
                (value, colnum, _) => (<StandardTableDataCell text_alignment_class={ data_alignment_class } key={ `data-${ rownum }-${ colnum }` }>{ value }</StandardTableDataCell>)
            )
            return (<StandardTableRow border_class="" key={ `row-${ rownum }` }>{ values_nodes }</StandardTableRow>)
        }
    )

    return (
        <table className={ `table-fixed ${ border_class } ${ reference_class }` }>
            <StandardTableCaption text_alignment_class="text-left">{ children }</StandardTableCaption>
            <thead>
                <StandardTableRow>
                    { header_nodes }
                </StandardTableRow>
            </thead>
            <tbody>
                { data_nodes }
            </tbody>
        </table>
    )
}