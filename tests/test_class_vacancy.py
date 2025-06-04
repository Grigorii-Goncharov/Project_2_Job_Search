from src.class_vacancy import Vacancy


def test_cast_to_object_list():
    """Тест: преобразование списка вакансий в объекты Vacancy"""
    mock_data = [
        {
            "name": "Python разработчик",
            "id": "123456",
            "area": {"name": "Москва"},
            "description": "Разработка на Python",
            "salary": {"from": 80000, "to": 120000, "currency": "RUR"}
        },
        {
            "name": "Junior Python",
            "id": "789012",
            "area": {"name": "Новосибирск"},
            "description": "Стажировка",
            "salary": {"from": 40000, "to": 60000, "currency": "RUR"}
        }
    ]

    vacancies = Vacancy.cast_to_object_list(mock_data)
    assert isinstance(vacancies, list), "Ожидается список объектов"
    assert len(vacancies) == 2, "Должно быть 2 вакансии"
    assert vacancies[0].name == "Python разработчик"
    assert vacancies[0].area == "Москва", "Город должен быть строкой"
    print(" test_cast_to_object_list — пройден")


def test_to_dict():
    """Тест: корректное преобразование в словарь"""
    vacancy = Vacancy(
        name="Тестировщик",
        id="test123",
        area="Санкт-Петербург",
        salary={"from": 50000, "to": 80000},
        description="Писать тесты"
    )

    data = vacancy.to_dict()
    assert isinstance(data, dict), "Ожидается тип dict"
    assert data["name"] == "Тестировщик"
    assert data["area"] == "Санкт-Петербург"
    print(" test_to_dict — пройден")


def test_salary_validation():
    """Тест: валидация зарплаты"""
    vacancy = Vacancy(
        name="Без зарплаты",
        id="no_salary_1",
        area="Неизвестный город",
        salary={},  # пустой словарь
        description=""
    )

    assert vacancy.salary_from == 0
    assert vacancy.salary_to == 0

    vacancy_with_salary = Vacancy(
        name="С зарплатой",
        id="has_salary",
        area="Москва",
        salary={"from": "сто тысяч", "to": "150000"},  # строка и число
        description=""
    )
    assert vacancy_with_salary.salary_from == 0  # некорректное значение должно стать 0
    assert vacancy_with_salary.salary_to == 150000
    print(" test_salary_validation — пройден")
