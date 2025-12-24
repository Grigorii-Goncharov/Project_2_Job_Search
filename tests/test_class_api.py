import pytest
import requests
from unittest.mock import Mock, patch


# Тест: успешный response_check (API доступно)
@patch("requests.get")
def test_response_check_success(mock_get, hh_api):
    """Тест: API доступно"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    result = hh_api._HeadHunterAPI__response_check()
    assert result is True
    print("✅ test_response_check_success — пройден")


# Тест: недоступное API
@patch("requests.get", raise_effect=Exception("Connection error"))
def test_response_check_failure(mock_get, hh_api):
    """Тест: API недоступно"""
    result = hh_api._HeadHunterAPI__response_check()
    assert result is True
    print("✅ test_response_check_failure — пройден")


# Тест: получение вакансий при успешном запросе
@patch("requests.get")
def test_get_vacancies_success(mock_get, hh_api):
    """Тест: успешное получение вакансий"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "items": [
            {"name": "Python разработчик", "id": "123456"},
            {"name": "Junior Python", "id": "789012"}
        ]
    }
    mock_get.return_value = mock_response

    result = hh_api.get_vacancies("Python", per_page=2)

    assert isinstance(result, list), "Ожидается список словарей"
    assert len(result) == 2, "Должно быть 2 вакансии"
    assert result[0]["name"] == "Python разработчик"
    print("✅ test_get_vacancies_success — пройден")


# Тест: ошибка сети — ConnectionError
@patch("requests.get", side_effect=requests.exceptions.RequestException("Network error"))
def test_get_vacancies_network_error(mock_get, hh_api):
    """Тест: сетевая ошибка при выполнении запроса"""
    with pytest.raises(ConnectionError, match="API недоступно. Невозможно получить вакансии."):
        hh_api.get_vacancies("Python", per_page=2)
    print("✅ test_get_vacancies_network_error — пройден")


# Тест: пустой ответ от API
@patch("requests.get")
def test_get_vacancies_empty_result(mock_get, hh_api):
    """Тест: API возвращает пустой список вакансий"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"items": []}
    mock_get.return_value = mock_response

    result = hh_api.get_vacancies("Несуществующая вакансия", per_page=10)
    assert isinstance(result, list)
    assert len(result) == 0, "Ожидается пустой список"
    print("✅ test_get_vacancies_empty_result — пройден")


# Тест: API возвращает 404 или другой код ошибки
@patch("requests.get")
def test_get_vacancies_bad_status(mock_get, hh_api):
    """Тест: API возвращает ошибку (например, 404)"""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
    mock_get.return_value = mock_response

    with pytest.raises(ConnectionError, match="API недоступно. Невозможно получить вакансии"):
        hh_api.get_vacancies("Python", per_page=2)
    print("✅ test_get_vacancies_bad_status — пройден")
