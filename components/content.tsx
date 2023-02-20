
import * as React from 'react';
import { unified } from 'unified';
import { visit, Test } from 'unist-util-visit';
import { Node } from 'unist-util-visit/lib';
import remarkParse from 'remark-parse';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import remarkRehype from 'remark-rehype';
import rehypeRaw from 'rehype-raw';
import rehypeParse from 'rehype-parse';
import rehypeSanitize, {defaultSchema} from 'rehype-sanitize';
import rehypeKatex from 'rehype-katex';
import rehypeHighlight from 'rehype-highlight';
import rehypeReact from 'rehype-react';
import { Root, Element } from 'hast';
import styles from './content.module.scss';
import 'highlight.js/styles/github-dark-dimmed.css';

let mathSanitizeSchema = structuredClone(defaultSchema);

if (!mathSanitizeSchema.attributes) {
    mathSanitizeSchema.attributes = {};
};

if (!mathSanitizeSchema.attributes.div) {
    mathSanitizeSchema.attributes.div = [['className', 'math', 'math-display']];
} else {
    mathSanitizeSchema.attributes.div.push(['className', 'math', 'math-display']);
}

if (!mathSanitizeSchema.attributes.span) {
    mathSanitizeSchema.attributes.span = [['className', 'math', 'math-inline']];
} else {
    mathSanitizeSchema.attributes.span.push(['className', 'math', 'math-inline']);
}

if (!mathSanitizeSchema.attributes.code) {
    mathSanitizeSchema.attributes.code = [['className', /^language-[a-z]+/i]];
} else {
    mathSanitizeSchema.attributes.code.push(['className', /^language-[a-z]+/i]);
}

function rehypeSetStylesRaw () {
    return function (tree: Root) {
        visit(tree, {type: 'element', tagName: 'style'}, function (node: Element) {
            for (let i in node.children) {
                node.children[i].type = 'raw';
            };
        });
    };
};

function rehypeAddAttr () {
    return function (tree: Root) {
        visit(tree, 'element', function (node: Element, index) {
            if (node.properties == null) {
                node.properties = {};
            };
            node.properties.id = `content-${node.tagName}-${index}`;
            node.properties.key = node.properties.id;
            switch (node.tagName) {
                case 'h1':
                    node.properties.className = `${styles['content-page-heading']}`
                    break
                case 'h2':
                    node.properties.className = `${styles['content-content-heading']}`
                    break
                case 'h3':
                    node.properties.className = `${styles['content-section-heading']}`
                    break
                case 'h4':
                    node.properties.className = `${styles['content-subsection-heading']}`
                    break
                case 'p':
                    node.properties.className = `${styles['content-text-content']}`
                    break
                case 'a':
                    node.properties.className = `${styles['content-text-link']}`
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
                case 'pre':
                    node.properties.className = `${styles['content-code-container']}`
                    break
                case 'code':
                    if (!node.properties.className) {
                        node.properties.className = `${styles['content-code-text']}`
                    }
                    break
                case 'math':
                case 'mrow':
                case 'msub':
                case 'mfrac':
                    node.properties.className = `${styles['content-math-text']}`
                    break
                case 'table':
                    node.properties.className = `${styles['content-table-container']}`
                    break
                case 'thead':
                    node.properties.className = `${styles['content-table-header']}`
                    break
                case 'tbody':
                    node.properties.className = `${styles['content-table-body']}`
                    break
                case 'tr':
                    node.properties.className = `${styles['content-table-row']}`
                    break
                case 'th':
                case 'td':
                    node.properties.className = `${styles['content-table-cell']}`
                    break
                default:
                    node.properties.className = `${styles['content-other']}`
                    break
            }
    })
    };
}

function rehypeLinkImgTags () {
    return function (tree: Root) {
        visit(tree, {tagName: 'img'}, function (node: Element) {
            node.properties!.src = `/data-projects/${node.properties!.src}`;
        });
    };
};

export default function Content (contentText: string, format: 'markdown'|'html'): JSX.Element {
    if (format === 'markdown') {
        return (
            <div className='row p-0 m-0'>
                {unified()
                .use(remarkParse)
                .use(remarkGfm)
                .use(remarkMath)
                .use(remarkRehype, {allowDangerousHtml: true})
                .use(rehypeRaw)
                .use(rehypeSetStylesRaw)
                .use(rehypeSanitize, mathSanitizeSchema)
                .use(rehypeKatex, {output: 'mathml'})
                .use(rehypeAddAttr)
                .use(rehypeLinkImgTags)
                .use(rehypeHighlight)
                .use(rehypeReact, {createElement: React.createElement})
                .processSync(contentText)
                .result}
            </div>
        );
    } else {
        return (
            <div className='row p-0 m-0'>
                {unified()
                .use(rehypeParse, {fragment: true, space: 'html'})
                .use(rehypeRaw)
                .use(rehypeSetStylesRaw)
                .use(rehypeSanitize, mathSanitizeSchema)
                .use(rehypeKatex, {output: 'mathml'})
                .use(rehypeAddAttr)
                .use(rehypeHighlight)
                .use(rehypeReact, {createElement: React.createElement})
                .processSync(contentText)
                .result}
            </div>
        );
    }
};
