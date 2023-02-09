
import styles from './footer.module.scss';
import { faEnvelope, IconDefinition } from '@fortawesome/free-regular-svg-icons';
import { faLinkedin, faGithub } from '@fortawesome/free-brands-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

export default function Footer () {
    return (<div className={`${styles['footer']}`}>
        <div className='row p-0 m-0'>
            <div className='col-4 p-3 m-0'>
                <h2 className={`${styles['footer-section']} p-0 m-0`}>Contact:</h2>
                {FooterLinkedIcon('', faEnvelope)}
            </div>
            <div className='col-4 p-3 m-0'>
                <h2 className={`${styles['footer-section']} p-0 m-0`}>Profile:</h2>
                {FooterLinkedIcon('https://www.linkedin.com/in/yeow-chong-goh-3aab5818b/', faLinkedin)}
                {FooterLinkedIcon('https://github.com/YC-Goh', faGithub)}
            </div>
        </div>
    </div>)
};

function FooterLinkedIcon (link: string, iconName: IconDefinition) {
    return (
        <a href={link} className={styles['footer-link']}>
            <FontAwesomeIcon icon={iconName} className={styles['footer-icon']} />
        </a>
    );
};
