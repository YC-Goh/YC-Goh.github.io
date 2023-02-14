
import PageTemplate from '../components/page-template';
import Content from '../components/content';

export default function App () {
    return (PageTemplate(Content(contentMarkdown)));
};

let contentMarkdown = `
## Hello TODOs

1. Use class-name and potentially style to style page contents using Bootstrap.js + SCSS.
2. Update the projects page with actual content and planned projects.
3. Incorporate notebook and math/LaTeX rendering for future project.
`;
