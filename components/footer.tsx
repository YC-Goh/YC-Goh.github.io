
import styles from './footer.module.scss';
import { faEnvelope, IconDefinition } from '@fortawesome/free-regular-svg-icons';
import { faLinkedin, faGithub, faReact, faSass, faBootstrap, faFontAwesome } from '@fortawesome/free-brands-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faN, faT, faU, faX } from '@fortawesome/free-solid-svg-icons';

export default function Footer () {
    return (
        <div className={`${styles['footer']} row p-0 m-0 text-bg-dark`}>
            {FooterSection(
                'Contact:', 
                3, 
                [
                    ['', faEnvelope]
                ]
            )}
            {FooterSection(
                'Profile:', 
                3, 
                [
                    ['https://www.linkedin.com/in/yeow-chong-goh-3aab5818b/', faLinkedin], 
                    ['https://github.com/YC-Goh', faGithub]
                ]
            )}
            {FooterSection(
                'Built with:', 
                6, 
                [
                    ['https://pages.github.com/', faGithub],
                    ['https://nextjs.org/', faN],
                    ['https://reactjs.org/', faReact],
                    ['https://www.typescriptlang.org/', faT],
                    ['https://sass-lang.com/', faSass],
                    ['https://unifiedjs.com/', faU],
                    ['https://katex.org/docs/node.html', faX],
                    ['https://getbootstrap.com/docs/5.3/layout/grid/', faBootstrap],
                    ['https://fontawesome.com/docs/web/use-with/react/', faFontAwesome]
                ]
            )}
        </div>
    )
};

function FooterSection (sectionName: string, sectionWidth: number, iconProps: [string, IconDefinition][]) {
    return (
        <div className={`col-${sectionWidth} p-3 m-0`}>
            <h3 className={`${styles['footer-section']} p-0 m-0`}>
                {sectionName}
            </h3>
            {iconProps.map(
                ([link, iconName], i) => FooterLinkedIcon(link, iconName, `section-icon-${i}`)
            )}
        </div>
    );
};

function FooterLinkedIcon (link: string, iconName: IconDefinition, key: string) {
    return (
        <a href={link} target='_blank' className={`${styles['footer-link']} px-1 py-0 m-0`}>
            <FontAwesomeIcon 
            icon={iconName} 
            className={styles['footer-icon']} 
            key={key} 
            />
        </a>
    );
};
