import json
import os
import shutil
import subprocess


def load_sing_psalms():
    with open(os.path.join("..", "masters", "sing_psalms.json"), 'r') as f:
        return json.loads(f.read())


def load_scottish_psalter():
    with open(os.path.join("..", "masters", "traditional_1650.json"), 'r') as f:
        return json.loads(f.read())


def make_output_folder(folder_path):
    base_dir = os.path.dirname(__file__)
    output_folder = os.path.join(base_dir, '..', 'output', *folder_path)
    os.makedirs(output_folder, exist_ok=True)
    return output_folder


def zip_folder(folder_path):
    if folder_path:
        shutil.make_archive(folder_path, 'zip', folder_path)


def remove_folder(folder_path):
    if folder_path:
        shutil.rmtree(folder_path)


def convert2pdf(folder_name):
    """If libre office is installed, use it to convert to pdf."""
    if not check_lo_installed():
        return ""
    # create folder
    output_folder = folder_name.replace('PowerPoint', 'PDF')
    os.makedirs(output_folder, exist_ok=True)
    # escape spaces
    if not folder_name.endswith('/'):
        folder_name = folder_name + '/'
    in_safe = folder_name.replace(' ', '\ ')
    out_safe = output_folder.replace(' ', '\ ')
    # call libre office
    cmd = f'soffice --headless --convert-to pdf --outdir {out_safe} {in_safe}*.pptx'
    subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)

    return output_folder


def check_lo_installed():
    output = subprocess.run(
        'soffice --version',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        output.check_returncode()
        return True
    except subprocess.CalledProcessError:
        return False

    return False


def remove_markup(text):
    return text.replace('<underline>', '').replace('</underline>', '')
