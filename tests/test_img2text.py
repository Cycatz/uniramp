import os
from uniramp import coverage
from uniramp.coverage import Coverage
from uniramp.img2text import img2text


TEST_FONT = "tests/NotoSansCJK-Regular.ttc"
TEST_IMAGE = "tests/octocat.png"
TEST_IMAGE_WIDTH = 10
TEST_OUTFILE = '/tmp/test.txt'


def get_img2text(character_set):
    image_data = []

    cov = coverage.Coverage(TEST_FONT, character_set)
    c = cov.get_coverage()[::-1]
    img2text(c, TEST_IMAGE, TEST_IMAGE_WIDTH, TEST_OUTFILE)

    with open(TEST_OUTFILE) as f:
        image_data = f.readlines() 
    os.unlink(TEST_OUTFILE)

    return image_data

def test_img2text_ascii():
    TEST_OUTPUT_IMAGE = ['jjjQbbRjjj\n',
                         'jjjqzzdjjj\n',
                         'jjjIpbWjjj\n',
                         'jjjfhVjjjj\n',
                         'jjjgMMgjjj']

    assert get_img2text(None) == TEST_OUTPUT_IMAGE

def test_img2text_CJK():
    TEST_CHARSET = "一二三四五六七八九十"
    TEST_OUTPUT_IMAGE = ['四四四五七七四四四四\n',
                         '四四四七八八九四四四\n',
                         '四四四九七七五四四四\n',
                         '四四四四三六四四四四\n',
                         '四四四四五五四四四四']

    assert get_img2text(TEST_CHARSET) == TEST_OUTPUT_IMAGE
