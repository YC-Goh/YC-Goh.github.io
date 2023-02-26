
import PageTemplate from '../components/page-template';
import Content from '../components/content';

export default function App (): JSX.Element {
    return (PageTemplate(Content(contentMarkdown, 'markdown')));
};

let contentMarkdown = `
## Home

Details will be filled in later.

## Recently changed

- I have configured the build steps to create pages from notebook files.
  - [First example](/projects/sg-open-data/marriages-pam-educ).
- Much of the site has been restyled using Bootstrap utilities.

## What else am I doing now

- Aside from my current course (see LinkedIn): [HackerRank](https://www.hackerrank.com/gohyc1993), [LeetCode](https://leetcode.com/YC-Goh/), [freeCodeCamp](https://www.freecodecamp.org/yc-goh).
  - Focus is on getting up to speed with data structures and algorithms.
`;
