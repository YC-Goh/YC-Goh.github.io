
#%%

import os
import re
import nbformat
from nbconvert import MarkdownExporter

#%%

if __name__ == '__main__':
    curdir = os.path.dirname(__file__)
    nb = nbformat.reads(open(os.path.join(curdir, 'sg-public-data', 'src', '_1_marriage_patterns.ipynb'), 'rt').read(), as_version=4)
    mdexporter = MarkdownExporter()
    data, resources = mdexporter.from_notebook_node(nb)
    data = re.compile(r'(\[[^\[\]]*\]\()([^\(\)]+)(\))').sub(r'\1/blog/marriage-patterns/\2\3', data)
    appdir = os.path.join(curdir, os.pardir, 'app')
    appdir = os.path.abspath(appdir)
    blogdir = os.path.abspath(os.path.join(appdir, 'blog'))
    blogpubdir = os.path.abspath(os.path.join(appdir, 'public', 'blog'))
    try:
        os.makedirs(os.path.join(blogdir, 'marriage-patterns'))
    except:
        pass
    with open(os.path.join(blogdir, 'marriage-patterns', 'page.md'), 'wt') as file:
        file.write(data)
    try:
        os.makedirs(os.path.join(blogpubdir, 'marriage-patterns'))
    except:
        pass
    for filename, content in resources['outputs'].items():
        with open(os.path.join(blogpubdir, 'marriage-patterns', filename), 'wb') as file:
            file.write(content)

#%%
