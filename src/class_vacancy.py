import pprint
from src.class_api import HeadHunterAPI

class Vacancy:
    """Класс для обработки вакансий"""

    __slots__ = (
        "name",
        "link",
        "area",
        "__salary",
        "description",
        "salary_from",
        "salary_to",
    )

    def __init__(
        self,
        name: str,
        link: str,
        salary: dict[str, int, float],
        area: str,
        description: str
    ):

        self.name = name
        self.link = link
        self.area = area
        self.__salary = salary #Зарплата подробно в словаре
        self.description = description
        self.salary_from = self.__salary_from() #Валидируем строку от из словаря
        self.salary_to = self.__salary_to() #Валидируем строку до из словаря

    def __salary_from(self) -> int:
        """Валидация данных по зарплате для поля 'от'"""
        self.salary_from = 0
        if self.__salary:  # если есть данные о зарплате
            self.salary_from = self.__salary.get("from") or 0

            try:
                self.salary_from = int(self.salary_from)
            except (TypeError, ValueError):
                self.salary_from = 0
        return self.salary_from

    def __salary_to(self) -> int:
        """Валидация данных по зарплате для поля 'до'"""
        self.salary_to = 0
        if self.__salary:
            self.salary_to = self.__salary.get("to") or 0

            try:
                self.salary_to = int(self.salary_to)
            except (TypeError, ValueError):
                self.salary_to = 0
        return self.salary_to

    def __repr__(self) -> str:
        """Метод преобразования атрибутов в строку и вывод в консоль"""
        return (f"{self.name} "
                f"{self.link} "
                f"{self.area} "
                f"{self.__salary} "
                f"{self.description} "
                f"{self.salary_from} - "
                f"{self.salary_to}\n "
                )

    def __ge__(self, other):
        if not isinstance(other, Vacancy):
            raise AttributeError("Невозможно сравнить разные типы")
        return self.salary_from >= other.salary_from

    def __le__(self, other):
        if not isinstance(other, Vacancy):
            raise AttributeError("Невозможно сравнить разные типы")
        return self.salary_from <= other.salary_from

    def __gt__(self, other):
        if not isinstance(other, Vacancy):
            raise AttributeError("Невозможно сравнить разные типы")
        return self.salary_from > other.salary_from

    def __lt__(self, other):
        if not isinstance(other, Vacancy):
            raise AttributeError("Невозможно сравнить разные типы")
        return self.salary_from < other.salary_from

    @staticmethod
    def cast_to_object_list(data: dict) -> "Vacancy":
        """метод преобразования JSON данных в объект """
        vacancy_list = []

        for item in data:
            # Извлечение полей из JSON-объекта вакансии
            name = item.get("name")
            link = item.get("url")

            area_full = item.get("area")
            area = area_full.get("name")

            description = item.get("snippet", {}).get("responsibility") or item.get("description")

            salary = item.get("salary")

            # Создание объекта Vacancy
            vacancy = Vacancy(
                name=name,
                link=link,
                area=area,
                salary = salary,
                description=description
            )
            vacancy_list.append(vacancy)

        return vacancy_list





if __name__ == "__main__":
    vacancy = Vacancy('Python-разработчик',
                      'https://api.hh.ru/areas/1',
                      {'from': 150000, 'to': 300000, 'currency': 'RUR'},
                      "Москва",
                      "python")
    print(vacancy)
    load = HeadHunterAPI()  # создаем объект API
    result = load.get_vacancies('Разработчик')
    vacancy_json = vacancy.cast_to_object_list(result)
    pprint.pprint(vacancy_json)
