import React from 'react'

export default function MdxLayout({ children }: { children: React.ReactNode }) {
    // Create any shared layout or styles here
    return (
        <div className="mx-auto w-full text-left sm:w-5/6 md:w-4/5 lg:w-3/4">
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css"/>
            { children }
        </div>
    )
}