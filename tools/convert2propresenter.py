# coding: utf-8
# derived from https://github.com/danthedeckie/OpenLP-To-ProPresenter5-Converter

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
import json
from base64 import b64encode, b64decode
from uuid import uuid1
from datetime import datetime

__re_uni_x = re.compile(r'\\x..')      # Unicode \x form
__re_uni_u = re.compile(r'\\u....')    # Unicode \u form


DEFAULT_FONT = "Franklin Gothic Book"


def make_uuid():
    return uuid1().__str__().upper()


def AntiUnicode(text):

    def escape_u(t):
        """ turns a '\u####' type hexadecimal unicode escape char into
            it's RTF '\uxxxx' decimal.
            For use in a re.sub function as the callback. """
        return r'\u' + unicode(int(t.group()[2:], 16)) + ' '

    return re.sub(__re_uni_x, escape_u,
                  re.sub(__re_uni_u, escape_u,
                         text.encode('unicode-escape'))).replace(r'\n', '\\\n')


def SuperScRTF(text):
    text = b64decode(text)
    # superscript verse #s at start of stanza:
    for ii in re.findall(r'uc0 \d+', text):
        num = ii.lstrip('uc0 ')
        text = text.replace(ii, 'uc0 \\super {' + num + '}\\nosupersub ')
    # superscript verse #s in middle of stanza:
    for ii in re.findall(r'\n\d+', text):
        num = re.findall(r'\d+', ii)
        text = text.replace(ii, '\n\\super {' + num[0] + '}\\nosupersub ')
    return b64encode(text)


def MakeRTFBlob(text, font_colour):
    return SuperScRTF(b64encode(
        '{\\rtf1\\ansi\\ansicpg1252\\cocoartf1038\\cocoasubrtf360\n{\\fonttbl\\f0\\fswiss\\fcharset0 ' + DEFAULT_FONT + ';}\n'
        + '{\\colortbl;\\red' + font_colour[0] + '\\green' + font_colour[1] + '\\blue' + font_colour[2] + ';}\n'
        + '\\pard\\tx560\\tx1120\\tx1680\\tx2240\\tx2800\\tx3360\\tx3920\\tx4480\\tx5040\\tx5600\\tx6160\\tx6720\\qc\\pardirnatural\n\n'
        + '\\f0\\fs144\\fsmilli51200 \\cf1 \\expnd0\\expndtw0\\kerning0\n \\uc0 ' + AntiUnicode(text) + '}'))


def SlideBlock(text, screen_size, font_colour, background_colour):

    return '<RVDisplaySlide backgroundColor="' + " ".join(background_colour) + '" enabled="1" highlightColor="0 0 0 0" hotKey="" label="" notes="" slideType="1" sort_index="0" UUID="' + make_uuid() + '" drawingBackgroundColor="1" chordChartPath="" serialization-array-index="0"><cues containerClass="NSMutableArray"></cues><displayElements containerClass="NSMutableArray"><RVTextElement displayDelay="0" displayName="Default" locked="0" persistent="0" typeID="0" fromTemplate="0" bezelRadius="0" drawingFill="0" drawingShadow="0" drawingStroke="0" fillColor="1 1 1 1" rotation="0" source="" adjustsHeightToFit="1" verticalAlignment="0" RTFData="' + MakeRTFBlob(text, font_colour) + '" revealType="0" serialization-array-index="0"><_-RVRect3D-_position x="0" y="0" z="0" width="' + screen_size[1] + '" height="' + screen_size[0] + '"></_-RVRect3D-_position><_-D-_serializedShadow containerClass="NSMutableDictionary"><NSNumber serialization-native-value="4" serialization-dictionary-key="shadowBlurRadius"></NSNumber><NSColor serialization-native-value="0 0 0 1" serialization-dictionary-key="shadowColor"></NSColor><NSMutableString serialization-native-value="{2.82842969894409, -2.82843065261841}" serialization-dictionary-key="shadowOffset"></NSMutableString></_-D-_serializedShadow><stroke containerClass="NSMutableDictionary"><NSColor serialization-native-value="1 1 1 1" serialization-dictionary-key="RVShapeElementStrokeColorKey"></NSColor><NSNumber serialization-native-value="0" serialization-dictionary-key="RVShapeElementStrokeWidthKey"></NSNumber></stroke></RVTextElement></displayElements><_-RVProTransitionObject-_transitionObject transitionType="-1" transitionDuration="1" motionEnabled="0" motionDuration="20" motionSpeed="100"></_-RVProTransitionObject-_transitionObject></RVDisplaySlide>'


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

    return '<RVPresentationDocument height="' + height + '" width="' + width + '" versionNumber="500" docType="0" creatorCode="1349676880" lastDateUsed="' + datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + '" usedCount="0" category="' + category + '" resourcesDirectory="" backgroundColor="0 0 0 1" drawingBackgroundColor="0" notes="' + Notes + '" artist="' + Artist + '" author="' + Authors + '" album="" CCLIDisplay="1" CCLIArtistCredits="" CCLISongTitle="' + Name + '" CCLIPublisher="' + Publisher + '" CCLICopyrightInfo="' + CCLICopyRightInfo + '" CCLILicenseNumber="' + CCLILicenceNumber + '" chordChartPath=""><timeline timeOffSet="0" selectedMediaTrackIndex="0" unitOfMeasure="60" duration="0" loop="0"><timeCues containerClass="NSMutableArray"></timeCues><mediaTracks containerClass="NSMutableArray"></mediaTracks></timeline><bibleReference containerClass="NSMutableDictionary"></bibleReference><_-RVProTransitionObject-_transitionObject transitionType="-1" transitionDuration="1" motionEnabled="0" motionDuration="20" motionSpeed="100"></_-RVProTransitionObject-_transitionObject><groups containerClass="NSMutableArray">'


