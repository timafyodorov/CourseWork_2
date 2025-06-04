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
    """Если API вернул пусто, main ничего не печатает"""
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
