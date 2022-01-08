import uniramp

def test_loadfont():
    t = uniramp._uniramp.Typeface("tests/NotoSansCJK-Regular.ttc")
    assert t.get_family_name() == "Noto Sans CJK JP"
    assert t.get_style_name() == "Regular"
