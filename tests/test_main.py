import builtins

import pytest

import main
from src.api import HeadHunterAPI
from src.vacancy import Vacancy


@pytest.fixture(autouse=True)
def patch_saver(monkeypatch):
    class DummySaver:
        def __init__(self, *args, **kwargs):
            pass

        def save_vacancies(self, vacs):
            pass

    monkeypatch.setattr(main, "JSONSaver", DummySaver)


def test_main_no_vacancies(monkeypatch, capsys):
    """Если API НЕ вернул, то main ничего не печатает"""
    inputs = iter(["", "5", "0", "3"])
    monkeypatch.setattr(
        builtins,
        "input",
        lambda prompt="": next(inputs),
    )
    monkeypatch.setattr(
        HeadHunterAPI,
        "get_vacancies",
        lambda self, q, per_page=None: [],
    )
    main.main()
    assert capsys.readouterr().out == ""


def test_main_with_vacancies(monkeypatch, capsys):
    vac1 = Vacancy(
        title="Low",
        company="Test Company",
        url="http://test.com",
        salary_from=100,
        salary_to=None,
        currency="RUR",
    )
    vac2 = Vacancy(
        title="High",
        company="Test Company",
        url="http://test.com",
        salary_from=200,
        salary_to=None,
        currency="RUR",
    )
    inputs = iter(["", "2", "150", "2"])
    monkeypatch.setattr(
        builtins,
        "input",
        lambda prompt="": next(inputs),
    )
    monkeypatch.setattr(
        HeadHunterAPI,
        "get_vacancies",
        lambda self, q, per_page=None: [vac1, vac2],
    )
    main.main()
    out = capsys.readouterr().out.strip().splitlines()
    assert out == [str(vac2)]
