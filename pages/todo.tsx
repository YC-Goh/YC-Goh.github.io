
import PageTemplate from '../components/page-template';
import Content from '../components/content';

export default function App () {
    return (PageTemplate(Content(contentMarkdown)));
};

let contentMarkdown = `
## Hello TODOs

1. Use plugins to alter properties of HTML tags generated through the unified.js remark-rehype process.
2. Use tag properties to style page contents using Bootstrap.js + SCSS.
3. Update the projects page with actual content and planned projects.
4. Incorporate notebook and math/LaTeX rendering for future project.
`;
