import sys
import os
import argparse
import shutil
from os.path import join as pjoin
from xml.etree import ElementTree
from collections import namedtuple
from pprint import pprint
from distutils.dir_util import mkpath


class AdobeCCFontExtractor:
    pass


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

# global configuration object


class Config:
    path_prefix = ''
    filename_prefix = ''
    filename_suffix = ''
    font_dir = ''
    manifest = ''
    install_path = ''
    target_path = ''


# font data object
FontData = namedtuple('FontData', 'id name weight')


def get_font_metadata(manifest_path):
    tree = ElementTree.parse(manifest_path)

    # find the <fonts> element containing the list of fonts
    fonts_subtree = tree.getroot().find('fonts')

    fonts = []

    for font_elem in fonts_subtree.findall('font'):
        props = font_elem.find('properties')
        f_id = font_elem.find('id').text
        f_name = props.find('familyName').text
        f_weight = props.find('variationName').text

        font = FontData(id=f_id, name=f_name, weight=f_weight)

        fonts.append(font)

    return fonts

# install the fonts on the system per the --install flag


def install_fonts(fonts):
    pass

# extract the fonts to location
# folder structure:
# location/
#     Font1/
#         Font1 - Variation1.otf
#         Font1 - Variation2.otf


def extract_fonts(fonts, config):
    font_dir = config.font_dir
    location = config.target_path
    filename_prefix = config.filename_prefix
    filename_suffix = config.filename_suffix

    # make dirs to location if they don't exist
    mkpath(location)

    for font in fonts:
        src = pjoin(font_dir, filename_prefix + str(font.id))
        # src = pjoin(font_dir, '.' + str(font.id) + '.otf')
        filename = font.name + ' - ' + font.weight + '.otf'
        dest = pjoin(location, filename)
        shutil.copy(src, dest)


def sync_all_fonts():
    ''' Go to the Adobe CC website and sync EVERY font '''
    pass


def platform_setup():
    '''Set up paths for MacOS or Windows'''
    c = Config()

    if sys.platform == 'win32':  # Windows
        c.path_prefix = os.path.expandvars(r'%APPDATA%\Adobe\CoreSync\plugins\livetype')
        c.font_dir = pjoin(c.path_prefix, 'r')
        c.manifest = pjoin(c.path_prefix, r'c\entitlements.xml')
        c.target_path = os.path.expandvars(r'%USERPROFILE%\Downloads\extracted-fonts')
    else:  # MacOS
        c.path_prefix = os.path.expandvars(r'$HOME/Library/Application Support/Adobe/CoreSync/plugins/livetype')
        c.filename_prefix = '.'
        c.filename_suffix = '.otf'
        c.font_dir = os.path.join(c.path_prefix, '.r')
        c.manifest = os.path.join(c.path_prefix, '.c/entitlements.xml')
        c.target_path = os.path.expandvars(r'$HOME/Downloads/extracted-fonts')

    return c


def main():
    config = platform_setup()

    # parse the command line arguments

    parser = argparse.ArgumentParser(description='Extract Adobe CC Typekit fonts. '
                                     'Adobe CC Font Sync syncs your fonts from Typekit, however '
                                     'These fonts are not available')
    # parser.add_argument('--install', type=
    parser.add_argument('-l', '--list', help='show which fonts are synced')
    parser.parse_args()

    try:
        font_data = get_font_metadata(config.manifest)
        pprint(font_data)
        extract_fonts(font_data, config)
    except IOError as e:
        print("Error: The font manifest could not be found. Make sure Adobe Creative Cloud is running.", e)


def test():
    config = platform_setup()
    config.target_path = 'TEST'
    fonts = get_font_metadata(config.manifest)
    extract_fonts(fonts, config)


if __name__ == '__main__':
    main()
