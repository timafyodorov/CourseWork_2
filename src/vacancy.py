from typing import Dict, Optional


class Vacancy:
    def __init__(
        self,
        title: str,
        salary: Optional[Dict],
        url: str,
        description: str,
        company: Optional[str] = None,
        city: Optional[str] = None,
        experience: Optional[str] = None,
        employment: Optional[str] = None,
    ):
        self.__validate_title(title)
        self.__validate_url(url)
        self.__validate_description(description)

        self.title = title
        self.url = url
        self.description = description
        self.company = company
        self.city = city
        self.experience = experience
        self.employment = employment

        self.salary_from, self.salary_to, self.currency = self.__process_salary(salary)
        self.salary = self.salary_from  # для сравнения (__lt__, __gt__, __eq__)

    def __validate_title(self, title: str) -> str:
        if not title.strip():
            raise ValueError("Пустой заголовок вакансии")
        return title

    def __validate_url(self, url: str) -> str:
        if not url.startswith("http"):
            raise ValueError("Некорректный URL")
        return url

    def __validate_description(self, description: str) -> str:
        if not description.strip():
            raise ValueError("Пустое описание вакансии")
        return description

    def __process_salary(self, salary: Optional[Dict]) -> tuple[int, int, str]:
        if not salary:
            return 0, 0, "RUB"
        salary_from = salary.get("from") or 0
        salary_to = salary.get("to") or 0
        currency = salary.get("currency") or "RUB"
        return salary_from, salary_to, currency

    def __lt__(self, other):
        return self.salary_from < other.salary_from

    def __gt__(self, other):
        return self.salary_from > other.salary_from

    def __eq__(self, other):
        return self.salary_from == other.salary_from

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "company": self.company,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
            "currency": self.currency,
            "url": self.url,
        }


