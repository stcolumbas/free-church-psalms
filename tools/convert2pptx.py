# coding: utf-8
import os
import json
import re
import zipfile
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def superscript_pptx():
    with zipfile.ZipFile('tmp.pptx', 'a') as f:
        slides = set([x for x in f.namelist() if x.startswith('ppt/slides/slide')])
        slides.remove('ppt/slides/slide1.xml')
        slides = list(slides)
        for slide in slides:
            text = f.open(slide).read()
            text = re.sub('<a:r><a:t>(\d+)',
                          '<a:r><a:rPr baseline="30000" dirty="0"/><a:t>\g<1></a:t></a:r><a:r><a:rPr dirty="0"/><a:t>',
                          text)
            text = re.sub('\n(\d+)',
                          '\n</a:t></a:r><a:r><a:rPr baseline="30000" dirty="0"/><a:t>\g<1></a:t></a:r><a:r><a:rPr dirty="0"/><a:t>',
                          text)
            f.writestr(slide, text)


def write_pptx(psalm, ratio, colour, output_folder):
    # set up pptx:
    prs = Presentation(os.path.join("..",
                       "masters",
                       ratio + "_" + colour + ".pptx"))
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    # title slide:
    title.text = psalm['name']
    if psalm['name'] == 'Sing Psalms':
        subtitle.text = psalm['metre'] + u'\n\u00A9 Free Church of Scotland'
    else:
        subtitle.text = psalm['metre']
    # stanzas
    blank_slide_layout = prs.slide_layouts[6]
    for v in psalm['stanzas']:
        slide = prs.slides.add_slide(blank_slide_layout)
        left = top = Inches(0)
        width = Inches(20)
        if ratio == "4x3":
            height = Inches(15)
        else:
            height = Inches(28.58 / 2.54)
        txBox = slide.shapes.add_textbox(left, top, width, height)
        tf = txBox.textframe
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        if ratio == "16x9":
            tf.auto_size = MSO_AUTO_SIZE.NONE
        tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
        tf.text = v
        p = tf.paragraphs[0]
        p.font.size = Pt(60)
        p.alignment = PP_ALIGN.CENTER
    # save tmp pptx
    prs.save('tmp.pptx')
    # superscript verse numbers
    superscript_pptx()
    # reload and save again to fix powerpoint complaining
    prs_ = Presentation('tmp.pptx')
    prs_.save(os.path.join(output_folder, psalm['short_name'] + '.pptx'))
    os.remove('tmp.pptx')


def convert2pptx(ratio="16x9", colour="b_w"):
    """Convert Psalms to pptx files
    """
    # sing psalms
    output_folder = os.path.join("..", "output", "pptx", ratio, colour, "SingPsalms")
    try:
        os.makedirs(output_folder)
    except Exception, e:
        print e
    with open(os.path.join("..", "masters", "sing_psalms.json"), 'r') as f:
        psalms = json.loads(f.read())
    for psalm in psalms:
        write_pptx(psalm, ratio, colour, output_folder)
    # trad psalms
    output_folder = os.path.join("..", "output", "pptx", ratio, colour, "Traditional1650")
    try:
        os.makedirs(output_folder)
    except Exception, e:
        print e
    with open(os.path.join("..", "masters", "traditional_1650.json"), 'r') as f:
        psalms = json.loads(f.read())
    for psalm in psalms:
        write_pptx(psalm, ratio, colour, output_folder)
