
import Content from '../components/content';
import PageTemplate from '../components/page-template';

export default function App () {
    return (PageTemplate(
        Content('Hello TODO')
    ));
};
