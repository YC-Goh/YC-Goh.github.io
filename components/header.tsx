
import styles from './header.module.scss';

export default function Header () {
    return (<div className={styles.header}>
        <h2 className={styles.title}>Hello World!</h2>
        <div className={styles.menu}>
            <a><p>Home</p></a>
            <p>|</p>
            <a><p>Projects</p></a>
            <p>|</p>
            <a><p>TODO</p></a>
        </div>
    </div>);
};
