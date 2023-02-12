
# YC-Goh Personal Website

## What?

This is the repository containing the source code and static webpage files for my personal website.

## Stack

This website uses the following web technologies:
- Github Pages + Actions: This is a small static site, which web hosting needs requires exactly the solution that GitHub Pages provides.
- Next.js: This replaces webpack.js and its loaders for transpiling and bundling project assets with a focus on generating front-end apps using the React.js framework as well as Node.js for running and managing development and production servers.
- React.js: This is the framework that the Next.js transpiler/compiler/bundler assumes. This website is built primarily using functional components as recommended by React.js, with Redux.js and React-Redux ready to be incorporated for any future stateful use-cases.
- Unified.js: Having to write entire blocks of text in HTML or JSX can be painful due to all the extra boilerplate such as tags. For my case, it isn't clear that the ability to customise each text block individually from writing each tag individually is all that valuable. Unified.js lets me write my contents in MarkDown in the vast majority of cases where I expect to style my contents in a fairly uniform way.
- TypeScript: It is important to ensure that functions work as expected and do not return unexpected types. In addition, it is important to ensure that variables to not take on unexpected types especially in the midst of complex data flows across the app. The best time to reinforce type-correctness is now, when the app is still small and refactoring costs are small.
- SCSS: Mixins, nesting, partials and inheritances help to keep CSS code logical and easier to maintain.
- Bootstrap: Someone else has already figured out responsive page sizing and I do not have a sufficiently convincing use-case to reinvent this wheel.
- Font Awesome: For similar reasons, why should I go through the trouble of finding and serving logo assets when someone else has already figured this out and provided convenient APIs that do most of what I need?
