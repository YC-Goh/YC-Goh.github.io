
import PageTemplate from '../components/page-template';

function TestBody (title: string) {
    return (<h1>
        {title}
    </h1>);
};

export default function App () {
    return (PageTemplate(TestBody('Hello World')));
};
