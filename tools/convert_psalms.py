# coding: utf-8
from convert2latex import convert2latex
from convert2pptx import convert2pptx
from convert2propresenter import convert2propresenter
from convert2txt import convert2txt

if __name__ == '__main__':
    print "Generating plain text files...\n"
    # plain text files
    convert2txt()

    # generate latex files for later compilation
    print "Generating .tex files...\n"
    convert2latex()

    # pptx, in two colours and two aspect ratios
    # - colours are inherited from templates in masters folder
    print "Generating .pptx files...\n"
    for ratio in ["4x3", "16x9"]:
        for colour in ["b_w", "w_b"]:
            convert2pptx(ratio=ratio,
                         colour=colour)

    # ProP in two colours and two screen sizes
    print "Generating ProPresenter files...\n"
    colours = [{'font': ('0', '0', '0'),
                'bg': ('1', '1', '1', '1'),  # rgba
                'name': "b_w"},
               {'font': ('255', '255', '255'),
                'bg': ('0', '0', '0', '1'),
                'name': "w_b"}]
    for screen_size in [("1080", "1920"), ("768", "1024")]:
        for colour in colours:
            convert2propresenter(screen_size=screen_size,
                                 font_colour=colour['font'],
                                 background_colour=colour['bg'],
                                 colour_name=colour['name'])
