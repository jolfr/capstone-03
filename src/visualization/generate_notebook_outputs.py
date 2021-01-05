import os
import nbformat
from traitlets.config import Config
from nbconvert import MarkdownExporter
from nbconvert.writers import FilesWriter

notebookDir = r'C:\Users\thoma\projects\datascience\capstone-03\notebooks'
outputDir = r'C:\Users\thoma\projects\datascience\jupyter-presentation-framework\src\notebooks'


def getsectionParams(sec):
    sec = sec.replace('-', ' ').replace('_', ' ')
    sec = sec.split(' ')
    num = sec.pop(0)
    newsec = ''
    for word in sec:
        newsec = newsec + ' ' + word
    sec = newsec.lstrip()
    return num, sec


def getnotebookparams(nb):
    nb = nb.replace('-', ' ').replace('_', ' ').replace('.ipynb', '')
    nb = nb.split(' ')
    num = nb.pop(0).split('.')[1]
    newnb = ''
    for word in nb:
        newnb = newnb + ' ' + word
    nb = newnb.lstrip()
    return num, nb


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
                (secNum, section) = getsectionParams(entry.name)
                secNum = 'secid : ' + secNum + '\n'
                section = 'section : "' + section + '"\n'
                (nbNum, title) = getnotebookparams(notebook.name)
                nbNum = 'nbid : ' + nbNum + '\n'
                title = 'title: "' + title + '"\n'
                header = '---\n' + secNum + nbNum + section + title + '---\n'
                fw.write(header + output, resource, notebook_name=notebook.name)
            elif notebook.name == 'README.md':
                with open(notebook.path, 'r', encoding='utf-8') as input_file:
                    text = input_file.read()
                    (secNum, section) = getsectionParams(entry.name)
                    section = 'section : "' + section + '"\n'
                    secNum = 'secid : ' + secNum + '\n'
                    title = 'title: readme\n'
                    header = '---\n' + secNum + section + title + '---\n'
                    newText = header + text
                with open(outputDir + "\\" + entry.name + '.md', 'w', encoding='utf-8') as output_file:
                    output_file.write(newText)
