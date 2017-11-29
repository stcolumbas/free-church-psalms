# derived from https://github.com/danthedeckie/OpenLP-To-ProPresenter5-Converter
import os
import re
from base64 import b64encode
from datetime import datetime
from uuid import uuid1

from utils import (load_scottish_psalter, load_sing_psalms, make_output_folder,
                   remove_folder, remove_markup, zip_folder)

__re_uni_x = re.compile(r'\\x..')      # Unicode \x form
__re_uni_u = re.compile(r'\\u....')    # Unicode \u form


DEFAULT_FONT = "Franklin Gothic Book"


def make_uuid():
    return uuid1().__str__().upper()


def SuperScRTF(text):
    # superscript verse #s at start of stanza:
    for ii in re.findall(r'uc0 \d+-*\d*', text):
        num = ii.lstrip('uc0 ')
        text = text.replace(ii, 'uc0 \\super {' + num + '}\\nosupersub ')
    # superscript verse #s in middle of stanza:
    for ii in re.findall(r'\n\d+-*\d*', text):
        num = re.findall(r'\d+-*\d*', ii)
        text = text.replace(ii, '\n\\super {' + num[0] + '}\\nosupersub ')
    return text


def underline_slide(text):
    text = text.replace('<underline>', r'{\lang2057\ul\ltrch ')
    text = text.replace('</underline>', r'}')
    return text


def convert_unicode_chars(text):
    def conv_char(c):
        o = ord(c)
        if o < 128:
            return c
        else:
            return rf'\u{o} '

    chars = [conv_char(char) for char in text]
    return ''.join(chars)


def MakeRTFBlob(text, font_colour, font_size):
    slide = '{\\rtf1\\ansi\\ansicpg1252\\cocoartf1038\\cocoasubrtf360{\\fonttbl\\f0\\fswiss\\fcharset0 ' + DEFAULT_FONT + ';}' \
        + '{\\colortbl;\\red' + font_colour[0] + '\\green' + font_colour[1] + '\\blue' + font_colour[2] + ';}' \
        + '\\pard\\tx560\\tx1120\\tx1680\\tx2240\\tx2800\\tx3360\\tx3920\\tx4480\\tx5040\\tx5600\\tx6160\\tx6720\\qc\\pardirnatural' \
        + '\\f0\\fs' + str(font_size * 2) + '\\fsmilli51200 \\cf1 \\expnd0\\expndtw0\\kerning0 \\uc0 ' + \
        convert_unicode_chars(text.lstrip("\n")) + '}'
    slide = SuperScRTF(slide)
    slide = underline_slide(slide)
    slide = slide.replace('\n', '\\\n')
    return b64encode(slide.encode()).decode()


def SlideBlock(text, screen_size, font_colour, background_colour):
    if screen_size[0] == '1080':
        font_size = 90
    else:
        font_size = 72

    return '<RVDisplaySlide backgroundColor="' + \
        " ".join(background_colour) + \
        '" enabled="1" highlightColor="0 0 0 0" hotKey="" label="" notes="" slideType="1" sort_index="0" UUID="' + \
        make_uuid() + \
        '" drawingBackgroundColor="1" chordChartPath="" serialization-array-index="0"><cues containerClass="NSMutableArray"></cues><displayElements containerClass="NSMutableArray"><RVTextElement displayDelay="0" displayName="Default" locked="0" persistent="0" typeID="0" fromTemplate="0" bezelRadius="0" drawingFill="0" drawingShadow="0" drawingStroke="0" fillColor="1 1 1 1" rotation="0" source="" adjustsHeightToFit="1" verticalAlignment="0" RTFData="' + \
        MakeRTFBlob(text, font_colour, font_size) + \
        '" revealType="0" serialization-array-index="0"><_-RVRect3D-_position x="0" y="0" z="0" width="' + \
        screen_size[1] + \
        '" height="' + \
        screen_size[0] + \
        '"></_-RVRect3D-_position><_-D-_serializedShadow containerClass="NSMutableDictionary"><NSNumber serialization-native-value="4" serialization-dictionary-key="shadowBlurRadius"></NSNumber><NSColor serialization-native-value="0 0 0 1" serialization-dictionary-key="shadowColor"></NSColor><NSMutableString serialization-native-value="{2.82842969894409, -2.82843065261841}" serialization-dictionary-key="shadowOffset"></NSMutableString></_-D-_serializedShadow><stroke containerClass="NSMutableDictionary"><NSColor serialization-native-value="1 1 1 1" serialization-dictionary-key="RVShapeElementStrokeColorKey"></NSColor><NSNumber serialization-native-value="0" serialization-dictionary-key="RVShapeElementStrokeWidthKey"></NSNumber></stroke></RVTextElement></displayElements><_-RVProTransitionObject-_transitionObject transitionType="-1" transitionDuration="1" motionEnabled="0" motionDuration="20" motionSpeed="100"></_-RVProTransitionObject-_transitionObject></RVDisplaySlide>'


