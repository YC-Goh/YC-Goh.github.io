
import PageTemplate from '../components/page-template';
import Content from '../components/content';

export default function App (): JSX.Element {
    return (PageTemplate(Content(contentMarkdown, 'markdown')));
};

let contentMarkdown = `
## Home

Aspiring data scientist coming from the more traditional econometrics way of thinking about statistics and inference.
- Profile: [LinkedIn](https://www.linkedin.com/in/yeow-chong-goh-3aab5818b/)

## Recently changed

- Configured build steps to create pages from notebook files.
  - [Example](/projects/sg-open-data/marriages-pam-educ).
  - Need to redo this step because the current procedure cannot handle more complex \`MDX\` files (on-hold: there are other more urgent things to cover and I don't need to display more complex MDX for now).
- Restyled using Bootstrap utilities.
- Removed projects temporarily: I don't foresee updating it significantly in the short-run (~ 1 month, give or take).

## What else am I doing now

- [HackerRank](https://www.hackerrank.com/gohyc1993), [LeetCode](https://leetcode.com/YC-Goh/).
  - Doing: database theory.
  - Done: basic data structures, basic algorithms, basic SQL.
- Doing the [SQL tutorial](https://mode.com/sql-tutorial/introduction-to-sql/) on Mode Analytics.
  - Course requirement in this DS/AI course.
  - Forgot to do each example exercise in a separate query (even though it is pointless: the answers are also given and public).
- Doing the [Neo4j tutorial](https://graphacademy.neo4j.com/u/5bbf4d76-7300-4c0f-9adf-3b389d478109/).
- Doing the [Data Science in Python Boot Camp](https://www.udemy.com/course/the-data-science-course-complete-data-science-bootcamp/) on Udemy.
  - As an additional supplement to the DS/AI course.
  - For the certification as well to show on LinkedIn.
  - Because it is free via the [National Library Board](https://eresources.nlb.gov.sg/main) subscription to Udemy.
- [freeCodeCamp](https://www.freecodecamp.org/yc-goh).
  - Kind of on-hold: time is not unlimited and there is a lot of ground to cover between even SMM/SML estimation methods and the frontier of DS/ML/AI.
- Playing with [Tableau](https://public.tableau.com/app/profile/goh.yeow.chong).
  - Started because of some assignments in this DS/AI course but going to just do some of my own because why not.
`;
