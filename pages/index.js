
import Header from '../components/header.tsx';
import style from './index.module.scss';

export default function App () {
    return (<div className={style.app}>
        <h1>Welcome!</h1>
        <Header />
    </div>)
};
