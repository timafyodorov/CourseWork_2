import pytest
from unittest.mock import patch, Mock
from src.api import HeadHunterAPI


@pytest.fixture
def api():
    return HeadHunterAPI()


def test_parse_valid_item():
    item = {
        "name": "Python Developer",
        "employer": {"name": "OpenAI"},
        "salary": {"from": 100000, "to": 150000, "currency": "RUB"},
        "alternate_url": "https://hh.ru/vacancy/123"
    }
    parsed = HeadHunterAPI._parse(item)
    assert parsed["title"] == "Python Developer"
    assert parsed["company"] == "OpenAI"
    assert parsed["salary_from"] == 100000
    assert parsed["salary_to"] == 150000
    assert parsed["currency"] == "RUB"
    assert parsed["url"] == "https://hh.ru/vacancy/123"


@patch("src.api.requests.get")
def test_get_vacancies_success(mock_get, api):
    mock_response = Mock()
    mock_response.json.return_value = {
        "items": [
            {
                "name": "Data Scientist",
                "employer": {"name": "DataCorp"},
                "salary": {"from": 200000, "to": 300000, "currency": "RUB"},
                "alternate_url": "https://hh.ru/vacancy/456"
            }
        ]
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    vacancies = api.get_vacancies("data", per_page=1)
    assert isinstance(vacancies, list)
    assert len(vacancies) == 1
    assert vacancies[0]["title"] == "Data Scientist"
