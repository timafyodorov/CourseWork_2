from src.vacancy import Vacancy


def test_validation():
    v = Vacancy("Test", "Company", None, None, "RUR", "http://test.com")
    assert v.salary_from == 0
    assert v.salary_to == 0
    try:
        Vacancy("Test", "Company", 100, 200, "RUR", "invalid_url")
        assert False
    except ValueError:
        pass


def test_comparison():
    v1 = Vacancy("Low", "Company", 100, 200, "RUR", "http://test.com")
    v2 = Vacancy("High", "Company", 200, 300, "RUR", "http://test.com")
    assert v1 < v2
    assert v2 > v1
    assert v1 != v2

