import sqlite3
import json
import pathlib

p = pathlib.Path(__file__)
print(p)

flagWork = True
connectWithDb = sqlite3.connect('rollCarRoll.db')

cursorDb = connectWithDb.cursor()

while (flagWork):
    listAttrTable = list()
    listAttrName = list()

    print(f"Введите названия файла json :")
    nameFileJson = input()

    BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
    filePathJson = BASE_DIR / "res" / "jsonForDb" / nameFileJson
    print(f"Путь к файлу {filePathJson}")

    with open(filePathJson , 'r', encoding='UTF-8') as f:
        data = json.load(f)


    print(f"Введите названия файла с параметрами таблицы :")
    nameFileParam = input()
    filePathParam = BASE_DIR / "res" / nameFileParam

    with open(filePathParam, 'r', encoding='UTF-8') as f:
        for line in f:
            listAttrTable.append(line.strip())

    nameTable = input("Введите имя таблицы для создания/записи: ")

    columns_sql = ",\n    ".join(listAttrTable)

    cursorDb.execute(f'''
    CREATE TABLE IF NOT EXISTS {nameTable} (
    id INTEGER PRIMARY KEY,
    {columns_sql}
    )
    ''')

    if isinstance(data, dict):
        for key, list_data in data.items():
            if key == nameTable:
                print(list_data)
                data = list_data

    if isinstance(data, list):
        for item in data:
            cursorDb.execute(
                f"""  INSERT INTO {nameTable} (firm,model,year,power,color,price)
                            VALUES (?, ?, ?, ?, ?, ?)  """,
                (
                    item.get("firm"),
                    item.get("model"),
                    item.get("year"),
                    item.get("power"),
                    item.get("color"),
                    item.get("price"),
                ),
            )

        connectWithDb.commit()
        print(f"Успешно загружено записей: {len(data)} в таблицу '{nameTable}'")
        flagWork = False
    else:
        print("Ошибка: Неподдерживаемый формат JSON (должен быть список или объект)")
        flagWork = False

connectWithDb.close()
