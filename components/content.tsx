
import * as React from 'react';
import { unified } from 'unified';
import { visit } from 'unist-util-visit';
import { is } from 'unist-util-is';
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

let mathSanitizeSchema = {...defaultSchema};

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
        visit(tree, 'element', function (node, index, parent) {
            if (node.properties == null) {
                node.properties = {};
            };
            node.properties.id = `content-${node.tagName}-${index}`;
            node.properties.key = node.properties.id;
            if (!node.properties.className) {
                node.properties.className = []
            } else if (!Array.isArray(node.properties.className)) {
                node.properties.className = [node.properties.className.toString()];
            }
            switch (node.tagName) {
                case 'h1':
                    node.properties.className.push(styles['content-page-heading']);
                    break;
                case 'h2':
                    node.properties.className.push(styles['content-content-heading']);
                    break
                case 'h3':
                    node.properties.className.push(styles['content-section-heading']);
                    break;
                case 'h4':
                    node.properties.className.push(styles['content-subsection-heading']);
                    break;
                case 'p':
                    if (node.children.some(
                        (child) => is(child, {type: 'text'})
                    )) {
                        node.properties.className.push(styles['content-text-content']);
                    } else if (node.children.some(
                        (child) => is(child, {type: 'element', tagName: 'img'})
                    )) {
                        node.tagName = 'div';
                        node.properties.className.push(styles['content-image-wrapper']);
                    };
                    break;
                case 'a':
                    node.properties.className.push(styles['content-text-link']);
                    break;
                case 'ul':
                    node.properties.className.push(styles['content-list-unordered']);
                    break;
                case 'ol':
                    node.properties.className.push(styles['content-list-ordered']);
                    break;
                case 'li':
                    node.properties.className.push(styles['content-list-item']);
                    node.properties.className.push(`mx-3`);
                    break;
                case 'pre':
                    node.properties.className.push(styles['content-code-container']);
                    node.properties.className.push('px-3');
                    break;
                case 'code':
                    if (node.properties.className.some(
                        (val) => /^language-[a-z]+/i.test(val as string)
                    )) {
                        node.properties.className.push('p-3');
                    } else {
                        if (is(parent, {type: 'element', tagName: 'pre'})) {
                            if (!parent.properties) {
                                parent.properties = {};
                            };
                            if (!parent.properties.className) {
                                parent.properties.className = [];
                            } else {
                                parent.properties.className = [parent.properties.className.toString()];
                            };
                            parent.tagName = 'p';
                            parent.properties.className.push(styles['content-text-wrapper']);
                        };
                        node.properties.className.push(styles['content-code-text']);
                    };
                    break;
                case 'math':
                case 'mrow':
                case 'msub':
                case 'mfrac':
                    node.properties.className.push(styles['content-math-text']);
                    break;
                case 'div':
                    if (node.children.some(
                        (child) => (is(child, {tagName: 'table'}))
                    )) {
                        node.properties.className.push(styles['content-table-wrapper']);
                    }
                    break;
                case 'table':
                    node.properties.className.push(styles['content-table-container']);
                    break;
                case 'thead':
                    node.properties.className.push(styles['content-table-header']);
                    break;
                case 'tbody':
                    node.properties.className.push(styles['content-table-body']);
                    break;
                case 'tr':
                    node.properties.className.push(styles['content-table-row']);
                    break;
                case 'th':
                case 'td':
                    node.properties.className.push(styles['content-table-cell']);
                    node.properties.className.push('p-1');
                    break;
                default:
                    node.properties.className.push(styles['content-other']);
                    break;
            };
            if (!node.properties.className.some(
                (val) => /p-[0-9]/.test(val as string)
            )) {
                if (!node.properties.className.some(
                    (val) => /px-[0-9]/.test(val as string)
                )) {
                    node.properties.className.push('px-0');
                };
                if (!node.properties.className.some(
                    (val) => /py-[0-9]/.test(val as string)
                )) {
                    node.properties.className.push('py-0');
                };
            }
            if (!node.properties.className.some(
                (val) => /m-[0-9]/.test(val as string)
            )) {
                if (!node.properties.className.some(
                    (val) => /mx-[0-9]/.test(val as string)
                )) {
                    node.properties.className.push('mx-0');
                };
                if (!node.properties.className.some(
                    (val) => /my-[0-9]/.test(val as string)
                )) {
                    node.properties.className.push('my-0');
                };
            }
        });
    };
}

function rehypeSpaceTopElements () {
    return function (tree: Root) {
        visit(tree, 'element', function (node, index, parent) {
            if (is(parent, {type: 'root'})) {
                let nextSiblingOffset = 1;
                let nextSibling = parent.children[index!+nextSiblingOffset];
                while (is(nextSibling, {type: 'text'})) {
                    nextSiblingOffset += 1;
                    nextSibling = parent.children[index!+nextSiblingOffset];
                }
                if (!(is(node, {tagName: 'pre'}) && is(nextSibling, {tagName: 'pre'}))) {
                    if (node.properties!.className) {
                        let classNames = (node.properties!.className as (string|number)[]);
                        let indexPyClass = classNames.indexOf('py-0');
                        if (indexPyClass >= 0) {
                            node.properties!.className = [...classNames.slice(0,indexPyClass), 'pt-0', 'pb-3',...classNames.slice(indexPyClass+1,)]
                        };
                    };
                };
            };
        });
    };
}

function rehypeLinkImgTags () {
    return function (tree: Root) {
        visit(tree, {tagName: 'img'}, function (node) {
            node.properties!.src = `/data-projects/${node.properties!.src}`;
        });
    };
};

export default function Content (contentText: string, format: 'markdown'|'html'): JSX.Element {
    const { createElement, Fragment } = React;
    if (format === 'markdown') {
        return (
            <div className='row p-3 m-0 justify-content-center'>
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
                .use(rehypeSpaceTopElements)
                .use(rehypeLinkImgTags)
                .use(rehypeHighlight)
                .use(rehypeReact, { createElement, Fragment })
                .processSync(contentText)
                .result}
            </div>
        );
    } else {
        return (
            <div className='row p-3 m-0 justify-content-center'>
                {unified()
                .use(rehypeParse, {fragment: true, space: 'html'})
                .use(rehypeRaw)
                .use(rehypeSetStylesRaw)
                .use(rehypeSanitize, mathSanitizeSchema)
                .use(rehypeKatex, {output: 'mathml'})
                .use(rehypeAddAttr)
                .use(rehypeSpaceTopElements)
                .use(rehypeHighlight)
                .use(rehypeReact, { createElement, Fragment })
                .processSync(contentText)
                .result}
            </div>
        );
    }
};
