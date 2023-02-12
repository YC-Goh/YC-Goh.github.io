
import PageTemplate from '../components/page-template';
import Content from '../components/content';

export default function App () {
    return (PageTemplate(Content(contentMarkdown)));
};

let contentMarkdown = `
## Hello Home

This is my home page.
Details will be filled in later.

The terrible blue colouring is not permanent.
`;
