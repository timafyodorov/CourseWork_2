import json
import os

VACANCIES_FILE = "vacancies.json"


def load_vacancies(filename):
    """Загружает вакансии из JSON-файла"""
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден.")
        return []

    with open(filename, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            print("Ошибка чтения JSON-файла")
            return []


def filter_vacancies_by_salary(vacancies, min_salary):
    """Фильтрует вакансии по минимальной зарплате"""
    filtered = []
    for vacancy in vacancies:
        salary_from = vacancy.get("salary_from") or 0
        salary_to = vacancy.get("salary_to") or 0

        try:
            salary_from = float(salary_from)
        except (ValueError, TypeError):
            salary_from = 0

        try:
            salary_to = float(salary_to)
        except (ValueError, TypeError):
            salary_to = 0

        salary = salary_from if salary_from else salary_to

        if salary >= min_salary:
            filtered.append(vacancy)
    return filtered


def print_vacancies(vacancies):
    """Выводит вакансии в консоль."""
    if not vacancies:
        print("Нет подходящих вакансий")
        return

    for idx, vacancy in enumerate(vacancies, 1):
        title = vacancy.get("name", "Без названия")
        employer = vacancy.get("employer", {}).get("name", "Неизвестный работодатель")
        city = vacancy.get("area", {}).get("name", "Не указан")
        salary_from = vacancy.get("salary_from", "—")
        salary_to = vacancy.get("salary_to", "—")
        url = vacancy.get("alternate_url", "Ссылка недоступна")

        print(f"{idx}. {title}")
        print(f"   Работодатель: {employer}")
        print(f"   Город: {city}")
        print(f"   Зарплата: от {salary_from} до {salary_to}")
        print(f"   Ссылка: {url}")
        print("-" * 60)


def main():
    vacancies = load_vacancies(VACANCIES_FILE)

    if not vacancies:
        return

    try:
        min_salary = float(input("Введите минимальную желаемую зарплату: "))
    except ValueError:
        print("Ошибка: введите числовое значение")
        return

    suitable = filter_vacancies_by_salary(vacancies, min_salary)
    print_vacancies(suitable)


if __name__ == "__main__":
    main()
