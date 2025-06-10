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
    reference_class = "standard-table-row", 
}: {
    children: React.ReactNode, 
    reference_class?: string, 
}) {
    return (
        <tr className={ `${ reference_class }` }>
            { children }
        </tr>
    )
}

export function StandardTableBody({
    children, 
    border_class = "border-y-2 border-sky-200", 
    reference_class = "standard-table-body", 
}: {
    children: React.ReactNode, 
    border_class?: string, 
    reference_class?: string, 
}) {
    return (
        <tbody className={ `${ border_class } ${ reference_class }` }>
            { children }
        </tbody>
    )
}

export function StandardTableHead({
    children, 
    border_class = "border-y-2 border-sky-200", 
    reference_class = "standard-table-head", 
}: {
    children: React.ReactNode, 
    border_class?: string, 
    reference_class?: string, 
}) {
    return (
        <thead className={ `${ border_class } ${ reference_class }` }>
            { children }
        </thead>
    )
}

export default function StandardTable({
    children, 
    border_class = "border-y-2 border-sky-200", 
    reference_class = "standard-table", 
}: {
    children: React.ReactNode, 
    border_class?: string, 
    reference_class?: string, 
}) {

    return (
        <table className={ `table-fixed ${ border_class } ${ reference_class }` }>
            { children }
        </table>
    )
}

export function StandardCaptionedTable({
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
            return (<StandardTableRow key={ `row-${ rownum }` }>{ values_nodes }</StandardTableRow>)
        }
    )

    return (
        <table className={ `table-fixed ${ border_class } ${ reference_class }` }>
            <StandardTableCaption text_alignment_class="text-left">{ children }</StandardTableCaption>
            <StandardTableHead border_class={ border_class } reference_class={ `${ reference_class }-head` }>
                <StandardTableRow>
                    { header_nodes }
                </StandardTableRow>
            </StandardTableHead>
            <StandardTableBody border_class={ border_class } reference_class={ `${ reference_class }-body` }>
                { data_nodes }
            </StandardTableBody>
        </table>
    )
}