FooterBlock = '</groups><arrangements containerClass="NSMutableArray"></arrangements></RVPresentationDocument>'


def write_prop(psalm, screen_size, font_colour, background_colour, output_folder):
    to_write = ""
    for v in psalm['stanzas']:
        to_write += SlideBlock(v,
                               screen_size,
                               font_colour,
                               background_colour)

    if psalm['book'] == "Sing Psalms":
        copyright_field = "Free Church of Scotland"
    else:
        copyright_field = ""
    # Prepare Header Block to write:
    to_write_header = (HeaderBlock(Name=psalm['name'],
                                   Artist='',
                                   CCLILicenceNumber='',
                                   Notes=psalm['metre'],
                                   CCLICopyRightInfo=copyright_field,
                                   Publisher='',
                                   Authors=psalm['book'],
                                   height=screen_size[0],
                                   width=screen_size[1],
                                   category=psalm['book']))
    to_write = to_write_header + '<RVSlideGrouping name="' + ' ' + '" uuid="' + make_uuid() + '" color="' + ' ' + '" serialization-array-index="0"><slides containerClass="NSMutableArray">' + to_write + '</slides></RVSlideGrouping>' + FooterBlock
    # Now actually write the thing.
    with open(os.path.join(output_folder, psalm['short_name'] + '.pro5'), 'w') as f:
        f.write(to_write)


def convert2propresenter(screen_size=("1920", "1080"), font_colour=('0', '0', '0'), background_colour=('1', '1', '1', '1'), colour_name='b_w'):
    """Convert Psalms to propresenter files
    """
    ratio = "x".join(screen_size)
    # sing psalms
    output_folder = os.path.join("..", "output", "ProPresenter", ratio, colour_name, "SingPsalms")
    try:
        os.makedirs(output_folder)
    except Exception, e:
        print e
    with open(os.path.join("..", "masters", "sing_psalms.json"), 'r') as f:
        psalms = json.loads(f.read())
    for psalm in psalms:
        write_prop(psalm, screen_size, font_colour, background_colour, output_folder)
    # trad psalms
    output_folder = os.path.join("..", "output", "ProPresenter", ratio, colour_name, "Traditional1650")
    try:
        os.makedirs(output_folder)
    except Exception, e:
        print e
    with open(os.path.join("..", "masters", "traditional_1650.json"), 'r') as f:
        psalms = json.loads(f.read())
    for psalm in psalms:
        write_prop(psalm, screen_size, font_colour, background_colour, output_folder)
