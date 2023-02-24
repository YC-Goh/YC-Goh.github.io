
import styles from './header.module.scss';
import Link from 'next/link';

export default function Header (): JSX.Element {
    let menuLinks: {[index: string]: string} = {'Home':'/', 'Projects':'/projects', 'TODO':'/todo'};
    return (
        <div className={`${styles['header']} sticky-md-top row px-0 py-3 m-0 text-bg-dark`}>
            <nav className={`${styles['header-menu']} p-0 m-0`} role='navigation'>
                <h2 className={`${styles['header-title']} px-3 py-0 m-0`}>
                    YC-Goh
                </h2>
                {Object.keys(menuLinks).map((label) => MenuLink(menuLinks[label], label))}
            </nav>
        </div>
    );
};

function MenuLink (href: string, label: string): JSX.Element {
    return (
        <Link href={href} className={`${styles['header-link']} px-3 py-0 m-0`} key={label}>
            {label}
        </Link>
    )
};
