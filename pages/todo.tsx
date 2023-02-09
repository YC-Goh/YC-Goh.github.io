
import PageTemplate from '../components/page-template';
import Content from '../components/content';

export default function App () {
    return (PageTemplate(Content(contentMarkdown)));
};

let contentMarkdown = `
## Hello TODOs

1. Figure out how to add classNames to components generated using Unified.js.
2. Restyle contents using Bootstrap.js + SCSS.
3. Update contents to actual contents.
4. Figure out how Next.js SSG works.
`;
