
import styles from './header.module.scss';
import Link from 'next/link';

export default function Header () {
    return (<div className={`${styles['header']} sticky-sm-top`}>
        <div className='row g-0'>
            <h1 className={`${styles['header-title']}`}>Hello World!</h1>
        </div>
        <nav className={`${styles['header-menu']} navbar row g-0`}>
            {MenuLink('/', 'Home')}
            {MenuLink('/projects', 'Projects')}
            {MenuLink('/todo', 'TODO')}
        </nav>
    </div>);
};

function MenuLink (href: string, label: string) {
    return (<div className='col g-0'>
        <Link href={href} className={`${styles['header-menu-link']}`}>
            <h4 className={`${styles['header-menu-link-label']}`}>{label}</h4>
        </Link>
    </div>)
};
