from src.utils import filter_by_keyword, filter_by_min_salary, sort_by_salary
from src.vacancy import Vacancy
from typing import Optional


def mk(
    title: str,
    company: str,
    salary_from: Optional[int],
    salary_to: Optional[int],
    currency: Optional[str],
    url: str
) -> Vacancy:
    """Хелпер для создания Vacancy"""
    return Vacancy(
        title=title,
        company=company,
        salary_from=salary_from,
        salary_to=salary_to,
        currency=currency,
        url=url if url.startswith('http') else f'http://{url}'
    )


def test_filter_by_keyword():
    """Фильтрация по ключевому слову"""
    v1 = mk("Engineer", "TechCorp", 100, 150, "USD", "u1")
    v2 = mk("Manager", "BizCorp", 200, 250, "USD", "u2")
    res = filter_by_keyword([v1, v2], "engine")
    assert v1 in res and v2 not in res


def test_filter_by_min_salary():
    """Фильтрация по минимальной зарплате"""
    v1 = mk("Dev", "A", 50, None, None, "u1")
    v2 = mk("Dev2", "B", 150, None, None, "u2")
    res = filter_by_min_salary([v1, v2], 100)
    assert v2 in res and v1 not in res


def test_sort_by_salary():
    v1 = mk("Low", "A", 50, None, None, "u1")
    v2 = mk("High", "B", 150, None, None, "u2")
    res = sort_by_salary([v1, v2])
    assert res == [v2, v1]
