
import styles from './header.module.scss';

export default function Header () {
    return (<div className={`${styles['header']} container p-0`}>
        <div className='row g-0 my-0 py-0'>
            <h2 className={`${styles['header-title']}`}>Hello World!</h2>
        </div>
        <div className={`${styles['header-menu']} row g-0 m-0 p-0`}>
            {menuLink('/', 'Home')}
            {menuLink('/', 'Projects')}
            {menuLink('/', 'TODO')}
        </div>
    </div>);
};

function menuLink (href: string, label: string) {
    return (<div className='col g-0 m-0 p-0'>
        <a href={href} className={`${styles['header-menu-link']}`}><p className={`${styles['header-menu-link-label']}`}>{label}</p></a>
    </div>)
};
