import pytest
from src.vacancy import Vacancy


def test_vacancy_creation_minimal():
    v = Vacancy(
        title="Python Developer",
        company="Tech Inc",
        salary={"from": 100_000, "to": 150_000, "currency": "RUB"},
        url="http://example.com/vacancy/123",
        description="Great job for Python devs",
    )
    assert v.title == "Python Developer"
    assert v.company == "Tech Inc"
    assert v.salary_from == 100_000
    assert v.salary_to == 150_000
    assert v.currency == "RUB"
    assert v.salary == 100_000
    assert v.url.startswith("http")


def test_vacancy_creation_with_missing_salary():
    v = Vacancy(
        title="No Salary Job",
        company="Mystery Co",
        salary=None,
        url="http://example.com/no-salary",
        description="Salary is not disclosed",
    )
    assert v.salary_from == 0
    assert v.salary_to == 0
    assert v.currency == "RUB"
    assert v.salary == 0


@pytest.mark.parametrize("title", ["", "   "])
def test_invalid_title_raises(title):
    with pytest.raises(ValueError, match="Пустой заголовок вакансии"):
        Vacancy(
            title=title,
            company="BadTitle Inc",
            salary=None,
            url="http://example.com",
            description="Valid description",
        )


@pytest.mark.parametrize("url", ["", "ftp://invalid.com", "example.com"])
def test_invalid_url_raises(url):
    with pytest.raises(ValueError, match="Некорректный URL"):
        Vacancy(
            title="Invalid URL Job",
            company="URL Inc",
            salary=None,
            url=url,
            description="Valid description",
        )
