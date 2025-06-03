import pytest
from src.utils import filter_by_keyword, filter_by_min_salary, sort_by_salary
from src.vacancy import Vacancy


def mk(
    title: str,
    company: str,
    salary_from: int,
    salary_to: int,
    currency: str,
    url: str,
    description: str = "Описание вакансии"
) -> Vacancy:
    if not url.startswith("http"):
        url = f"http://{url}"

    return Vacancy(
        title=title,
        company=company,
        salary={"from": salary_from, "to": salary_to, "currency": currency},
        url=url,
        description=description,
    )


def test_filter_by_keyword_matches_title():
    v1 = mk("Python Developer", "OpenAI", 100, 150, "RUB", "u1")
    v2 = mk("Java Developer", "Yandex", 120, 160, "RUB", "u2")
    res = filter_by_keyword([v1, v2], "python")
    assert v1 in res
    assert v2 not in res


def test_filter_by_keyword_matches_company():
    v1 = mk("Developer", "Pythonic Corp", 100, 150, "RUB", "u1")
    v2 = mk("Developer", "C++ Corp", 120, 160, "RUB", "u2")
    res = filter_by_keyword([v1, v2], "python")
    assert v1 in res
    assert v2 not in res


def test_filter_by_min_salary():
    v1 = mk("LowPay", "CheapCo", 50, 100, "RUB", "u1")
    v2 = mk("HighPay", "RichCo", 200, 300, "RUB", "u2")
    res = filter_by_min_salary([v1, v2], 150)
    assert v2 in res
    assert v1 not in res


def test_sort_by_salary_descending():
    v1 = mk("Low", "A", 50, 100, "RUB", "u1")
    v2 = mk("Mid", "B", 100, 150, "RUB", "u2")
    v3 = mk("High", "C", 200, 250, "RUB", "u3")
    res = sort_by_salary([v1, v2, v3])
    assert res == [v3, v2, v1]
