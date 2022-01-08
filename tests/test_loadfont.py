import uniramp
import pytest


def test_loadfont():
    t = uniramp._uniramp.Typeface("tests/NotoSansCJK-Regular.ttc")
    assert t.get_family_name() == "Noto Sans CJK JP"
    assert t.get_style_name() == "Regular"


def test_loadfont_with_valid_index():
    t = uniramp._uniramp.Typeface("tests/NotoSansCJK-Regular.ttc", 3)
    assert t.get_family_name() == "Noto Sans CJK TC"
    assert t.get_style_name() == "Regular"


def test_loadfont_with_invalid_index():
    with pytest.raises(ValueError):
        t = uniramp._uniramp.Typeface("tests/NotoSansCJK-Regular.ttc", -1)
    with pytest.raises(ValueError):
        t = uniramp._uniramp.Typeface("tests/NotoSansCJK-Regular.ttc", 100)
