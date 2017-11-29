#!/usr/bin/env python
import json
import os
import re
import sys

import docx

from halo import Halo

re_trad_metres = re.compile(r"(PSALM) ([0-9]+)(.*)(C\.M\.|L\.M\.|S\.M\.|10 10 10 10 10|8 7 8 7 iambic|6 6 6 6 8 8|6 6 6 6 D)")
re_sp_metres = re.compile(r"10 10 10 10 10 10|10 10 10 10 10|10 10 10 10|10 7 7 10|10 9 10 9 9 9|10 9 10 9 anapaestic|10 9 10 9 trochaic|11 10 11 10 dactylic|11 10 11 10|11 11 11 11|11 11 11|12 11 12 11 \+ 12 11|12 12 12 12 anapaestic|6 6 6 6 8 8|6 6 6 6 D|6 6 6 6|6 8 8 6|7 7 7 7|7 6 7 6 D|7 6 7 6|8 6 8 8 6|8 7 8 7 7 7|8 7 8 7 8 7|8 7 8 7 D|8 7 8 7 iambic|8 7 8 7|8 8 8 8 6 6 6 6 8|8 8 8 8 8 8|8 8 8 8 anapaestic|9 8 9 8 8 8|9 8 9 8|9 9 9 9 anapaestic|C\.M\.|D.L.M.|D\.C\.M\.|L\.M\.|S\.M\.")


class Psalm(object):
    """Psalm"""

    def __init__(self, name, book, metre, stanzas, copyright):
        super(Psalm, self).__init__()
        self.name = name
        self.book = book
        self.metre = metre
        self.stanzas = stanzas
        self.copyright = copyright
        self.generate_filename()

    def __repr__(self):
        return self.name

    def generate_filename(self):
        ps_num = re.findall(r"\d+", self.name)[0]
        name = self.name.replace('Psalm', self.book)
        name = name.replace(ps_num, ps_num.zfill(3))
        name = name.replace(' ', '-')
        self.file_name = f'{name} [{self.metre}]'


def _extract_run(run):
    if run.underline:
        return f'<underline>{run.text}</underline>'
    else:
        return run.text


def _extract_line(p):
    return ''.join([_extract_run(r) for r in p.runs])


def _extract_paragraphs(filename):
    document = docx.Document(filename)
    paratextlist = [_extract_line(p) for p in document.paragraphs]
    # replace quotation marks
    paratextlist = [para.replace('“', '"').replace('”', '"') for para in paratextlist]
    # stitch back into single text blob
    text = '\n'.join(paratextlist)
    text = text.replace("\t", "")

    return text


def extract_sing_psalms():
    # read in docx file
    filename = os.path.join('..', 'masters', 'SingPsalms.docx')
    text = _extract_paragraphs(filename)
    # normalise the line breaks between Psalms:
    text = text.replace('\n\n\n\n', '\n\n\n')
    text = text.replace('\n\nPSALM', '\n\n\nPSALM')
    text = text.replace('\nPSALM', '\n\nPSALM')
    # split into separate Psalms:
    processed_psalms = list()
    psalms = text.split('\n\n\n')
    for psalm in psalms:
        psalm = psalm.strip("\n")
        # extract metre
        m_metre = re.search(re_sp_metres, psalm)
        metre_str = m_metre.group(0)
        psalm = psalm.replace(metre_str, "")
        m = re.match(r"\s*(PSALM) ([0-9]|[0-9][0-9]|1[0-5][0-9])(.*)", psalm)
        if len(m.group(3)) == 0:
            ps_name = 'Psalm ' + m.group(2)
        else:
            ps_name = 'Psalm ' + m.group(2) + m.group(3)

        stanzas = psalm[psalm.find('\n') + 2:]
        processed_psalms.append(
            Psalm(
                ps_name,
                "Sing Psalms",
                metre_str,
                stanzas.split('\n\n'),
                'Free Church of Scotland',
            )
        )

    psalms_json = [psalm.__dict__ for psalm in processed_psalms]
    with open(os.path.join("..", "masters", "sing_psalms.json"), 'w') as f:
        f.write(json.dumps(psalms_json))


def extract_trad_psalms():
    # read in docx file
    filename = os.path.join('..', 'masters', '1650revisedwords.docx')
    text = _extract_paragraphs(filename)
    # split into separate Psalms:
    processed_psalms = list()
    psalms = text.split('\n\n\n')
    for psalm in psalms:
        psalm = psalm.lstrip('\n')
        m = re.match(re_trad_metres, psalm)
        metre_str = m.group(4)
        if len(m.group(3)) == 0:
            ps_name = 'Psalm ' + m.group(2) + ' (T)'
        else:
            ps_name = 'Psalm ' + m.group(2) + m.group(3) + ' (T)'

        stanzas = psalm[psalm.find('\n') + 2:]
        processed_psalms.append(
            Psalm(
                ps_name,
                "Scottish Psalter",
                metre_str,
                stanzas.split('\n\n'),
                None,
            )
        )

    psalms_json = [psalm.__dict__ for psalm in processed_psalms]
    with open(os.path.join("..", "masters", "traditional_1650.json"), 'w') as f:
        f.write(json.dumps(psalms_json))


if __name__ == '__main__':
    with Halo(text='Extracting Psalms and saving as JSON', spinner='dots'):
        extract_sing_psalms()
        extract_trad_psalms()
