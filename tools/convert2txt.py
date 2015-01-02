# coding: utf-8
import os
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def write_text_file(psalm, output_folder, fname):
    fname += ".txt"
    with open(os.path.join(output_folder, fname), 'w') as f:
        text = psalm['name'] + "\r\n"  # use windows compat. line breaks
        text += psalm['metre'] + "\r\n\r\n"
        text += "\r\n\r\n".join(psalm['stanzas'])
        f.write(text)


def convert2txt():
    """Convert both sets of Psalms to text files and
    save in output/plain_text
    """
    # sing psalms
    output_folder = os.path.join("..", "output", "plain_text", "SingPsalms")
    try:
        os.makedirs(output_folder)
    except Exception, e:
        print e
    with open(os.path.join("..", "masters", "sing_psalms.json"), 'r') as f:
        psalms = json.loads(f.read())
    for psalm in psalms:
        write_text_file(psalm, output_folder, psalm['short_name'])

    # trad psalms
    output_folder = os.path.join("..", "output", "plain_text", "Traditional1650")
    try:
        os.makedirs(output_folder)
    except Exception, e:
        print e
    with open(os.path.join("..", "masters", "traditional_1650.json"), 'r') as f:
        psalms = json.loads(f.read())
    for psalm in psalms:
        write_text_file(psalm, output_folder, psalm['short_name'])

if __name__ == '__main__':
    convert2txt()
