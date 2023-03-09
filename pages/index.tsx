
import PageTemplate from '../components/page-template';
import Content from '../components/content';

export default function App (): JSX.Element {
    return (PageTemplate(Content(contentMarkdown, 'markdown')));
};

let contentMarkdown = `
## Home

Aspiring data scientist trained in the macro-econometrics tradition of empirical social science.
- Profile: [LinkedIn](https://www.linkedin.com/in/yeow-chong-goh-3aab5818b/)

## Recently changed

- Configured build steps to create pages from notebook files.
  - [Example](/projects/sg-open-data/marriages-pam-educ).
  - Going to redo this step soon because the current procedure cannot handle more complex \`MDX\` files.
- Restyled using Bootstrap utilities.

## What else am I doing now

- [HackerRank](https://www.hackerrank.com/gohyc1993), [LeetCode](https://leetcode.com/YC-Goh/), [freeCodeCamp](https://www.freecodecamp.org/yc-goh).
  - Focus is on databases, data structures and algorithms.
  - Recently finished: basic data structures (LeetCode), basic SQL (LeetCode \& HackerRank), intermediate SQL (HackerRank).
`;
