import json


def json_load(filename):
    """Функция Открытия json файла на чтение"""
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
        return data
