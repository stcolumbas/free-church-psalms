#!/usr/bin/env python
import os

from convert2latex import convert2latex
from convert2pptx import convert2pptx
from convert2propresenter import convert2propresenter
from convert2txt import convert2txt
from utils import zip_folder

def main():
    # plain text files
    print('Generating Plain Text')
    convert2txt()

    # pptx, in two colours and two aspect ratios
    # - colours are inherited from templates in masters folder
    print('Generating .pptx files')
    for ratio in ['4x3', '16x9']:
        for colour in ['b_w', 'w_b']:
            for underline in [True, False]:
                convert2pptx(
                    ratio=ratio,
                    colour=colour,
                    underline=underline,
                )

    # ProP in two colours and two screen sizes
    print('Generating ProPresenter files')
    colours = [{'font': ('0', '0', '0'),
                'bg': ('1', '1', '1', '1'),  # rgba
                'name': 'b_w'},
            {'font': ('255', '255', '255'),
                'bg': ('0', '0', '0', '1'),
                'name': 'w_b'}]
    for screen_size in [('1080', '1920'), ('720', '1280'), ('768', '1024')]:
        for colour in colours:
            for underline in [True, False]:
                for extra_slide in [True, False]:
                    convert2propresenter(
                        screen_size=screen_size,
                        font_colour=colour['font'],
                        background_colour=colour['bg'],
                        colour_name=colour['name'],
                        underline=underline,
                        extra_slide=extra_slide,
                    )


if __name__ == '__main__':
    main()
