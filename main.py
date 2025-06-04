from src.api import HeadHunterAPI
from src.savers import JSONSaver
from src.utils import filter_by_keyword, filter_by_min_salary, sort_by_salary
from src.vacancy import Vacancy


def main() -> None:
    """Сбор, фильтрация и вывод вакансий по заданным критериям"""
    api = HeadHunterAPI()
    saver = JSONSaver()

    query = input("🔎 Введите поисковый запрос: ")
    per_page = int(input("📄 Сколько вакансий загрузить: "))
    min_salary = int(input("💰 Минимальная зарплата: "))
    top_n = int(input("🏆 Сколько топ-вакансий показать: "))

    vacancies_dicts = api.get_vacancies(query, per_page=per_page)

    vacancies = [
        Vacancy(
            title=item["title"],
            company=item["company"],
            description=item.get("description", ""),
            salary={"from": item.get("from"), "to": item.get("to")},
            url=item["url"],
        )
        for item in vacancies_dicts
    ]

    saver.save_vacancies(vacancies)

    filtered_kw = filter_by_keyword(vacancies, query)
    filtered = filter_by_min_salary(filtered_kw, min_salary)
    sorted_all = sort_by_salary(filtered)

    for vac in sorted_all[:top_n]:
        print(vac)


if __name__ == "__main__":
    main()
