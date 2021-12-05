import argparse
import pathlib
from ._uniramp import Typeface


__all__ = [
    'main'
]


def print_ramp(font, character_set):
    tf = Typeface(str(font))
    if character_set is None or len(character_set) == 0:  
        character_set = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ramp = sorted([(c, tf.load_glyph(ord(c))) for c in character_set], key=lambda x: x[1], reverse=True)

    print('Ramp: ' + ''.join([c[0] for c in ramp]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--font', type=pathlib.Path, required=True,
                        help='specify the font file')
    parser.add_argument('-c', '--character-set', type=str,
                        help='specify the character set (default is [a-z][A-Z])')

    args = parser.parse_args()
    print_ramp(str(args.font), args.character_set)
