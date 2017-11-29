set -e

# generate plain text, .tex, pptx and ProPresenter files:
. venv/bin/activate
cd tools/

python extract_psalms.py
python convert_psalms.py

cd ../
