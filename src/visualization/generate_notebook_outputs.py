import os
import nbformat
from traitlets.config import Config
from nbconvert import MarkdownExporter
from nbconvert.writers import FilesWriter

notebookDir = r'C:\Users\thoma\projects\datascience\capstone-03\notebooks'
outputDir = r'C:\Users\thoma\projects\datascience\jupyter-presentation-framework\src\notebooks'

for entry in os.scandir(notebookDir):
    if not entry.name.startswith('.'):
        for notebook in os.scandir(entry.path):
            if (not notebook.name.startswith('.')) and notebook.path.endswith('.ipynb'):
                nb_node = nbformat.read(notebook.path, nbformat.NO_CONVERT)
                me = MarkdownExporter()
                (output, resource) = me.from_notebook_node(nb_node)
                c = Config()
                c.FilesWriter.build_directory = outputDir
                fw = FilesWriter(config=c)
                section = entry.name.replace(r'^\d', '').replace('-', '').replace('_', ' ')
                section = 'section : "' + section + '"\n'
                title = notebook.name.replace('/.ipynb', '')
                title = 'title: "' + title + '"\n'
                header = '---\n' + section + title + '---\n'
                fw.write(header + output, resource, notebook_name=notebook.name)
