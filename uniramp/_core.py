import argparse
import pathlib

from .img2text import img2text
from .ramp import Ramp


__all__ = [
    'main'
]

def init_args():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='cmd')

    parser_ramp = subparser.add_parser('ramp', help='Print ramp infomation')
    parser_ramp.add_argument('-f', '--font', type=pathlib.Path, required=True,
                            help='specify the font file')
    parser_ramp.add_argument('-c', '--character-set', type=str,
                        help='specify the character set (default is [a-z][A-Z])')
    parser_ramp.add_argument('-g', '--graph', action="store_true", help='Print ramp graph')
    # parser_ramp.set_defaults(func=self.ramp)

    parser_image = subparser.add_parser('image', help='Convert an image to chars')
    parser_image.add_argument('-i', '--image', type=pathlib.Path, required=True,
                            help='specify the image')
    parser_image.add_argument('-f', '--font', type=pathlib.Path, required=True,
                            help='specify the font file')
    parser_image.add_argument('-c', '--character-set', type=str,
                        help='specify the character set (default is [a-z][A-Z])')
    # parser_image.set_defaults(func=self.image)

    args = parser.parse_args()
    return args

def main():
    args = init_args()
    r = Ramp(args)
    if args.cmd == 'ramp':
        r.show_ramp()
    elif args.cmd == 'image':
        ramp = r.get_ramp()
        img2text(str(args.image), ramp[::-1])
    else:
        pass
