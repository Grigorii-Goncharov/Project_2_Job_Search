import json
from src.class_json import JSONSaver
from src.class_vacancy import Vacancy

# Вспомогательная функция для очистки файла перед тестами
def setup_test_file(data=None):
    saver = JSONSaver()
    with open(saver.filepath, "w", encoding="utf-8") as f:
        json.dump(data or [], f, ensure_ascii=False, indent=4)
    return saver


def test_save_to_json():
    """Тест: запись вакансий в JSON"""
    print("\n=== Тест: save_to_json ===")
    saver = JSONSaver()

    mock_data = [
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
            "salary": {"from": 40000, "to": 60000},
            "description": "Стажировка"
        }
    ]

    saver.save_to_json(mock_data)

    with open(saver.filepath, "r", encoding="utf-8") as file:
        result = json.load(file)

    assert len(result) == 2, "Должно быть 2 вакансии"
    assert result[0]["name"] == "Python разработчик"
    print(" test_save_to_json — пройден")


def test_load_from_json():
    """Тест: загрузка данных из файла"""
    print("\n=== Тест: load_from_json ===")
    saver = setup_test_file([
        {
            "name": "Тестировщик",
            "id": "test_123",
            "area": "Санкт-Петербург",
            "salary": {"from": 50000, "to": 80000},
            "description": "Писать тесты"
        }
    ])

    data = saver.load_from_json()
    assert isinstance(data, list), "Ожидается список словарей"
    assert data[0]["name"] == "Тестировщик"
    print(" test_load_from_json — пройден")


def test_add_vacancy():
    """Тест: добавление новой вакансии как объекта или словаря"""
    print("\n=== Тест: add_vacancy ===")
    saver = setup_test_file([])

    vacancy = Vacancy(
        name="Добавленный тестировщик",
        id="new_test_123",
        area="Екатеринбург",
        salary={"from": 60000, "to": 90000},
        description="Писать тесты"
    )

    # Добавляем как объект
    saver.add_vacancy(vacancy)

    # Проверяем, что вакансия добавилась
    data = saver.load_from_json()
    assert len(data) == 1
    assert data[0]["name"] == "Добавленный тестировщик"

    # Попробуем добавить дубликат
    saver.add_vacancy(vacancy)
    data = saver.load_from_json()
    assert len(data) == 1, "Дубликат не должен добавляться"

    print(" test_add_vacancy — пройден")


def test_delete_vacancy_by_id():
    """Тест: удаление вакансии по ID"""
    print("\n=== Тест: delete_vacancy_by_id ===")
    test_data = [
        {"name": "Вакансия 1", "id": "1"},
        {"name": "Вакансия 2", "id": "2"}
    ]
    saver = setup_test_file(test_data)

    saver.delete_vacancy_by_id("1")
    data = saver.load_from_json()
    assert len(data) == 1
    assert data[0]["id"] == "2"
    print(" test_delete_vacancy_by_id — пройден")


def test_filter_vacancies_by_salary_range():
    """Тест: фильтрация вакансий по зарплате"""
    print("\n=== Тест: filter_vacancies_by_salary_range ===")
    test_data = [
        {"name": "Вакансия 1", "id": "1", "salary_from": 50000, "salary_to": 80000},
        {"name": "Вакансия 2", "id": "2", "salary_from": 100000, "salary_to": 150000},
    ]
    saver = setup_test_file(test_data)

    filtered = saver.filter_vacancies_by_salary_range("70000-120000")
    assert len(filtered) == 2, "Должны подойти обе вакансии"
    print(" test_filter_vacancies_by_salary_range — пройден")


def test_search_vacancies_by_keyword():
    """Тест: поиск по ключевому слову (включая 'area')"""
    print("\n=== Тест: search_vacancies_by_keyword ===")
    test_data = [
        {"name": "Python разработчик", "description": "", "area": "Москва"},
        {"name": "Python", "description": "Ищем разработчика", "area": "Санкт-Петербург"},
        {"name": "Java", "description": "Ищем Java разработчика", "area": "Новосибирск"},
    ]
    saver = setup_test_file(test_data)

    result = saver.search_vacancies_by_keyword("Москва")
    assert len(result) == 1, "Должна быть одна вакансия из Москвы"
    print(" test_search_vacancies_by_keyword — пройден")
