# Ref: https://github.com/RameshAditya/asciify/blob/master/asciify.py

from PIL import Image

__all__ = [
    'img2text'
]


'''
method resize():
    - takes as parameters the image, and the final width
    - resizes the image into the final width while maintaining aspect ratio
'''
def resize(image, new_width):
    (old_width, old_height) = image.size
    aspect_ratio = float(old_height)/float(old_width)
    new_height = int(aspect_ratio * new_width)
    new_dim = (new_width, new_height)
    new_image = image.resize(new_dim)
    return new_image


'''
method grayscalify():
    - takes an image as a parameter
    - returns the grayscale version of image
'''
def grayscalify(image):
    return image.convert('L')


'''
method modify():
    - replaces every pixel with a character whose intensity is similar
'''
def modify(image, coverage):
    # Assume the gray level = 2 ^ 8 = 256
    GRAY_LEVEL = 256

    pixels = list(image.getdata())
    coverage_len = len(coverage)
    new_pixels = [coverage[int(pixel_val / GRAY_LEVEL * coverage_len)][0] for pixel_val in pixels]
    return ''.join(new_pixels)


'''
method convert():
    - does all the work by calling all the above functions
'''
def convert(image, coverage, new_width):
    image = resize(image, new_width)
    image = grayscalify(image)
    pixels = modify(image, coverage)
    len_pixels = len(pixels)

    # Construct the image from the character list
    new_image = [pixels[index:index+new_width] for index in range(0, len_pixels, new_width)]
    return '\n'.join(new_image)


def img2text(coverage, path, width, outfile):
    if width is None or width <= 0:
        width = 80
    with Image.open(path) as image:
        new_image = convert(image, coverage, width)
        if outfile is None:
            print(new_image)
        else:
            with open(outfile, 'w') as f:
                f.write(new_image)

