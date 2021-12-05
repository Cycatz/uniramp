from ._uniramp import Typeface

__all__ = [
    'main'
]


def main():
    # tf = Typeface("/home/cycatz/.local/share/fonts/Apple_Fonts/Arial/Arial.ttf")
    tf = Typeface("/home/cycatz/.local/share/fonts/Inconsolata_git/Inconsolata-Regular.otf")
    print(tf)
    print(tf.num_glyph())

    # for c in range(ord('A'), ord('Z') + 1):
    #     print('Current character: ', chr(c))
    #     tf.load_glyph(c)


    for c in '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft':
        print('Current character: ', c)
        print(tf.load_glyph(ord(c)))
