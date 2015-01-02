# coding: utf-8

import docx
import json
import os
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Psalm(object):
    """Psalm"""

    def __init__(self, name, book, metre, stanzas):
        super(Psalm, self).__init__()
        self.name = name
        self.book = book
        self.metre = metre
        self.stanzas = stanzas
        shorter_name = name.lower().replace("psalm", "").replace("(t)", "").replace(",", "").lstrip().rstrip().replace(" ", "-")
        ps_num = re.findall(r"\d+", shorter_name)[0]
        shorter_name = shorter_name.replace(ps_num, ps_num.zfill(3))
        if book == "Sing Psalms":
            self.short_name = "s-" + shorter_name
        elif book == "Traditional":
            self.short_name = "t-" + shorter_name

    def __repr__(self):
        return self.name

    def json(self):
        return json.dumps({'name': self.name,
                           'book': self.book,
                           'metre': self.metre,
                           'stanzas': self.stanzas})


def extract_sing_psalms():
    # read in docx file
    filename = os.path.join('..', 'masters', 'SingPsalms.docx')
    document = docx.opendocx(filename)
    paratextlist = docx.getdocumenttext(document)
    # replace quotation marks
    paratextlist = [para.replace('“', '"').replace('”', '"') for para in paratextlist]
    # stitch back into single text blob
    text = '\n'.join(paratextlist)
    text = text.replace("\t", "")
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
        m_metre = re.search(r"10 10 10 10 10 10|10 10 10 10 10|10 10 10 10|10 7 7 10|10 9 10 9 9 9|10 9 10 9 anapaestic|10 9 10 9 trochaic|11 10 11 10 dactylic|11 10 11 10|11 11 11 11|11 11 11|12 11 12 11 \+ 12 11|12 12 12 12 anapaestic|6 6 6 6 8 8|6 6 6 6 D|6 6 6 6|6 8 8 6|7 7 7 7|7 6 7 6 D|7 6 7 6|8 6 8 8 6|8 7 8 7 7 7|8 7 8 7 8 7|8 7 8 7 D|8 7 8 7 iambic|8 7 8 7|8 8 8 8 6 6 6 6 8|8 8 8 8 8 8|8 8 8 8 anapaestic|9 8 9 8 8 8|9 8 9 8|9 9 9 9 anapaestic|C\.M\.|D.L.M.|D\.C\.M\.|L\.M\.|S\.M\.", psalm)
        metre_str = m_metre.group(0)
        psalm = psalm.replace(metre_str, "")
        m = re.match(r"\s*(PSALM) ([0-9]|[0-9][0-9]|1[0-5][0-9])(.*)", psalm)
        if len(m.group(3)) == 0:
            ps_name = 'Psalm ' + m.group(2)
        else:
            ps_name = 'Psalm ' + m.group(2) + m.group(3)

        stanzas = psalm[psalm.find('\n') + 2:]
        processed_psalms.append(Psalm(ps_name,
                                "Sing Psalms",
                                metre_str,
                                stanzas.split('\n\n')))

    psalms_json = [psalm.__dict__ for psalm in processed_psalms]
    with open(os.path.join("..", "masters", "sing_psalms.json"), 'w') as f:
        f.write(json.dumps(psalms_json))


def extract_trad_psalms():
    # read in docx file
    filename = os.path.join('..', 'masters', '1650revisedwords.docx')
    document = docx.opendocx(filename)
    paratextlist = docx.getdocumenttext(document)
    # replace quotation marks
    paratextlist = [para.replace('“', '"').replace('”', '"') for para in paratextlist]
    # stitch back into single text blob
    text = '\n'.join(paratextlist)
    text = text.replace("\t", "")
    # split into separate Psalms:
    processed_psalms = list()
    psalms = text.split('\n\n\n')
    for psalm in psalms:
        m = re.match(r"(PSALM) ([0-9]+)(.*)(C\.M\.|L\.M\.|S\.M\.|10 10 10 10 10|8 7 8 7 iambic|6 6 6 6 8 8|6 6 6 6 D)", psalm)
        metre_str = m.group(4)
        if len(m.group(3)) == 0:
            ps_name = 'Psalm ' + m.group(2) + ' (T)'
        else:
            ps_name = 'Psalm ' + m.group(2) + m.group(3) + ' (T)'

        stanzas = psalm[psalm.find('\n') + 2:]
        processed_psalms.append(Psalm(ps_name,
                                "Traditional",
                                metre_str,
                                stanzas.split('\n\n')))

    psalms_json = [psalm.__dict__ for psalm in processed_psalms]
    with open(os.path.join("..", "masters", "traditional_1650.json"), 'w') as f:
        f.write(json.dumps(psalms_json))


if __name__ == '__main__':
    print "Extracting Psalms and saving as JSON...\n"
    extract_sing_psalms()
    extract_trad_psalms()
