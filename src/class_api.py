
from src.class_abstract import BaseAPI
import requests
import pprint

class HeadHunterAPI(BaseAPI):
    """Класс работы с HeadHunterAPI """
    def __init__(self, url):
        self.url = url

    def get_vacancies(self):
        """Метод получения Вакансий """
        self.headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36" }
        vacancy_resp = requests.get(self.url, headers=self.headers)
        if not vacancy_resp:
            raise ValueError(f'Запрос {vacancy_resp} недоступен!')
        vacancy_data = vacancy_resp.json()
        return vacancy_data

if __name__ == "__main__":
    url = "https://api.hh.ru/vacancies"
    test_api = HeadHunterAPI(url)
    vacancies = test_api.get_vacancies()
    pprint.pprint(vacancies)