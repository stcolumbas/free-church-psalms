# convert to a single pdf - using latex
import json
import os
import re

from utils import (load_scottish_psalter, load_sing_psalms, make_output_folder,
                   remove_folder, zip_folder)


def create_latex_body(psalms, toc_name, output_name):
    body = u'''\\documentclass[11pt,a4paper]{report}
\\setlength{\parindent}{0pt}
\\usepackage{fixltx2e}
\\usepackage{hyperref}
\\usepackage[top=2cm, bottom=2cm, left=2.5cm, right=2.5cm]{geometry}
\\title{''' + toc_name + '''}
\\renewcommand*\contentsname{''' + toc_name + '''}
\\begin{document}
\\tableofcontents
\\pagebreak
\\pagestyle{empty}\n'''

    for psalm in psalms:
        body += "\\addcontentsline{toc}{section}{" + psalm['name'] + "}\n"
        body += "\\section*{" + psalm['name'] + "}\n\n"
        body += "\\textit{" + psalm['metre'] + "}\\\\\n\n"
        for v in psalm['stanzas']:
            # superscript verse #s
            for ii in re.findall(r'\d+', v):
                num = re.findall(r'\d+', ii)
                v = v.replace(ii, '\\textsuperscript{' + num[0] + '}')
            body += v.replace("\n", "\\\\") + "\\\\\n\n"

        body += "\\pagebreak"

    body += '\\end{document}'
    for quote in re.findall(r'''\".+\"''', body):
        body = body.replace(quote, "``" + quote.replace('"', '') + "''")
    with open(output_name, 'w') as f:
        f.write(body)


def convert2latex():
    """Convert both sets of Psalms to text files and save in output/plain_text"""
    output_folder = make_output_folder(["tex"])
    # sing psalms
    psalms = load_sing_psalms()
    create_latex_body(psalms, "Sing Psalms", os.path.join(output_folder, 'Sing Psalms.tex'))

    # trad psalms
    psalms = load_scottish_psalter()
    create_latex_body(psalms, "Scottish Psalter", os.path.join(output_folder, 'Scottish Psalter.tex'))

    zip_folder(output_folder)
    remove_folder(output_folder)

if __name__ == '__main__':
    convert2latex()
