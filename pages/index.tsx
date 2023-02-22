
import PageTemplate from '../components/page-template';
import Content from '../components/content';

export default function App () {
    return (PageTemplate(Content(contentMarkdown, 'markdown')));
};

let contentMarkdown = `
## Hello Home

This is my home page.
Details will be filled in later.

## Recently changed

- I have configured the build steps to create pages from notebook files. You can see the first example [here](/data-projects/sg-marriages-pam).
`;
