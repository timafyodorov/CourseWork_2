from abc import ABC, abstractmethod
from typing import Any, Dict, List

import requests


class BaseAPI(ABC):
    @abstractmethod
    def get_vacancies(self, keyword: str, per_page: int = 20) -> List[Dict[str, Any]]:
        pass


class HeadHunterAPI(BaseAPI):
    BASE_URL = "https://api.hh.ru/vacancies"

    def get_vacancies(self, keyword: str, per_page: int = 20) -> List[Dict[str, Any]]:
        params: Dict[str, str] = {"text": keyword}
        if per_page is not None:
            params["per_page"] = str(per_page)

        try:
            resp = requests.get(self.BASE_URL, params=params)
            resp.raise_for_status()
        except requests.RequestException:
            return []

        items = resp.json().get("items", [])
        return [self._parse(item) for item in items]

    @staticmethod
    def _parse(item: dict) -> Dict[str, Any]:
        salary = item.get("salary") or {}
        return {
            "title": item.get("name", ""),
            "company": item.get("employer", {}).get("name", ""),
            "from": salary.get("from"),
            "to": salary.get("to"),
            "currency": salary.get("currency"),
            "url": item.get("alternate_url", ""),
        }
