from abc import ABC, abstractmethod


class BaseAPI(ABC):
    """Абстрактный класс для работы с API сервиса с вакансиями"""

    @abstractmethod
    def get_vacancies(self):
        """Абстрактный метод получения вакансий"""
        pass

    @property
    @abstractmethod
    def url(self):
        """ Абстрактный метод получение приватного атрибута url"""
        pass

    @property
    @abstractmethod
    def headers(self):
        """ Абстрактный метод получение приватного атрибута headers"""
        pass

    @property
    @abstractmethod
    def vacancies(self):
        """Абстрактный метод получение приватного атрибута vacancies"""
        pass


class BaseFileStorage(ABC):
    """Абстрактный класс для работы с файлами или хранилищами данных"""

    @property
    @abstractmethod
    def filepath(self):
        """Метод получение приватного атрибута filepath"""
        pass

    @abstractmethod
    def save_to_json(self):
        """Абстрактный метод загрузки сохранения в json"""
        pass

    @abstractmethod
    def load_from_json(self):
        """Абстрактный метод загрузки данных из json"""
        pass

    @abstractmethod
    def add_vacancy(self):
        """Абстрактный метод добавления вакансий"""
        pass

    @abstractmethod
    def delete_vacancy(self):
        """Абстрактный метод удаления вакансий по критерию"""
        pass

    @abstractmethod
    def search_vacancies_by_keyword(self):
        """Абстрактный метод поиска вакансии по ключевому слову"""
        pass

    @abstractmethod
    def filter_vacancies_by_keyword(self):
        """Абстрактный Метод фильтрации вакансии по ключевому слову"""
        pass

    @abstractmethod
    def filter_vacancies_by_salary_range(self):
        """Абстрактный Метод фильтрации вакансии по диапазону зарплат"""
        pass
