import json
import os
from typing import List, Dict, Any, Optional
from src.class_abstract import BaseFileStorage
from src.class_api import HeadHunterAPI
from src.class_vacancy import Vacancy


class JSONSaver(BaseFileStorage):
    def __init__(self, file_name: str = "vacancies.json"):
        # Получаем путь относительно текущего файла
        self.__file_path = os.path.join(os.path.dirname(__file__), "..", "data", file_name)
        print(f"[INFO] Файл будет сохранён по пути: {self.__file_path}")
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Создает файл, если он не существует"""
        os.makedirs(os.path.dirname(self.__file_path), exist_ok=True)
        if not os.path.exists(self.__file_path):
            with open(self.__file_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _load_data(self) -> List[Dict]:
        """Загрузка данных из файла"""
        try:
            with open(self.__file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Если элементы — строки, парсим их как JSON
            if isinstance(data, list) and data and isinstance(data[0], str):
                parsed_data = []
                for item in data:
                    try:
                        parsed_data.append(json.loads(item))
                    except json.JSONDecodeError:
                        continue  # Пропускаем поврежденные строки
                return parsed_data

            return data

        except json.JSONDecodeError:
            return []

    def _save_data(self, data: List[Dict]) -> None:
        """Сохранение данных в файл"""
        with open(self.__file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy: Dict[str, Any]) -> None:
        """Добавление уникальной вакансии в файл"""
        data = self._load_data()

        # Проверяем на дубликаты по имени + зарплате
        is_duplicate = False
        for item in data:
            if (
                item.get("name") == vacancy.get("name")
                and item.get("salary_from") == vacancy.get("salary_from")
                and item.get("salary_to") == vacancy.get("salary_to")
            ):
                is_duplicate = True
                break

        if not is_duplicate:
            data.append(vacancy)
            self._save_data(data)
            print(f"[INFO] Вакансия '{vacancy.get('name')}' успешно добавлена.")
        else:
            print(f"[INFO] Вакансия '{vacancy.get('name')}' уже существует.")

    def get_vacancies(self, criteria: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Получение вакансий по критериям"""
        data = self._load_data()
        if not criteria:
            return data

        result = []
        for item in data:
            match = True
            for key, value in criteria.items():
                if item.get(key) != value:
                    match = False
                    break
            if match:
                result.append(item)
        return result

    def delete_vacancy(self, criteria: Dict[str, Any]) -> None:
        """Удаление вакансии по критерию"""
        data = self._load_data()
        new_data = [item for item in data if not all(item.get(k) == v for k, v in criteria.items())]
        self._save_data(new_data)

if __name__ == "__main__":

    api = HeadHunterAPI()
    vacancies_json = api.get_vacancies(text="Python", per_page=5)
    print(f"Найдено вакансий: {len(vacancies_json)}")

    vacancies = Vacancy.cast_to_object_list(vacancies_json)


    for vac in vacancies:
        print(f"Название: {vac.name}")
        print(f"Ссылка: {vac.link}")
        print(f"Зарплата: {vac.salary_from} - {vac.salary_to}")
        print(f"Описание: {vac.description}")
        print("-" * 40)

    # Сохраняем в JSON
    saver = JSONSaver()

    # Добавляем тестовую вакансию
    test_vac = {
        "name": "Шутник",
        "link": "https://example.com/test-vac",
        "salary_from": 7500,
        "salary_to": 10000,
        "description": "Надо носить кофе сеньорам"
    }
    vac_obj = Vacancy.from_dict(test_vac)
    saver.add_vacancy(vac_obj.to_dict())

    # Добавляем вакансии из API
    for vac in vacancies:
        saver.add_vacancy(vac.to_dict())

    # Проверяем содержимое файла
    saved_vacs = saver.get_vacancies()
    print("\n[INFO] Вакансии в файле:")
    for v in saved_vacs:
        print(v)

        # Удаляем тестовую вакансию по ссылке
    print("\n[INFO] Удаляем тестовую вакансию...")
    saver.delete_vacancy({"link": "https://example.com/test-vac"})

    # Проверяем, что вакансия удалена
    saved_vacs_after = saver.get_vacancies()
    print("\n[INFO] Вакансии в файле после удаления:")
    for v in saved_vacs_after:
        print(v)
