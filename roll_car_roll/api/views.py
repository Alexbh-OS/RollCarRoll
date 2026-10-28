from django.db.models import ProtectedError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .serializers import CarSerializer, DealerSerializer
from storage.models import Car, Dealer


"""Получение всех записей таблице машин, добавление новой записи/ей в таблицу машин 
   !при добавлении нам не нужны параметры в URL-запросе """
@api_view(['GET','POST'])
def get_cars(request):
    if request.method == 'POST': # POST(CREATE) - Запрос на добавления записи/ей в БД
        serializer = CarSerializer(data=request.data, many=True) # Пытаемся из исходного JSON сделать словарь сериализатором
        if serializer.is_valid(): # Если валиден ,добавляем записи в БД
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # Если GET запрос,сначала получаем QuerySet из БД,
    # преобразуем в словарь сериализатором,отдаем ответ JSON всей таблицы сущности
    cars = Car.objects.all()
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)


"""Получение,изменение,замена,удаления конкретной записи в таблице машин"""
@api_view(['GET','PATCH','DELETE','PUT'])
def get_car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)

    if request.method == 'PATCH' or request.method == 'PUT':
        serializer = CarSerializer(car, data=request.data,partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = CarSerializer(car)
    return Response(serializer.data)


"""Получение всех записей таблице дилеров, добавление новой записи/ей  в таблицу дилеров
   !при добавлении нам не нужны параметры в URL-запросе """
@api_view(['GET','POST'])
def get_dealers(request):
    if request.method == 'POST': # POST(CREATE) - Запрос на добавления записи/ей в БД
        serializer = DealerSerializer(data=request.data, many=True) # Пытаемся из исходного JSON сделать словарь сериализатором
        if serializer.is_valid(): # Если валиден ,добавляем записи в БД
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # Если GET запрос,сначала получаем QuerySet из БД,
    # преобразуем в словарь сериализатором,отдаем ответ JSON всей таблицы сущности
    dealers = Dealer.objects.all()
    serializer = DealerSerializer(dealers, many=True)
    return Response(serializer.data)


"""Получение,изменение,замена,удаления конкретной записи в таблице диллеров"""
@api_view(['GET','PATCH','DELETE','PUT'])
def get_dealer_detail(request, pk):
    dealer = get_object_or_404(Dealer, pk=pk)

    # DELETE: удаляем объект
    if request.method == 'DELETE':
        try:
            dealer.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            # Если у дилера есть машины, возвращаем 400 Bad Request (а не 500)
            return Response(
                {"error": "Нельзя удалить дилера, так как у него есть автомобили в базе."},
                status=status.HTTP_400_BAD_REQUEST
            )

    # PUT или PATCH: обновляем объект
    if request.method == 'PUT' or request.method == 'PATCH':
        serializer = DealerSerializer(dealer, data=request.data,partial=(request.method == 'PATCH'))  # True для PATCH, False для PUT)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer = DealerSerializer(dealer)
    return Response(serializer.data)






"""
1. БАЗА ДАННЫХ (SQLite)
   Хранит строки в таблицах (реляционный формат).

2. Car.objects.all() (QuerySet)
   Django забирает строки из БД и превращает их в Python-объекты <Car>.

3. CarSerializer(cars, many=True) (Сериализация)
   DRF берет объекты <Car> и превращает их в обычные Python-словари {"firm": "Toyota"}.
   Готовый результат лежит в serializer.data.

4. Response(serializer.data) (Рендеринг)
   DRF берет Python-словари и "выплевывает" их в виде текста формата JSON:
   [{"id": 1, "firm": "Toyota", ...}, {"id": 2, ...}]

5. БРАУЗЕР
   Получает чистый текст JSON, проверяет заголовок Content-Type и красиво отрисовывает его.
"""
