import argparse
import pathlib
from ._uniramp import Typeface
from .img2text import img2text



__all__ = [
    'main'
]


def get_ramp(font, character_set):
    tf = Typeface(str(font))
    if character_set is None or len(character_set) == 0:  
        character_set = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ramp = sorted([(c, tf.get_coverage(ord(c))) for c in character_set], key=lambda x: x[1], reverse=True)

    return ramp


def image_to_text(image, ramp):
    img2text(image, ramp)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--font', type=pathlib.Path, required=True,
                        help='specify the font file')
    parser.add_argument('-i', '--image', type=pathlib.Path,
                        help='specify the image')
    parser.add_argument('-c', '--character-set', type=str,
                        help='specify the character set (default is [a-z][A-Z])')

    args = parser.parse_args()

    ramp = get_ramp(str(args.font), args.character_set)
    print('Ramp: ' + ''.join([c[0] for c in ramp]))

    if args.image:
        image_to_text(str(args.image), ramp[::-1])
