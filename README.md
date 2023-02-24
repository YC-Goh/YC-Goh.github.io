
# YC-Goh Personal Website

## What?

This is the repository containing the source code and static webpage files for my personal website.

## Stack

This website uses the following web technologies:
- HTML, CSS, JavaScript: The foundations of a modern webpage.
- Github Pages + Actions: This provides a convenient web hosting solution that a small static website like this needs.
- Next.js: This replaces webpack.js and its loaders for transpiling and bundling project assets with a focus on generating front-end apps using the React.js framework and Node.js for running and managing development and production servers.
- React.js + JSX: This is the framework that Next.js assumes. I use functional components as recommended by React maintainers.
- Unified.js: Convenience library to reduce writing HTML pages to writing a markdown report.
- TypeScript: Type correctness helps ensure functions do not behave in some unexpected ways.
- KaTeX: If data science notebooks are to be shown, there needs to be some way to display math.
- SCSS: Mixins, nesting, partials and inheritances help to keep CSS code logical and easier to maintain.
- Bootstrap: Convenience library for making the page layout responsive and filling in some colour schemes.
- Font Awesome: Convenience library to insert logos.

Behind the scenes, the following tools are also used:
- Jupyter: Pretty much the leading format in terms of convenience, ease of use and expressiveness for showcasing a data science project workflow and results.
- NBConvert: I am not using the NBViewer service. Instead this is how I turn my notebooks into web content or a format that I can transpile into web content.
- Python 3: My current data science language of choice when Stata is not freely available.
  - NumPy, Pandas, SciPy, MatPlotLib.

I might also use these in the future depending on what I do for personal projects:
- R, Julia: Other data/computation-focused languages that I know.
- Scikit-Learn, TensorFlow, Keras: ML/AI stack.
- GeoPandas, QVis: For dealing with geographic data.
- Proper web hosting solutions like Vercel or Heroku.
- Proper database management systems like PostgreSQL or MongoDB.
- Proper cloud service providers like AWS, Azure, or IBM Cloud.
