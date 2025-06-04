from src.class_api import HeadHunterAPI
from src.class_vacancy import Vacancy
from src.class_json import JSONSaver


def user_interaction():
    """Функция для взаимодействия с пользователем."""
    print("Добро пожаловать в приложение по поиску вакансий!\n")

    search_query = input("Введите поисковый запрос, например, Python-разработчик: ")
    top_n = int(input("Введите количество вакансий для загрузки: "))
    filter_words = input(
        "Введите ключевые слова для фильтрации через пробел (например, 'Москва инженер') или оставьте пустым: ").split()
    salary_range_input = input("Введите диапазон зарплат (например, 50000-150000) или оставьте пустым: ")

    # Шаг 1: Получаем вакансии с HH
    hh_api = HeadHunterAPI()
    raw_vacancies = hh_api.get_vacancies(search_query, per_page=top_n)

    # Шаг 2: Преобразуем в объекты Vacancy
    vacancies_list = Vacancy.cast_to_object_list(raw_vacancies)
    print(f"Загружено {len(vacancies_list)} вакансий.")

    # Шаг 3: Сохраняем в файл
    saver = JSONSaver()
    saver.save_to_json(vacancies_list)

    # Шаг 4: Фильтрация по ключевым словам
    if filter_words:
        keyword_query = " ".join(filter_words)
        print(f"\n Фильтрация по ключевым словам: '{keyword_query}'")
        filtered_by_keyword = saver.filter_vacancies_by_keyword(keyword_query)
        for v in filtered_by_keyword:
            print(v)

    # Шаг 5: Фильтрация по зарплате
    if salary_range_input:
        print(f"\n Фильтрация по зарплате в заданном диапазоне: {salary_range_input}\n")
        try:
            filtered_by_salary = saver.filter_vacancies_by_salary_range(salary_range_input)
            for v in filtered_by_salary:
                print(v)
        except ValueError as e:
            print(e)

    # Шаг 6: Вывод всех вакансий из файла
    print("\n Вывод вакансий вакансии после обработки: \n")
    all_vacancies = saver.load_vacancies()
    for v in all_vacancies:
        print(v)

    # Шаг 7: Сортировка по зарплате
    while True:
        sort_choice = input("\nХотите отсортировать вакансии по зарплате? (да/нет): ").lower()
        if sort_choice == 'нет':
            break
        elif sort_choice == 'да':
            while True:
                reverse_choice = input("Сортировать по возрастанию (в) или убыванию (у)? ").lower()
                if reverse_choice == 'в':
                    reverse = False
                    break
                elif reverse_choice == 'у':
                    reverse = True
                    break
                else:
                    print("Введите пожалуйста только 'в' (возрастание) или 'y' (убывание)!")

            sorted_vacancies = Vacancy.sort_vacancies_by_salary(all_vacancies, reverse=reverse)
            print("\n Отсортированные вакансии: \n")
            for v in sorted_vacancies:
                print(v)
            break
        else:
            print("Введите пожалуйста только 'да' или 'нет'!")


if __name__ == "__main__":
    user_interaction()

