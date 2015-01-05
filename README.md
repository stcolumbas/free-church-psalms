Free Church Psalms
======

*Please note that this is currently a work in progress - some formatting bugs are still being worked out.*

The purpose of this project is to make Sing Psalms (copyright Free Church of Scotland) and the Scottish Psalter (1650 revised words) easily downloadable for churches.

## Quickstart

If you just want to download the files please go to *coming soon*.

## Formats

The words are produced in a variety of formats to suit the different technologies congregations may be using:

 * Microsoft PowerPoint (pptx)
 * ProPresenter
 * Plain Text
 * PDF

If your church is using a different piece of software, please get [in touch](mailto:technical.team@stcolumbas.freechurch.org) and we can hopefully add it to the rest.

## Advanced

If you want to contribute, or you want to generate slides in a different resolution/colour you can follow the following instructions:

Clone this repo:

    git clone git@github.com:stcolumbas/free-church-psalms.git
    cd free-church-psalms

Install the dependencies:

    virtualenv venv --no-site-packages
    source venv/bin/activate
    pip install -r requirements.txt

Generate the default output:

    cd tools
    python extract_psalms.py
    python convert_psalms.py

The Psalms are extracted from the Word files in the master folder and saved as json before being converted to different display formats.
See `convert2txt.py` for an example.

## License

All code in this project is licensed under the terms of the MIT license.

However the "Sing Psalms" words are copyright of the Free Church of Scotland and are reproduced here with permission.
