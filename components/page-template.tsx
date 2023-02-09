
import Header from './header';
import styles from './page-template.module.scss';
import * as React from 'react';

export default function PageTemplate (Content: JSX.Element | JSX.Element[] | (() => JSX.Element | JSX.Element[])) {
    if (typeof Content === 'function') {
        Content = Content();
    }
    return (<div className={`${styles['app']} container p-0 my-0`}>
        <Header />
        {Content}
    </div>);
};
