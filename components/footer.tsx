
import styles from './footer.module.scss';

export default function Footer () {
    return (<div className={`${styles['footer']}`}>
        <h2 className={`${styles['footer-text']} my-0`}>Contact:</h2>
        <div className='row g-0 m-0 py-0'>
            <div className='col m-0 py-0'>
                <h4 className={`${styles['footer-text']} my-0`}>LinkedIn</h4>
            </div>
            <div className='col m-0 py-0'>
                <h4 className={`${styles['footer-text']} my-0`}>email</h4>
            </div>
        </div>
    </div>)
};
