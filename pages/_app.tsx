
import './next.scss';
import '../node_modules/bootstrap/scss/bootstrap-grid.scss';
import '../node_modules/bootstrap/scss/bootstrap-utilities.scss';
import {ComponentType} from 'react';

export default function App ({Component, pageProps} : {Component: ComponentType, pageProps: {}}) {
    return (<Component {...pageProps} />);
};
