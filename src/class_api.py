from src.class_abstract import BaseAPI
import requests
import pprint
from config import USER_AGENT


class HeadHunterAPI(BaseAPI):
    """Класс работы с HeadHunterAPI """

    def __init__(self) -> None:
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {'User-Agent': USER_AGENT}
        self.__vacancies = []

    @property
    def url(self) -> None:
        """Метод получение приватного атрибута url"""
        return self.__url

    @property
    def headers(self) -> None:
        """Метод получение приватного атрибута headers"""
        return self.__url

    @property
    def vacancies(self) -> None:
        """Метод получение приватного атрибута vacancies"""
        return self.__vacancies

    def __response_check(self) -> bool:
        """Проверяет доступность API"""
        try:
            response = requests.get(self.__url, timeout=5)
            response.raise_for_status()  # если status_code == 200
            return True
        except requests.exceptions.RequestException:
            return False

    def get_vacancies(self, text: str, per_page: int = 10) -> list[dict]:
        if not self.__response_check():
            raise ConnectionError("API недоступно. Невозможно получить вакансии.")

        params = {'text': text, 'per_page': per_page}
        try:
            response = requests.get(self.__url, headers=self.__headers, params=params)
            response.raise_for_status()  # Если код будет 200
            self.__vacancies = response.json().get('items', [])  # получение данных из items если найдет( или [] )
            return self.__vacancies
        except requests.exceptions.RequestException as e:  # отлов только сетевых ошибок
            raise ValueError(f"Ошибка при выполнении запроса: {e}") from e  # Сохранить историю ошибки from e


if __name__ == "__main__":
    load = HeadHunterAPI()  # создаем объект API
    vac = load.vacancies
    print(vac)
    result = load.get_vacancies('Рзработчик')
    # pprint.pprint(result)# получен json
    vac = load.vacancies
    print(vac)
