# coding: utf-8

# convert to a single pdf - using latex

import os
import json
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


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
    """Convert both sets of Psalms to text files and
    save in output/plain_text
    """
    # sing psalms
    output_folder = os.path.join("..", "output", "pdf")
    try:
        os.makedirs(output_folder)
    except Exception, e:
        print e
    with open(os.path.join("..", "masters", "sing_psalms.json"), 'r') as f:
        psalms = json.loads(f.read())
    create_latex_body(psalms, "Sing Psalms", os.path.join(output_folder, 'Sing Psalms.tex'))

    # trad psalms
    output_folder = os.path.join("..", "output", "pdf")
    try:
        os.makedirs(output_folder)
    except Exception, e:
        print e
    with open(os.path.join("..", "masters", "traditional_1650.json"), 'r') as f:
        psalms = json.loads(f.read())
    create_latex_body(psalms, "Traditional Scottish Psalter", os.path.join(output_folder, 'Traditional 1650.tex'))

if __name__ == '__main__':
    convert2latex()
