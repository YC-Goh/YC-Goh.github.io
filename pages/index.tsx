
import PageTemplate from '../components/page-template';
import Content from '../components/content';

export default function App (): JSX.Element {
    return (PageTemplate(Content(contentMarkdown, 'markdown')));
};

let contentMarkdown = `
## Home

Aspiring data analyst.

Temporarily cleared the home screen as there is no point displaying such outdated information without proper formatting or contextualisation.

## What am I doing now

0. From a long time ago in industry timeline terms: Configured my website project to automatically build pages from notebook files.
  - [Example](/projects/sg-open-data/marriages-pam-educ).
1. Doing something with Canadian Labour Force Survey data (the public-use version). Exactly what is not clear yet, but I just like toying around with labour force data.
  - [Just finished downloading data](/projects/can-open-data/lfs/0-download).
  - [Preprocess SPSS syntax files to recover value labels](/projects/can-open-data/lfs/1-1-get-value-labels).
  - [Checked for changes in value labels for all syntax files marked as 2023 recode](/projects/can-open-data/lfs/1-2-check-value-labels).
  - [Loaded data to a PostgreSQL database](/projects/can-open-data/lfs/1-3-load-monthly-data).

`;

/*
Aspiring data scientist coming from the more traditional econometrics way of thinking about statistics and inference.
- Profile: 

## Recently changed

- Configured build steps to create pages from notebook files.
  - [Example](/projects/sg-open-data/marriages-pam-educ).
  - Need to redo this step because the current procedure cannot handle more complex \`MDX\` files (on-hold: there are other more urgent things to cover and I don't need to display more complex MDX for now).
- Restyled using Bootstrap utilities.
- Removed projects temporarily: I don't foresee updating it significantly in the short-run (~ 1 month, give or take).

## What else am I doing now

- [HackerRank](https://www.hackerrank.com/gohyc1993), [LeetCode](https://leetcode.com/YC-Goh/).
  - Basic data structures, basic algorithms, basic SQL.
- [SQL tutorial](https://mode.com/sql-tutorial/introduction-to-sql/) on Mode Analytics.
  - Course requirement in this DS/AI course.
  - The answers in the tutorial are given and public.
- [Neo4j tutorial](https://graphacademy.neo4j.com/u/5bbf4d76-7300-4c0f-9adf-3b389d478109/).
- [Data Science in Python Boot Camp](https://www.udemy.com/course/the-data-science-course-complete-data-science-bootcamp/) on Udemy.
  - As a supplement.
  - Done.
  - Free via [National Library Board](https://eresources.nlb.gov.sg/main) subscription to Udemy.
- [freeCodeCamp](https://www.freecodecamp.org/yc-goh).
  - On-Hold: time is not unlimited and there is a lot of ground to cover between even SMM/SML estimation methods and the frontier of DS/ML/AI.
- [Tableau](https://public.tableau.com/app/profile/goh.yeow.chong).
  - Had been on hold but will resume soon.
*/
