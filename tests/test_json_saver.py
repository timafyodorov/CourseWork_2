import json
from src.savers import JSONSaver
from src.vacancy import Vacancy


def mk_vacancy(title="Dev", company="Company", salary_from=100, salary_to=200,
               currency="RUB", url="http://example.com", description="desc") -> Vacancy:
    return Vacancy(
        title=title,
        company=company,
        description=description,
        salary={"from": salary_from, "to": salary_to, "currency": currency},
        url=url
    )


def test_prevent_duplicate_by_url(tmp_path):
    filename = tmp_path / "vacancies.json"
    saver = JSONSaver(str(filename))

    v1 = mk_vacancy(title="Python Dev", url="http://unique.com")
    saver.save_vacancies([v1])
    saver.save_vacancies([v1])  # попытка дублирования

    with open(filename, encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 1


def test_delete_all(tmp_path):
    filename = tmp_path / "vacancies.json"
    saver = JSONSaver(str(filename))

    v1 = mk_vacancy()
    saver.save_vacancies([v1])
    saver.delete_all()

    with open(filename, encoding="utf-8") as f:
        data = json.load(f)
    assert data == []
