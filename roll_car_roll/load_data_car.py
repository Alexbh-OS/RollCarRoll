
import os
import json
import pathlib

import django

# Настраиваем окружение Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roll_car_roll.settings')
django.setup()

from storage.models import Car, Dealer


def load_data():
    BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

    file_path_cars = os.path.join(BASE_DIR,'res', 'jsonForDb', 'cars.json')
    file_path_dilers = os.path.join(BASE_DIR,'res', 'jsonForDb', 'dilers.json')

    # 1. ЗАГРУЗКА ДИЛЕРОВ
    print("--- Загрузка дилеров ---")
    with open(file_path_dilers, 'r', encoding='utf-8') as file:
        # В твоем файле это просто список, без ключа "dilers"
        dilers_list = json.load(file)

    created_dealers = []
    for item in dilers_list:
        # Обрати внимание: берем ключи с большой буквы, как в JSON,
        # и записываем в поля модели с маленькой буквы.
        dealer = Dealer.objects.create(
            title=item.get('Name', 'Без названия'),
            city=item.get('City', ''),
            address=item.get('Address', ''),
            area=item.get('Area', ''),
            rating=item.get('Rating', 0.0)
        )
        created_dealers.append(dealer)

    print(f"Успешно добавлено дилеров: {len(created_dealers)}")

    # 2. ЗАГРУЗКА МАШИН
    print("\n--- Загрузка машин ---")
    with open(file_path_cars, 'r', encoding='utf-8') as file:
        data_cars = json.load(file)

    cars_list = data_cars.get('cars', [])

    # Если дилеров нет, создаем одного, чтобы скрипт не упал
    if not created_dealers:
        created_dealers.append(Dealer.objects.create(title="Тестовый Дилер", city="Москва", address="Улица 1"))

    for index, item in enumerate(cars_list):
        # Распределяем машины по дилерам по кругу (0, 1, 2, 0, 1, 2...)
        dealer = created_dealers[index % len(created_dealers)]

        car = Car.objects.create(
            firm=item.get('firm'),
            model=item.get('model'),
            year=item.get('year'),
            power=item.get('power'),
            color=item.get('color'),
            price=item.get('price'),
            dealer=dealer
        )
        # Печатаем каждую 10-ю машину, чтобы не засорять консоль
        if (index + 1) % 10 == 0 or index == len(cars_list) - 1:
            print(f"Загружено машин: {index + 1} из {len(cars_list)}")


if __name__ == '__main__':
    load_data()
    print("\nГотово! Все данные в базе.")