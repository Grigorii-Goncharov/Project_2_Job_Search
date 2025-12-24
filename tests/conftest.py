import pytest
import json
from src.class_api import HeadHunterAPI
from src.class_vacancy import Vacancy


# Фикстура для создания экземпляра API
@pytest.fixture
def hh_api():
    return HeadHunterAPI()


@pytest.fixture
def vacancy_data():
    return [
        {
            "name": "Python разработчик",
            "id": "123456",
            "area": {"name": "Москва"},
            "salary": {"from": 80000, "to": 120000},
            "description": "Работа с Python"
        },
        {
            "name": "Junior Python",
            "id": "789012",
            "area": {"name": "Новосибирск"},
            "salary": {"from": 60000, "to": 90000},
            "description": "Стажировка"
        }
    ]


@pytest.fixture
def vacancies(vacancy_data):
    return Vacancy.cast_to_object_list(vacancy_data)


# Фикстура для временного пути к файлу
@pytest.fixture
def tmp_json_file(tmp_path):
    return tmp_path / "vacancies_hh.json"


# Фикстура с тестовыми данными
@pytest.fixture
def test_vacancies():
    return [
        {
            "name": "Python разработчик",
            "id": "123456",
            "area": "Москва",
            "salary": {"from": 80000, "to": 120000},
            "description": "Работа с Python"
        },
        {
            "name": "Junior Python",
            "id": "789012",
            "area": "Новосибирск",
            "salary": {"from": 60000, "to": 90000},
            "description": "Стажировка"
        }
    ]


# Фикстура для подготовки тестовых данных
@pytest.fixture
def setup_salary_data(tmp_path):
    test_file = tmp_path / "vacancies_hh.json"

    test_data = [
        {
            "name": "Python разработчик",
            "id": "123456",
            "area": "Москва",
            "salary": {"from": 80000, "to": 120000},
            "description": "Работа с Python",
            "salary_from": 80000,
            "salary_to": 120000
        },
        {
            "name": "Junior Python",
            "id": "789012",
            "area": "Новосибирск",
            "salary": {"from": 60000, "to": 90000},
            "description": "Стажировка",
            "salary_from": 60000,
            "salary_to": 90000
        },
        {
            "name": "Без указания зарплаты",
            "id": "no_salary",
            "area": "Екатеринбург",
            "salary": None,
            "description": "Зарплата не указана",
            "salary_from": 0,
            "salary_to": 0
        }
    ]

    # Сохраняем данные в временный JSON-файл
    with open(test_file, "w", encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=4)

    return str(test_file)


@pytest.fixture
def setup_keyword_data(tmp_path):
    test_file = tmp_path / "vacancies_hh.json"

    data = [
        {
            "name": "Python разработчик",
            "id": "123456",
            "area": "Москва",
            "description": "Ищем Python программиста для разработки backend",
            "salary_from": 80000,
            "salary_to": 120000
        },
        {
            "name": "Junior Python",
            "id": "789012",
            "area": "Новосибирск",
            "description": "Стажировка для начинающих",
            "salary_from": 40000,
            "salary_to": 60000
        },
        {
            "name": "Java разработчик",
            "id": "345678",
            "area": "Санкт-Петербург",
            "description": "Работа с Java и Spring",
            "salary_from": 90000,
            "salary_to": 130000
        }
    ]

    with open(test_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return str(test_file)
