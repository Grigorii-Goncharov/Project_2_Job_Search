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
        pass

class BaseSaver(ABC):
    """Абстрактный класс для работы с ваканаиями"""

    @abstractmethod
    def add_vacancy(self):
        """Абстрактный метод для добавления вакансии"""
        pass

    @abstractmethod
    def delete_vacancy(self):
        """Абстрактный метод для удаления вакансии"""
        pass

    @abstractmethod
    def save_vacancy(self):
        """Абстрактный метод для добавления вакансии"""
        pass

