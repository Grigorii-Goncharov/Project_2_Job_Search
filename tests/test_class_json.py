import os
import json
from pathlib import Path
import pytest
import json

# Импортируем ваш класс
from src.class_json import JSONSaver
from src.class_vacancy import Vacancy

# Тест: успешное сохранение данных
def test_save_to_json(tmp_json_file, test_vacancies):
    saver = JSONSaver()
    saver._JSONSaver__filepath = str(tmp_json_file)

    # Сохраняем данные
    saver.save_to_json(test_vacancies)

    with open(tmp_json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 2
    assert data[0]["name"] == "Python разработчик"
    print(" test_save_to_json — пройден")


# Тест: загрузка данных из JSON
def test_load_from_json(tmp_json_file, test_vacancies):
    saver = JSONSaver()
    saver._JSONSaver__filepath = str(tmp_json_file)

    # Сохраняем тестовые данные
    with open(tmp_json_file, "w", encoding="utf-8") as f:
        json.dump(test_vacancies, f, ensure_ascii=False, indent=4)

    result = saver.load_from_json()

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["name"] == "Python разработчик"
    print(" test_load_from_json — пройден")


# Тест: загрузка объектов Vacancy через load_vacancies
def test_load_vacancies(tmp_json_file, test_vacancies):
    # Сохраняем тестовые данные
    with open(tmp_json_file, "w", encoding="utf-8") as f:
        json.dump(test_vacancies, f, ensure_ascii=False, indent=4)

    saver = JSONSaver()
    saver._JSONSaver__filepath = str(tmp_json_file)

    result = saver.load_vacancies()

    assert isinstance(result, list)
    assert all(isinstance(v, Vacancy) for v in result), "Все элементы должны быть объектами Vacancy"
    assert result[0].area == "Москва"
    assert result[0].salary_from == 80000
    print(" test_load_vacancies — пройден")


# Тест: добавление новой вакансии
def test_add_vacancy(tmp_json_file):
    # Создаем пустой файл
    with open(tmp_json_file, "w", encoding="utf-8") as f:
        f.write("[]")

    saver = JSONSaver()
    saver._JSONSaver__filepath = str(tmp_json_file)

    new_vacancy = Vacancy(
        name="Middle Python",
        id="new_123",
        area="Екатеринбург",
        salary={"from": 100000, "to": 150000},
        description="Опыт от 3 лет"
    )

    # Тест: добавление как объекта Vacancy
    saver.add_vacancy(new_vacancy)

    result = saver.load_from_json()
    assert len(result) == 1
    assert result[0]["id"] == "new_123"
    print(" test_add_vacancy (объект Vacancy) — пройден")



# Корректная фильтрация по диапазону зарплат
def test_filter_vacancies_by_salary_range_valid(setup_salary_data):
    saver = JSONSaver()
    saver._JSONSaver__filepath = setup_salary_data

    result = saver.filter_vacancies_by_salary_range("70000-110000")

    assert len(result) == 2, "Ожидается 2 вакансия в диапазоне 70000-110000"
    assert result[0].name == "Python разработчик"
    print(" test_filter_vacancies_by_salary_range_valid — пройден")


# Диапазон по верхней границе (salary_to)
def test_filter_vacancies_by_salary_upper(setup_salary_data):
    saver = JSONSaver()
    saver._JSONSaver__filepath = setup_salary_data

    result = saver.filter_vacancies_by_salary_range("85000-130000")
    assert len(result) == 2
    assert result[0].name == "Python разработчик"
    print(" test_filter_vacancies_by_salary_upper — пройден")


# Диапазон по нижней границе (salary_from)
def test_filter_vacancies_by_salary_lower(setup_salary_data):
    saver = JSONSaver()
    saver._JSONSaver__filepath = setup_salary_data


    result = saver.filter_vacancies_by_salary_range("50000-70000")
    assert len(result) == 1
    assert result[0].name == "Junior Python"
    print(" test_filter_vacancies_by_salary_lower — пройден")


# Вакансии вне диапазона не должны попадать в результат
def test_filter_vacancies_by_salary_out_of_range(setup_salary_data):
    saver = JSONSaver()
    saver._JSONSaver__filepath = setup_salary_data

    result = saver.filter_vacancies_by_salary_range("130000-150000")
    assert len(result) == 0, "Не должно быть вакансий в этом диапазоне"
    print(" test_filter_vacancies_by_salary_out_of_range — пройден")


# Некорректный формат диапазона
def test_filter_vacancies_by_salary_invalid_format():
    saver = JSONSaver()

    with pytest.raises(ValueError, match=r"Диапазон зарплат должен быть в формате 'мин-макс', например '50000-100000'."):
        saver.filter_vacancies_by_salary_range("неправильный_диапазон")
    print(" test_filter_vacancies_by_salary_invalid_format — пройден")


# Пустой файл или отсутствующие данные
def test_filter_vacancies_by_salary_empty_file(tmp_path):
    empty_file = tmp_path / "empty.json"
    with open(empty_file, "w", encoding="utf-8") as f:
        f.write("[]")

    saver = JSONSaver()
    saver._JSONSaver__filepath = str(empty_file)

    result = saver.filter_vacancies_by_salary_range("50000-100000")
    assert isinstance(result, list), "Ожидается список"
    assert len(result) == 0, "Должен быть пустой список"
    print(" test_filter_vacancies_by_salary_empty_file — пройден")


# Файл не найден → должен вернуть пустой список
def test_load_from_json_file_not_found(tmp_path):
    non_existent_file = tmp_path / "non_existent.json"
    saver = JSONSaver()
    saver._JSONSaver__filepath = str(non_existent_file)

    result = saver.load_from_json()

    assert isinstance(result, list), "Ожидается список"
    assert len(result) == 0, "Должен быть пустой список при отсутствии файла"
    print(" test_load_from_json_file_not_found — пройден")


# Файл существует, но JSON повреждён (некорректный формат)
def test_load_from_json_invalid_format(tmp_path):
    invalid_file = tmp_path / "invalid.json"

    # Записываем битый JSON
    with open(invalid_file, "w", encoding="utf-8") as f:
        f.write("Это не JSON")

    saver = JSONSaver()
    saver._JSONSaver__filepath = str(invalid_file)

    result = saver.load_from_json()

    assert isinstance(result, list), "Ожидается список"
    assert len(result) == 0, "Должен быть пустой список при ошибке парсинга"
    print(" test_load_from_json_invalid_format — пройден")

# Search_vacancies_by_keyword
def test_search_vacancies_by_keyword(setup_keyword_data):
    saver = JSONSaver()
    saver._JSONSaver__filepath = setup_keyword_data

    result = saver.search_vacancies_by_keyword("Python")

    assert isinstance(result, list)
    assert len(result) == 2, "Должны найтись 2 вакансии с 'Python'"
    assert any("Python разработчик" in item["name"] for item in result)
    print(" test_search_vacancies_by_keyword — пройден")


# Filter_vacancies_by_keyword
def test_filter_vacancies_by_keyword(setup_keyword_data):
    saver = JSONSaver()
    saver._JSONSaver__filepath = setup_keyword_data

    result = saver.filter_vacancies_by_keyword("Python")
    assert isinstance(result, list)
    assert all(isinstance(v, Vacancy) for v in result), "Все элементы должны быть типа Vacancy"
    assert len(result) == 2
    assert result[0].name == "Python разработчик"
    print(" test_filter_vacancies_by_keyword — пройден")


# Тест: поиск по полю area
def test_search_by_city(setup_keyword_data):
    saver = JSONSaver()
    saver._JSONSaver__filepath = setup_keyword_data

    result = saver.search_vacancies_by_keyword("Москва")
    assert len(result) == 1, "Ожидается одна вакансия из Москвы"
    assert result[0]["area"] == "Москва"
    print(" test_search_by_city — пройден")


# Тест: ничего не найдено
def test_no_results(setup_keyword_data):
    saver = JSONSaver()
    saver._JSONSaver__filepath = setup_keyword_data


    result = saver.search_vacancies_by_keyword("Golang")
    assert len(result) == 0, "Не должно быть результатов по Golang"
    print(" test_no_results — пройден")


# Тест: некорректные данные в файле
def test_invalid_json_format(tmp_path):
    invalid_file = tmp_path / "invalid.json"
    with open(invalid_file, "w", encoding="utf-8") as f:
        f.write("Это не JSON")

    saver = JSONSaver()
    saver._JSONSaver__filepath = str(invalid_file)

    result = saver.search_vacancies_by_keyword("Python")
    assert isinstance(result, list)
    assert len(result) == 0, "Ошибка при чтении файла → возвращается пустой список"
    print(" test_invalid_json_format — пройден")
