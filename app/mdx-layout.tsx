import React from 'react'

export function RowLayout({ children }: { children: React.ReactNode }) {
    return (
        <div className="flex flex-row py-2">
            { children }
        </div>
    )
}

export function LeftCellLayout({ children }: { children: React.ReactNode }) {
    return (
        <div className="text-right flex flex-col w-1/2 px-2">
            { children }
        </div>
    )
}

export function RightCellLayout({ children }: { children: React.ReactNode }) {
    return (
        <div className="text-left flex flex-col w-1/2 px-2 py-1">
            { children }
        </div>
    )
}

export default function MdxLayout({ children }: { children: React.ReactNode }) {
    // Create any shared layout or styles here
    return (
        <div className="flex flex-col text-center mx-auto w-full sm:w-5/6 md:w-4/5 lg:w-3/4">
            { children }
        </div>
    )
}