
import './next.scss';
import {ComponentType} from 'react';

export default function App ({Component, pageProps} : {Component: ComponentType, pageProps: {}}) {
    return (<Component {...pageProps} />);
};
