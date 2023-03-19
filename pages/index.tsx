
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
  - Doing: Databases (HackerRank)
  - Done: basic data structures (LeetCode), basic algorithms (LeetCode), basic SQL (LeetCode/HackerRank), intermediate SQL (HackerRank).
- Doing the [SQL tutorial](https://mode.com/sql-tutorial/introduction-to-sql/) on Mode Analytics.
  - Course requirement in this DS/AI course.
  - Forgot to do each example exercise in a separate query (even though it is pointless: the answers are also given and public).
- Doing the [Data Science in Python Boot Camp](https://www.udemy.com/course/the-data-science-course-complete-data-science-bootcamp/) on Udemy.
  - As an additional supplement to the DS/AI course.
  - For the certification as well to show on LinkedIn.
  - Because it is free via the [National Library Board](https://eresources.nlb.gov.sg/main) subscription to Udemy.
- Playing with [Tableau](https://public.tableau.com/app/profile/goh.yeow.chong).
  - Started because of some assignments in this DS/AI course but going to just do some of my own because why not.
`;
