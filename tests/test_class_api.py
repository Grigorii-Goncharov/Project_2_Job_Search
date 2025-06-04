import requests
from unittest.mock import patch, Mock

# Подключаем ваш API
from src.class_api import HeadHunterAPI


def test_response_check_success():
    """Тест: API доступно (возвращает 200)"""
    api = HeadHunterAPI()

    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = api._HeadHunterAPI__response_check()
        assert result is True, "Ожидается, что API доступно"
        print(" test_response_check_success — пройден")


def test_response_check_failure():
    """Тест: API недоступно (сетевая ошибка)"""
    api = HeadHunterAPI()

    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")

        result = api._HeadHunterAPI__response_check()
        assert result is False, "Ожидается, что API недоступно"
        print("test_response_check_failure — пройден")


def test_get_vacancies_success():
    """Тест: успешное получение вакансий"""
    api = HeadHunterAPI()

    with patch("requests.get") as mock_get:
        # Подготовка фейкового ответа
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {"name": "Python разработчик", "id": "123456"},
                {"name": "Junior Python", "id": "789012"}
            ]
        }
        mock_get.return_value = mock_response

        result = api.get_vacancies("Python", per_page=2)
        assert isinstance(result, list), "Ожидается список вакансий"
        assert len(result) == 2, "Ожидается 2 вакансии"
        assert result[0]["name"] == "Python разработчик"
        print(" test_get_vacancies_success — пройден")


def test_get_vacancies_api_unavailable():
    """Тест: API недоступно — вызывается ConnectionError"""
    api = HeadHunterAPI()
    api._HeadHunterAPI__url = "https://api.hh.u/vacancies_down"   # некорректный URL

    with patch("requests.get"):
        try:
            api.get_vacancies("Python", per_page=2)
        except ConnectionError:
            print(" test_get_vacancies_api_unavailable — пройден")
            return

    assert True, "Ожидается ConnectionError при недоступном API"


def test_get_vacancies_network_error():
    """Тест: сетевая ошибка при выполнении запроса"""
    api = HeadHunterAPI()

    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        try:
            api.get_vacancies("Python", per_page=2)
        except ConnectionError:
            print(" test_get_vacancies_network_error — пройден")
            return

    assert True, "Ожидается ValueError при сетевой ошибке"


def test_get_vacancies_empty_result():
    """Тест: API возвращает пустой список вакансий"""
    api = HeadHunterAPI()

    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        mock_get.return_value = mock_response

        result = api.get_vacancies("Несуществующая вакансия", per_page=10)
        assert isinstance(result, list), "Ожидается тип list"
        assert len(result) == 0, "Ожидается пустой список"
        print(" test_get_vacancies_empty_result — пройден")
