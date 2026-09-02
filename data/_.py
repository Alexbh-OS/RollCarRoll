import sqlite3
import json
import pathlib

p = pathlib.Path(__file__)
print(p)

flagWork = True
connectWithDb = sqlite3.connect('rollCarRoll.db')

cursorDb = connectWithDb.cursor()

while (flagWork):
    nameFileJson = input()

    BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
    print(f"Base dir path: {BASE_DIR}")

    file_path = BASE_DIR / "res" / "jsonForDb" / nameFileJson
    print(f"File path {file_path}")

    with open(file_path, 'r', encoding='UTF-8') as f:
        data = json.load(f)

    print(data)
    nameTable = input("Введите имя таблицы для создания/записи: ")

    cursorDb.execute(f'''
    CREATE TABLE IF NOT EXISTS {nameTable} (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER
    )
    ''')

    if isinstance(data, dict):
        # Если в файле один объект, превращаем его в список из одного элемента
        data = [data]

    if isinstance(data, list):
        for item in data:
            cursorDb.execute(
                f"""  INSERT INTO {nameTable} (username, email, age)
                            VALUES (?, ?, ?)  """,
                (
                    item.get("username"),
                    item.get("email"),
                    item.get("age"),
                ),
            )

        connectWithDb.commit()
        print(
            f"Успешно загружено записей: {len(data)} в таблицу '{nameTable}'!"
        )
    else:
        print("Ошибка: Неподдерживаемый формат JSON (должен быть список или объект)")


connectWithDb.close()

