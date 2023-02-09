
import PageTemplate from '../components/page-template';

function TestBody () {
    return (<h1>
        Projects Page
    </h1>);
};

export default function App () {
    return (PageTemplate(TestBody));
};
