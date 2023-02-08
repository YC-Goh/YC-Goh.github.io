
import Header from '../components/header';
import style from './index.module.scss';
import * as React from 'react';

export default function App () {
    let bodyText: React.ReactNode[] = [];
    for (let i = 0; i < 1000; i++) {
        bodyText.push(<p key={`key-${i}`}>Hello World</p>)
    }
    return (<div className={`${style['app']} container`}>
        <Header />
        <div className={`row`}>
            <div className={`col`}>
                {bodyText}
            </div>
        </div>
    </div>)
};
