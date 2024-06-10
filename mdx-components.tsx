import type { MDXComponents } from 'mdx/types'

export function useMDXComponents(components: MDXComponents): MDXComponents {
  return {
    h1: ({ children }) => <h1 className="text-5xl py-2">{ children }</h1>,
    h2: ({ children }) => <h2 className="text-xl py-2">{ children }</h2>,
    h3: ({ children }) => <h3 className="text-lg py-2">{ children }</h3>,
    p: ({ children }) => <p className="text-xs py-1">{ children }</p>,
    a: (props) => <a className="hover:text-slate-500" {...props}/>,
    ol: ({ children }) => <ol className="list-decimal px-4 py-2">{ children }</ol>,
    ul: ({ children }) => <ul className="list-disc px-4 py-2">{ children }</ul>,
    li: ({ children }) => <li className="text-xs">{ children }</li>,
    code: ({ children }) => <div className="text-xs px-2 py-2 my-2 bg-slate-800 text-wrap">{ children }</div>,
    table: ({ children }) => <table className="text-xs text-center">{ children }</table>,
    thead: ({ children }) => <thead className="border-solid border-y-2 border-white">{ children }</thead>,
    tbody: ({ children }) => <tbody className="border-solid border-y-2 border-white">{ children }</tbody>,
    tr: ({ children }) => <tr className="first:*:text-left *:px-1">{ children }</tr>,
    ...components
  }
}