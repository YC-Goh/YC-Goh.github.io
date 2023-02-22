
import PageTemplate from '../components/page-template';
import Content from '../components/content';

export default function App () {
    return (PageTemplate(Content(contentMarkdown, 'markdown')));
};

let contentMarkdown = `
## Hello TODOs

1. Update projects with planned projects.
2. Further update page styling at some point to make use of bootstrap colour themes.
`;
