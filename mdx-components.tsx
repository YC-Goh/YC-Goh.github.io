import type { MDXComponents } from 'mdx/types'

export function useMDXComponents(components: MDXComponents): MDXComponents {
  return {
    h1: ({ children }) => <h1 className="text-5xl py-2">{ children }</h1>,
    h2: ({ children }) => <h2 className="text-xl py-2">{ children }</h2>,
    h3: ({ children }) => <h3 className="text-lg py-2">{ children }</h3>,
    p: ({ children }) => <p className="text-xs">{ children }</p>,
    a: (props) => <a className="hover:text-slate-500" {...props}/>,
    ol: ({ children }) => <ol className="list-decimal px-4 py-2">{ children }</ol>,
    ul: ({ children }) => <ul className="list-disc px-4 py-2">{ children }</ul>,
    li: ({ children }) => <li className="text-xs">{ children }</li>,
    ...components
  }
}