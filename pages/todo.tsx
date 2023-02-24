
import PageTemplate from '../components/page-template';
import Content from '../components/content';

export default function App (): JSX.Element {
    return (PageTemplate(Content(contentMarkdown, 'markdown')));
};

let contentMarkdown = `
## TODO:

- Update projects with planned projects, maybe after actually getting some progress.
- Redo colour scheme of the main content area, but this is not that important now.
`;
