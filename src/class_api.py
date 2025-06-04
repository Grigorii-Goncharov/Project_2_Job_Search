import os

import requests

from config import USER_AGENT
from src.class_abstract import BaseAPI

# Получаем путь к текущему скрипту
script_dir = os.path.dirname(os.path.abspath(__file__))
path_to_json = os.path.join(script_dir, "../data/vacancy_hh.json")


class HeadHunterAPI(BaseAPI):
    """Метод запроса через API"""

    def __init__(self) -> None:
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": USER_AGENT}
        self.__vacancies = []

    @property
    def url(self) -> None:
        """Метод получение приватного атрибута url"""
        return self.__url

    @property
    def headers(self) -> None:
        """Метод получение приватного атрибута headers"""
        return self.__headers

    @property
    def vacancies(self) -> None:
        """Метод получение приватного атрибута vacancies"""
        return self.__vacancies

    def __response_check(self) -> bool:
        """Защищенный метод Проверяет доступность API - для внутренних методов"""
        try:
            response = requests.get(self.__url, timeout=5)
            response.raise_for_status()  # if status_code == 200
            return True
        except requests.exceptions.RequestException:
            return False

    def get_vacancies(self, text: str, per_page: int = 10) -> list[dict]:
        """Метод получения вакансий по API"""
        if not self.__response_check():
            raise ConnectionError("API недоступно. Невозможно получить вакансии.")

        params = {"text": text, "per_page": per_page}
        try:
            response = requests.get(self.__url, headers=self.__headers, params=params)
            response.raise_for_status()  # Если код будет 200
            self.__vacancies = response.json().get("items", [])  # получение items если найдет( или [] )
            return self.__vacancies
        except requests.exceptions.RequestException as e:  # отлов только сетевых ошибок
            raise ValueError(f"Ошибка при выполнении запроса: {e}") from e  # Сохранить историю ошибки from e


# if __name__ == "__main__":
#     load = HeadHunterAPI()  # создаем объект API
#     vac = load.get_vacancies
#     print(vac)
#     result = load.get_vacancies('Плотник')
#     print("=== Получаем вакансии с HH и сохраняем в файл ===")
#     print("Полученные сырые данные:", result)  # DEBUG
# pprint.pprint(result)# получен json
# vac = load.vacancies
# print(vac)
