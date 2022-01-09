import uniramp
import math

TEST_FONT = "tests/NotoSansCJK-Regular.ttc"


def is_equal(x: float, y: float, eps=1e-3):
    return math.isclose(x, y, abs_tol=eps)


def test_coverage_ascii():
    t = uniramp._uniramp.Typeface(TEST_FONT)

    assert is_equal(t.get_coverage(ord("a")), 0.199)
    assert is_equal(t.get_coverage(ord("b")), 0.237)


def test_coverage_CJK():
    t = uniramp._uniramp.Typeface(TEST_FONT)

    assert is_equal(t.get_coverage(ord("一")), 0.074)
    assert is_equal(t.get_coverage(ord("二")), 0.132)