def HeaderBlock(Name='New Song',
                Authors='',
                Artist='',
                CCLICopyRightInfo='',
                CCLILicenceNumber='',
                Publisher='',
                Notes='',
                height="1080",
                width="1920",
                category=""):

    return '<RVPresentationDocument height="' + \
        height + \
        '" width="' + \
        width + \
        '" versionNumber="500" docType="0" creatorCode="1349676880" lastDateUsed="' + \
        datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + \
        '" usedCount="0" category="' + \
        category + \
        '" resourcesDirectory="" backgroundColor="0 0 0 1" drawingBackgroundColor="0" notes="' + \
        Notes + \
        '" artist="' + \
        Artist + \
        '" author="' + \
        Authors + \
        '" album="" CCLIDisplay="1" CCLIArtistCredits="" CCLISongTitle="' + \
        Name + \
        '" CCLIPublisher="' + \
        Publisher + \
        '" CCLICopyrightInfo="' + \
        CCLICopyRightInfo + \
        '" CCLILicenseNumber="' + \
        CCLILicenceNumber + \
        '" chordChartPath=""><timeline timeOffSet="0" selectedMediaTrackIndex="0" unitOfMeasure="60" duration="0" loop="0"><timeCues containerClass="NSMutableArray"></timeCues><mediaTracks containerClass="NSMutableArray"></mediaTracks></timeline><bibleReference containerClass="NSMutableDictionary"></bibleReference><_-RVProTransitionObject-_transitionObject transitionType="-1" transitionDuration="1" motionEnabled="0" motionDuration="20" motionSpeed="100"></_-RVProTransitionObject-_transitionObject><groups containerClass="NSMutableArray">'


FooterBlock = '</groups><arrangements containerClass="NSMutableArray"></arrangements></RVPresentationDocument>'


def write_prop(psalm, screen_size, font_colour, background_colour, underline, extra_slide, output_folder):
    to_write = ""
    if extra_slide:
        psalm['stanzas'] = [""] + psalm['stanzas']
    for v in psalm['stanzas']:
        if not underline:
            v = remove_markup(v)

        to_write += SlideBlock(
            v,
            screen_size,
            font_colour,
            background_colour
        )

    if psalm['book'] == "Sing Psalms":
        copyright_field = "Free Church of Scotland"
    else:
        copyright_field = ""
    # Prepare Header Block to write:
    to_write_header = HeaderBlock(
        Name=psalm['name'],
        Artist='',
        CCLILicenceNumber='',
        Notes=psalm['metre'],
        CCLICopyRightInfo=copyright_field,
        Publisher='',
        Authors=psalm['book'],
        height=screen_size[0],
        width=screen_size[1],
        category=psalm['book'])
    to_write = to_write_header + \
        '<RVSlideGrouping name="' + \
        ' ' + \
        '" uuid="' + \
        make_uuid() + \
        '" color="' + \
        ' ' + \
        '" serialization-array-index="0"><slides containerClass="NSMutableArray">' + \
        to_write + \
        '</slides></RVSlideGrouping>' + \
        FooterBlock
    # Now actually write the thing.
    with open(os.path.join(output_folder, psalm['file_name'] + '.pro5'), 'w') as f:
        f.write(to_write)


def convert2propresenter(screen_size=("1080", "1920"), font_colour=('0', '0', '0'), background_colour=('1', '1', '1', '1'), colour_name='b_w', underline=False, extra_slide=False):
    """Convert Psalms to propresenter files."""
    ratio = "x".join(screen_size)
    folder_ids = [ratio, colour_name]
    if underline:
        folder_ids.append("underlined")
    if extra_slide:
        folder_ids.append("stcs")
    # sing psalms
    file_name = "Sing Psalms"
    output_folder = make_output_folder(["ProPresenter5", '_'.join(folder_ids), file_name])
    psalms = load_sing_psalms()
    for psalm in psalms:
        write_prop(psalm, screen_size, font_colour, background_colour, underline, extra_slide, output_folder)

    # scottish psalter
    file_name = "Scottish Psalter"
    output_folder = make_output_folder(["ProPresenter5", '_'.join(folder_ids), file_name])
    psalms = load_scottish_psalter()
    for psalm in psalms:
        write_prop(psalm, screen_size, font_colour, background_colour, underline, extra_slide, output_folder)

    zip_folder(os.path.dirname(output_folder))
    remove_folder(os.path.dirname(output_folder))

if __name__ == '__main__':
    convert2propresenter()
