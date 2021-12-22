import argparse
import pathlib

from .img2text import img2text
from .ramp import show_ramp
from .coverage import Coverage


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
    parser_image.add_argument('-r', '--reverse', action="store_true", help='reverse the ramp order')
    # parser_image.set_defaults(func=self.image)

    args = parser.parse_args()
    return args

def main():
    args = init_args()
    cov = Coverage(args)
    c = cov.get_coverage()

    if args.cmd == 'ramp':
        show_ramp(c, args.graph)
    elif args.cmd == 'image':
        img2text(str(args.image), c[::-1], args.reverse)
    else:
        pass
