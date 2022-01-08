import uniramp
import pytest

TEST_FONT = "tests/NotoSansCJK-Regular.ttc"


def test_loadfont():
    t = uniramp._uniramp.Typeface(TEST_FONT)
    assert t.get_family_name() == "Noto Sans CJK JP"
    assert t.get_style_name() == "Regular"


def test_loadfont_with_valid_index():
    t = uniramp._uniramp.Typeface(TEST_FONT, 3)
    assert t.get_family_name() == "Noto Sans CJK TC"
    assert t.get_style_name() == "Regular"


def test_loadfont_with_invalid_index():
    with pytest.raises(ValueError):
        t = uniramp._uniramp.Typeface(TEST_FONT, -1)
    with pytest.raises(ValueError):
        t = uniramp._uniramp.Typeface(TEST_FONT, 100)
