export default function StandardTitle({
    children, 
    margin_class, 
    text_size_class, 
    text_alignment_class, 
    reference_class = "standard-title", 
}: {
    children: React.ReactNode, 
    margin_class: string, 
    text_size_class: string, 
    text_alignment_class: string, 
    reference_class?: string, 
}) {
    return (
        <h1 className={`${ margin_class } ${ text_size_class } font-medium ${ text_alignment_class } text-sky-200 ${ reference_class }` }>
            { children }
        </h1>
    )
}

export function StandardSubtitle({
    children, 
    margin_class, 
    text_size_class, 
    text_alignment_class, 
    reference_class = "standard-title", 
}: {
    children: React.ReactNode, 
    margin_class: string, 
    text_size_class: string, 
    text_alignment_class: string, 
    reference_class?: string, 
}) {
    return (
        <h2 className={`${ margin_class } ${ text_size_class } font-medium ${ text_alignment_class } text-sky-200 ${ reference_class }` }>
            { children }
        </h2>
    )
}

export function StandardHeading({
    children, 
    margin_class, 
    text_size_class, 
    text_alignment_class, 
    reference_class = "standard-title", 
}: {
    children: React.ReactNode, 
    margin_class: string, 
    text_size_class: string, 
    text_alignment_class: string, 
    reference_class?: string, 
}) {
    return (
        <h3 className={`${ margin_class } ${ text_size_class } font-normal underline ${ text_alignment_class } text-sky-200 ${ reference_class }` }>
            { children }
        </h3>
    )
}

export function StandardSubheading({
    children, 
    margin_class, 
    text_size_class, 
    text_alignment_class, 
    reference_class = "standard-title", 
}: {
    children: React.ReactNode, 
    margin_class: string, 
    text_size_class: string, 
    text_alignment_class: string, 
    reference_class?: string, 
}) {
    return (
        <h4 className={`${ margin_class } ${ text_size_class } font-normal italic ${ text_alignment_class } text-sky-200 ${ reference_class }` }>
            { children }
        </h4>
    )
}