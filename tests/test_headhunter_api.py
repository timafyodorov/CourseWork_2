import pytest
import requests

from src.api import HeadHunterAPI
from src.vacancy import Vacancy


class DummyResponse:
    def __init__(self, status_code=200, json_data=None):
        self.status_code = status_code
        self._json = json_data or {"items": []}

    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.HTTPError(f"HTTP {self.status_code}")

    def json(self):
        return self._json


def dummy_get(url, params=None):
    if params is None:
        return DummyResponse(status_code=200)
    item = {
        "name": "TestVac",
        "employer": {"name": "TestCo"},
        "salary": {"from": 100, "to": 200, "currency": "USD"},
        "alternate_url": "http://test",
    }
    return DummyResponse(status_code=200, json_data={"items": [item]})


@pytest.fixture
def mock_response(requests_mock):
    mock_data = {
        "items": [
            {
                "name": "Python Developer",
                "url": "http://test.com",
                "salary": {"from": 100000, "to": 150000},
                "snippet": {"requirement": "Test description"},
            }
        ]
    }
    requests_mock.get("https://api.hh.ru/vacancies", json=mock_data)
    return mock_data


def test_get_vacancies_success(requests_mock):
    items = [
        {
            "name": "TestVac",
            "employer": {"name": "TestCo"},
            "salary": {"from": 100, "to": 200, "currency": "USD"},
            "alternate_url": "http://test",
        }
    ]
    requests_mock.get(HeadHunterAPI.BASE_URL, json={"items": items})
    api = HeadHunterAPI()
    result = api.get_vacancies("python", per_page=1)
    assert isinstance(result, list) and len(result) == 1
    vac = result[0]
    assert isinstance(vac, Vacancy)
    assert vac.title == "TestVac"
    assert vac.company == "TestCo"
    assert vac.salary_from == 100
    assert vac.salary_to == 200
    assert vac.currency == "USD"
    assert vac.url == "http://test"


def test_get_vacancies_http_error(requests_mock):
    requests_mock.get(HeadHunterAPI.BASE_URL, status_code=500)
    api = HeadHunterAPI()
    assert api.get_vacancies("irrelevant") == []


def test_get_vacancies_network_error(monkeypatch):
    """При сетевой ошибке возвращает пустой список"""

    def fail(*args, **kwargs):
        raise requests.RequestException("network fail")

    monkeypatch.setattr(requests, "get", fail)
    api = HeadHunterAPI()
    assert api.get_vacancies("x") == []
