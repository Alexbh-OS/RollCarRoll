from django.db import connection

with connection.cursor() as cursor:
    """
    cursor.execute("DELETE FROM storage_car;")
    cursor.execute("DELETE FROM storage_dealer;")
    # Добавление данных
    sql = "
        INSERT INTO storage_dealer (title, city, address, area, rating) 
        VALUES (%s, %s, %s, %s, %s)
    "
    seq_of_params = [
        ("Альфа Авто", "Москва", "ул. Ленина, 1", "Центр", 4.7),
        ("Бета Моторс", "Санкт-Петербург", "ул. Мира, 12", "Север", 4.2),
        ("Гамма Трейд", "Новосибирск", "ул. Новая, 5", "Юг", 4.9),
    ]

    cursor.executemany(sql, seq_of_params)

    print("Данные диллеров успешно добавлены!")

    sql = "
            INSERT INTO storage_car (firm,model,year,power,color,price,dealer_id) 
            VALUES (%s, %s, %s, %s, %s,%s, %s)
        "
    seq_of_params = [
        ("Toyota", "Yaris", 2016, 200, "Red", 45 ,2),
        ("Nissan", "Qashqae", 2005 ,198, "Blue", 67 , 2),
        ("Lada", "Vesta", 1999, 100, "Yellow", 78 ,2),
    ]

    cursor.executemany(sql, seq_of_params)

    print("Данные машин успешно добавлены!")

"""
    cursor.execute("""SELECT *
                   FROM storage_dealer""")
    rows = cursor.fetchall()

    for row in rows:
        print(f"ID: {row[0]}, Дилер: {row[1]}")


    cursor.execute("""
                    SELECT *
                   FROM storage_car
                   WHERE year > 2000""")
    rows = cursor.fetchall()

    for row in rows:
        print(f"Модель: {row[0]}, Фирма: {row[1]} ,Год: {row[2]}")
