import os
import json
import re
from typing import Union
from src.class_vacancy import Vacancy
from src.class_abstract import BaseFileStorage


class JSONSaver(BaseFileStorage):
    """Класс для сохранения и загрузки данных о вакансиях в/из JSON-файла."""

    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.__filepath = os.path.join(script_dir, "../data/vacancies_hh.json")
        os.makedirs(os.path.dirname(self.__filepath), exist_ok=True)

    @property
    def filepath(self):
        """Метод получение приватного атрибута filepath"""
        return self.__filepath

    def _write_to_file(self, data: list) -> None:
        try:
            with open(self.filepath, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            print("Данные успешно записаны в файл.")
        except Exception as e:
            raise IOError(f"Ошибка при записи в файл: {e}")

    def save_to_json(self, vacancies: list) -> None:
        try:
            if isinstance(vacancies[0], Vacancy):
                data = [vacancy.to_dict() for vacancy in vacancies]
            else:
                data = vacancies
            print("Пример данных для записи:", data[:2])  # DEBUG: первые две вакансии
            self._write_to_file(data)
            print(f"Данные успешно сохранены в {self.filepath}")
        except Exception as e:
            print(f"Ошибка при сохранении данных в JSON: {e}")

    def load_from_json(self) -> list:
        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data  # Возвращаем словари, а не объекты Vacancy
        except FileNotFoundError:
            print(f"Файл {self.filepath} не найден.")
            return []
        except json.JSONDecodeError:
            print(f"Ошибка чтения JSON из файла {self.filepath}.")
            return []

    def add_vacancy(self, vacancy: Union[Vacancy, dict]) -> None:
        current_data = self.load_from_json()  # Теперь это список словарей

        if isinstance(vacancy, Vacancy):
            vacancy_dict = vacancy.to_dict()
        elif isinstance(vacancy, dict):
            vacancy_dict = vacancy
        else:
            raise ValueError("Можно добавлять только объект Vacancy или словарь.")

        existing_id = {item["id"] for item in current_data}
        if vacancy_dict["id"] in existing_id:
            print("Вакансия с такой ссылкой уже существует. Дубликат не добавлен.")
            return

        current_data.append(vacancy_dict)

        try:
            self._write_to_file(current_data)
            print("Новая вакансия успешно добавлена.")
        except IOError as e:
            print(e)

    def delete_vacancy(self, id: str) -> None:
        data = self.load_from_json()
        filtered_data = [item for item in data if item.get("id") != id]

        if len(data) == len(filtered_data):
            print(f"Вакансия с ссылкой {id} не найдена.")
        else:
            self._write_to_file(filtered_data)
            print(f"Вакансия с ссылкой {id} успешно удалена.")

    def search_vacancies_by_keyword(self, keyword: str) -> list:
        """
        Ищет вакансии по ключевому слову во всех полях: name, description, area.
        """
        data = self.load_from_json()
        pattern = re.compile(keyword, re.IGNORECASE)

        result = [
            item for item in data
            if pattern.search(item.get("name", ""))
               or pattern.search(item.get("description", ""))
               or pattern.search(item.get("area", ""))
        ]

        print(f"Найдено {len(result)} вакансий по ключевому слову '{keyword}'.")
        return result

    def filter_vacancies_by_keyword(self, keyword: str) -> list[Vacancy]:
        """Метод фильтрации вакансии по ключевому слову"""
        data = self.load_from_json()
        pattern = re.compile(keyword, re.IGNORECASE)

        filtered_data = [
            item for item in data
            if pattern.search(item.get("name", ""))
               or pattern.search(item.get("description", ""))
               or pattern.search(item.get("area", ""))
        ]

        result = Vacancy.cast_to_object_list(filtered_data)
        print(f"Отфильтровано {len(result)} вакансий по ключевому слову '{keyword}'.")
        return result

    def filter_vacancies_by_salary_range(self, salary_range: str) -> list[Vacancy]:
        """Метод фильтрации вакансии по диапазону зарплат"""
        try:
            min_salary, max_salary = map(int, salary_range.split("-"))
        except ValueError:
            raise ValueError("Диапазон зарплат должен быть в формате 'мин-макс', например '50000-100000'.")

        data = self.load_from_json()
        filtered_data = []

        for item in data:
            salary_from = item.get("salary_from", 0)
            salary_to = item.get("salary_to", 0)

            if (salary_from and min_salary <= salary_from <= max_salary) or \
                    (salary_to and min_salary <= salary_to <= max_salary):
                filtered_data.append(item)

        result = Vacancy.cast_to_object_list(filtered_data)
        print(f"Отфильтровано {len(result)} вакансий по диапазону зарплат {salary_range}.")
        return result

    def load_vacancies(self) -> list[Vacancy]:
        """Загружает вакансии и возвращает их как объекты Vacancy"""
        data = self.load_from_json()
        return Vacancy.cast_to_object_list(data)

# if __name__ == "__main__":
#     # Инициализация API и JSONSaver
#     hh_api = HeadHunterAPI()
#     saver = JSONSaver()
# #
#     print("=== Получаем вакансии с HH и сохраняем в файл ===")
#     raw_vacancies = hh_api.get_vacancies("Строитель", per_page=5)
#     vacancies_list = Vacancy.cast_to_object_list(raw_vacancies)
#     saver.save_to_json(vacancies_list)  # Сохраняем в JSON
# #
#     print("\n=== Выводим все загруженные вакансии ===")
#     all_vacancies = saver.load_vacancies()
#     for v in all_vacancies:
#         print(f"{v.name} | {v.area} | {v.salary_from}-{v.salary_to} | {v.id}") # Получаем объекты Vacancy
# #
#     print("\n=== Добавляем новую вакансию как объект Vacancy ===")
#     new_vacancy = Vacancy(
#         id="123456789",
#         name="Тестовая должность",
#         area="Урюпинск",
#         salary={"from": 25000, "to": 40000, "currency": "RUR"},
#         description="Тестовый наборчик непонятных тестов"
#     )
#     saver.add_vacancy(new_vacancy)# Добавляем и записываем вакансию как объект Vacancy
# #
#     print("\n=== Ищем вакансии по ключевому слову ===")
#     results_by_keyword = saver.search_vacancies_by_keyword("Волгоград")
#     for v in results_by_keyword:
#         print(f"{v['name']} | {v['area']}") # Поиск вакансии по ключ-слову
# #
#     print("\n=== Фильтруем вакансии по зарплате от 70 000 до 150 000 ===")
#     filtered_by_salary = saver.filter_vacancies_by_salary_range("70000-150000")
#     for vacancy in filtered_by_salary:
#         print(f"{vacancy.name} | {vacancy.salary_from}-{vacancy.salary_to} | {vacancy.id}")  # Фильтрация вакансии по диапазоу ЗП
# #
#     print("\n=== Удаляем вакансию по id ===")
#     saver.delete_vacancy_by_id("1234567890")  # Удаление вакансии из JSON по ID
# #
#     print("\n=== Проверяем итоговый список вакансий после всех изменений ===")
#     final_vacancies = saver.load_from_json()
#     for vacancy in final_vacancies:
#         print(f"{vacancy.get('name')} | {vacancy.get('area')} | {vacancy.get('salary_from')}-{vacancy.get('salary_to')} | {vacancy.get('id')}")
#         # Вывод итоговый по наличию вакансий
# #
#     print("\n=== Содержимое файла после сохранения ===")
#     with open(saver.filepath, "r", encoding="utf-8") as f:
#         content = json.load(f)  # Загружаем данные как JSON-объект (список словарей)
#     print("Выводим вакансии напрямую из файла:")
#     for vacancy in content:
#         print(vacancy["name"], vacancy["salary_from"], vacancy["id"])  # Вывод итогового списка, но сразу из файла
# #
#     print("\nПуть к файлу:", saver.filepath)
