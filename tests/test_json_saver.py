import pytest

from src.savers import JSONSaver
from src.vacancy import Vacancy


@pytest.fixture
def tmp_file(tmp_path):
    return str(tmp_path / "test.json")


def test_save_and_load_and_delete(tmp_path):
    """Тест для загрузки и сохранения вакансий"""
    file_path = tmp_path / "test.json"
    saver = JSONSaver(str(file_path))
    vacancy = Vacancy(
        title="Python Dev",
        company="Test Company",
        url="http://test.com",
        salary_from=100000,
        salary_to=150000,
        currency="RUR",
    )
    saver.save_vacancies([vacancy])
    loaded = saver.load_vacancies()
    assert len(loaded) == 1
    assert loaded[0].title == vacancy.title


