
import styles from './header.module.scss';

export default function Header () {
    return (<div className={`${styles['header']} sticky-sm-top`}>
        <div className='row g-0'>
            <h1 className={`${styles['header-title']}`}>Hello World!</h1>
        </div>
        <nav className={`${styles['header-menu']} navbar row g-0`}>
            {menuLink('/', 'Home')}
            {menuLink('/', 'Projects')}
            {menuLink('/', 'TODO')}
        </nav>
    </div>);
};

function menuLink (href: string, label: string) {
    return (<div className='col g-0'>
        <a href={href} className={`${styles['header-menu-link']}`}>
            <h4 className={`${styles['header-menu-link-label']}`}>{label}</h4>
        </a>
    </div>)
};
