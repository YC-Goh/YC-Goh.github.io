
import * as React from 'react';
import { unified } from 'unified';
import { visit } from 'unist-util-visit';
import remarkParse from 'remark-parse';
import remarkGfm from 'remark-gfm';
import remarkRehype from 'remark-rehype';
import rehypeSanitize from 'rehype-sanitize';
import rehypeReact from 'rehype-react';
import { Root, Element } from 'hast';
import styles from './content.module.scss';

function rehypeAddAttr () {
    return function (tree: Root) {
        visit(tree, 'element', function (node: Element, index) {
            if (node.properties == null) {
                node.properties = {};
            };
            node.properties.id = `content-${node.tagName}-${index}`;
            switch (node.tagName) {
                case 'h1':
                    node.properties.className = `${styles['content-superheading']}`
                    break
                case 'h2':
                    node.properties.className = `${styles['content-heading']}`
                    break
                case 'h3':
                    node.properties.className = `${styles['content-subheading']}`
                    break
                case 'p':
                    node.properties.className = `${styles['content-text']}`
                    break
                case 'ul':
                    node.properties.className = `${styles['content-list-unordered']}`
                    break
                case 'ol':
                    node.properties.className = `${styles['content-list-ordered']}`
                    break
                case 'li':
                    node.properties.className = `${styles['content-list-item']}`
                    break
                default:
                    node.properties.className = `${styles['content-other']}`
                    break
            }
    })
    };
}

export default function Content (markdownSchema: string) {
    let componentSchema = unified()
    .use(remarkParse)
    .use(remarkGfm)
    .use(remarkRehype)
    .use(rehypeSanitize)
    .use(rehypeAddAttr)
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
