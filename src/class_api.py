from src.class_abstract import BaseAPI
import requests
import pprint


class HeadHunterAPI(BaseAPI):
    """Класс работы с HeadHunterAPI """

    def __init__(self, url):
        self.__url = url

    @property
    def url(self):
        """Метод получения получения приватного атрибута - ссылки"""
        return self.__url

    def __answer_check(self):
        """Метод получения ответа по запросу по ссылке"""
        try:
            answer_code = requests.get(self.url, timeout=3)
            if answer_code.status_code == 200 or answer_code.status_code == 300:
                return True
        except requests.exceptions.RequestException:
            return False

    def get_vacancies(self, text, per_page=10):
        """Метод получения Вакансий """

        if not self.__answer_check():
            raise ConnectionError("Отсутствует подключение к сети")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"}
        params = {'text': text.lower(), 'per_page': per_page}
        try:
            vacancy_resp = requests.get(self.url, headers=headers, params=params)
            return vacancy_resp.json().get('items', [])
        except:
            if not vacancy_resp:
                raise ValueError(f'Запрос {vacancy_resp} недоступен!')


# if __name__ == "__main__":
#     url1 = "https://api.hh.ru/vacancies"
#     test_api = HeadHunterAPI(url1)
#     vacancies = test_api.get_vacancies('Водитель')
#     pprint.pprint(len(vacancies))
