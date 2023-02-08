
import PageTemplate from '../components/page-template';
import * as React from 'react';

export default function App () {
    let bodyText: JSX.Element[] = [];
    for (let i = 0; i < 1000; i++) {
        bodyText.push(<p key={`key-${i}`}>Hello World</p>)
    }
    return (PageTemplate(bodyText));
};
