import os
import pprint

# Получаем путь к текущему скрипту
script_dir = os.path.dirname(os.path.abspath(__file__))
path_to_json = os.path.join(script_dir, "../data/vacancy_result.json")

class Vacancy():
    """ Класс для работы с вакансиями"""
    __slots__ = ("text", "link", "salary_from_to", "experience")
    def __init__(self, text, link, salary_from_to, experience):
            self.text = text
            self.link = link
            self.salary_from_to = salary_from_to
            self.experience = experience

    def __repr__(self) -> str:
        """Метод преобразования атрибутов в строку и вывод в консоль"""
        return f"{self.text}, ссылка на вакансию: {self.link}, {self.salary_from_to} {self.experience}"

    @staticmethod
    def cast_to_object_list(data: dict) -> "Vacancy":
        """метод преобразования JSON данных в объект """
        vacancy_list = []

        for item in data:
            # Извлечение полей из JSON-объекта вакансии
            name = item.get("name")
            link = item.get("url")

            salary = item.get("salary")
            salary_from = salary.get("from")
            salary_to = salary.get("to")

            experience = item.get("experience")
            experience_name = experience.get("name")

            # Создание объекта Vacancy
            vacancy = Vacancy(
                text=name,
                link=link,
                salary_from_to=f'{salary_from}-{salary_to}',
                experience=experience_name
            )
            vacancy_list.append(vacancy)

        return vacancy_list






# if __name__ == "__main__":
#     vacancy = Vacancy("Python Developer", "<https://hh.ru/vacancy/123456>", "100 000-150 000 руб.",
#                       "Требования: опыт работы от 3 лет...")
#     print(vacancy)
