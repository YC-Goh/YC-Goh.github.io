
import * as React from 'react';
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkGfm from 'remark-gfm';
import remarkRehype from 'remark-rehype';
import rehypeSanitize from 'rehype-sanitize';
import rehypeReact from 'rehype-react';

export default function Content (markdownSchema: string) {
    let componentSchema = unified()
    .use(remarkParse)
    .use(remarkGfm)
    .use(remarkRehype)
    .use(rehypeSanitize)
    .use(rehypeReact, {
        createElement: React.createElement
    })
    .processSync(markdownSchema)
    .result;
    return (
        <div className='row p-0 m-0'>
            {componentSchema}
        </div>
    )
};
