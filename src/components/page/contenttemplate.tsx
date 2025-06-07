export default function ContentTemplate({
    children, 
}:{
    children: React.ReactNode, 
}) {
    return (
        <div className="flex flex-row flex-wrap justify-center w-9/10 divide-x-2 divide-sky-100">
            <div className="flex flex-col flex-nowrap w-1/8 p-2">
                { children[0] }
            </div>
            <div className="flex flex-col flex-nowrap w-5/8 p-2">
                { children[1] }
            </div>
            <div className="flex flex-col flex-nowrap w-1/8 p-2">
            </div>
        </div>
    )
}