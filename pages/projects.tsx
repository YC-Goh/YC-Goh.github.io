
import PageTemplate from '../components/page-template';
import Content from '../components/content';

export default function App () {
    return (PageTemplate(Content(contentMarkdown)));
};

let contentMarkdown = `
## Hello Projects

This is my projects page.
Details will be filled in later.
`;
