import os
import json
from pathlib import Path
import pytest
from typing import Union
from src.class_vacancy import Vacancy

# Вспомогательная функция для создания тестовых JSON-файлов
def setup_test_file(filepath: Union[Path, str], content: dict):
    """Создаёт временный JSON-файл с заданным содержимым."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=4)


# Тест: корректное создание вакансий из словарей
def test_cast_to_object_list(vacancies):
    assert isinstance(vacancies, list), "Ожидается список объектов Vacancy"
    assert len(vacancies) == 2, "Должно быть 2 вакансии"
    assert vacancies[0].name == "Python разработчик"
    assert vacancies[0].area == "Москва"
    assert vacancies[0].salary_from == 80000
    print(" test_cast_to_object_list — пройден")


# Тест: метод to_dict()
def test_to_dict(vacancies):
    vacancy = vacancies[0]
    data = vacancy.to_dict()

    assert isinstance(data, dict), "Ожидается тип dict"
    assert data["name"] == "Python разработчик"
    assert data["area"] == "Москва"
    assert data["salary_from"] == 80000
    print(" test_to_dict — пройден")


# Тест: сравнение вакансий (lt, gt)
def test_compare_salary(vacancies):
    v1, v2 = vacancies

    # Проверка __lt__
    assert v2.salary_from < v1.salary_from, "Junior должен получать меньше"
    with pytest.raises(AttributeError):
        v1 > "Не вакансия"  # должно вызвать ошибку
    print(" test_compare_salary — пройден")


# Тест: сортировка по зарплате
def test_sort_vacancies_by_salary(vacancies):
    sorted_asc = Vacancy.sort_vacancies_by_salary(vacancies, reverse=False)
    salaries_asc = [v.salary_from for v in sorted_asc]
    assert salaries_asc == sorted(salaries_asc), "Сортировка по возрастанию работает некорректно"

    sorted_desc = Vacancy.sort_vacancies_by_salary(vacancies, reverse=True)
    salaries_desc = [v.salary_from for v in sorted_desc]
    assert salaries_desc == sorted(salaries_desc, reverse=True), "Сортировка по убыванию работает некорректно"
    print(" test_sort_vacancies_by_salary — пройден")


# Успешная загрузка вакансий из корректного JSON
def test_load_from_json_success(tmp_path):
    # Создаем временный файл с корректными данными
    test_file = tmp_path / "vacancies.json"

    test_data = [
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

    setup_test_file(test_file, test_data)

    result = Vacancy.load_from_json(str(test_file))

    assert isinstance(result, list), "Ожидается список объектов Vacancy"
    assert len(result) == 2, "Должно быть 2 вакансии"
    assert result[0].name == "Python разработчик"
    assert result[0].area == "Москва"
    assert result[0].salary_from == 80000
    print(" test_load_from_json_success — пройден")


# Файл не найден
def test_load_from_json_file_not_found(tmp_path):
    non_existent_file = tmp_path / "non_existent.json"

    result = Vacancy.load_from_json(str(non_existent_file))

    assert isinstance(result, list), "Ожидается список"
    assert len(result) == 0, "Список должен быть пустым при отсутствии файла"
    print(" test_load_from_json_file_not_found — пройден")


# Некорректный JSON (битый файл)
def test_load_from_json_invalid(tmp_path):
    invalid_file = tmp_path / "invalid.json"
    with open(invalid_file, "w", encoding="utf-8") as f:
        f.write("Это не JSON")

    result = Vacancy.load_from_json(str(invalid_file))
    assert isinstance(result, list), "Ожидается список"
    assert len(result) == 0, "Список должен быть пустым при ошибке JSON"
    print(" test_load_from_json_invalid — пройден")


# Пустой JSON (но валидный)
def test_load_from_json_empty(tmp_path):
    empty_file = tmp_path / "empty.json"
    with open(empty_file, "w", encoding="utf-8") as f:
        f.write("[]")

    result = Vacancy.load_from_json(str(empty_file))
    assert isinstance(result, list), "Ожидается список"
    assert len(result) == 0, "Список должен быть пустым"
    print(" test_load_from_json_empty — пройден")
