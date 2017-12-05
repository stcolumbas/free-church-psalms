import os

from utils import (load_scottish_psalter, load_sing_psalms, make_output_folder,
                   remove_folder, remove_markup, zip_folder)


def write_text_file(psalm, output_folder, fname):
    fname += ".txt"
    with open(os.path.join(output_folder, fname), 'w') as f:
        text = psalm['name'] + "\r\n"  # use windows compat. line breaks
        text += psalm['metre'] + "\r\n\r\n"
        text += "\r\n\r\n".join(psalm['stanzas'])

        if psalm['copyright'] is not None:
            text += "\r\n\r\n© " + psalm['copyright']

        remove_markup(text)

        f.write(text)


def convert2txt():
    """Convert both sets of Psalms to text files and
    save in output/plain_text
    """
    # sing psalms
    output_folder = make_output_folder(["PlainText", "Sing Psalms"])
    psalms = load_sing_psalms()
    for psalm in psalms:
        write_text_file(psalm, output_folder, psalm['file_name'])

    # trad psalms
    output_folder = make_output_folder(["PlainText", "Scottish Psalter"])
    psalms = load_scottish_psalter()
    for psalm in psalms:
        write_text_file(psalm, output_folder, psalm['file_name'])

    zip_folder(os.path.dirname(output_folder))
    remove_folder(os.path.dirname(output_folder))

if __name__ == '__main__':
    convert2txt()
