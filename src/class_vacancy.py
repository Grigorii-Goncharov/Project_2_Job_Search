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
        if self.__salary:  #
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
                f"{self.salary_from}-"
                f"{self.salary_to}\n"
                "--------------------------")

    def __ge__(self, other):
        """Методы сравнения конкретных вакансий"""
        if not isinstance(other, Vacancy):
            raise AttributeError("Невозможно сравнить разные типы")
        return self.salary_from >= other.salary_from

    def __le__(self, other):
        """Методы сравнения конкретных вакансий"""
        if not isinstance(other, Vacancy):
            raise AttributeError("Невозможно сравнить разные типы")
        return self.salary_from <= other.salary_from

    def __gt__(self, other):
        """Методы сравнения конкретных вакансий"""
        if not isinstance(other, Vacancy):
            raise AttributeError("Невозможно сравнить разные типы")
        return self.salary_from > other.salary_from

    def __lt__(self, other):
        """Методы сравнения конкретных вакансий"""
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

    @staticmethod
    def sort_vacancies_by_salary(vacancies: list["Vacancy"], reverse: bool = True) -> list["Vacancy"]:
        """Сортировка списка вакансий по зарплате (по возрастанию или убыванию)"""
        return sorted(vacancies, key=lambda v: v.salary_from, reverse=reverse)


    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data.get("name"),
            link=data.get("link"),
            area=data.get("area"),
            salary={"from": data.get("salary_from"), "to": data.get("salary_to")},
            description=data.get("description")
        )

    # В class Vacancy:
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "link": self.link,
            "area": self.area,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
            "description": self.description
        }


# if __name__ == "__main__":
    # hh_api = HeadHunterAPI() # создаем объект API
    # data = hh_api.get_vacancies("Python разработчик")
    # vacancy = Vacancy('Плотник',
    #                   'https://api.hh.ru/areas/1',
    #                   {'from': 5000000, 'to': 180000, 'currency': 'RUR'},
    #                   "Москва",
    #                   "Выполнение столярно-плотницких работ")
    #
    # print(vacancy)
    # pprint.pprint(vacancies)

    # vacancies = Vacancy.cast_to_object_list(data)
    # if len(vacancies) >= 2:
    #     if vacancies[0] > vacancies[9]:
    #         print("Вакансия 0 лучше вакансии 1")
    #     elif vacancies[0] < vacancies[1]:
    #         print("Вакансия 1 лучше вакансии 0")
    #     else:
    #         print("Зарплаты равны")
    # else:
    #     print("Недостаточно вакансий для сравнения")

    # # Сортируем по возрастанию зарплаты
    # sorted_vacancies_asc = Vacancy.sort_vacancies_by_salary(vacancies)
    #
    # # Сортируем по убыванию зарплаты
    # sorted_vacancies_desc = Vacancy.sort_vacancies_by_salary(vacancies, reverse=False)
    #
    # # Выводим результат
    # for vacancy in sorted_vacancies_desc:
    #     print(vacancy)
