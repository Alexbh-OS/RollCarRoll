# 1. Берем официальный образ Python (твоя версия 3.10)
FROM python:3.10-slim

# 2. Устанавливаем переменные окружения (чтобы логи выводились сразу, а не копились)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Создаем рабочую директорию внутри контейнера
WORKDIR /app

# 4. Сначала копируем только requirements.txt и устанавливаем зависимости
# (это кэшируется, чтобы при изменении кода не переустанавливать библиотеки заново)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Копируем весь остальной код проекта в контейнер
COPY . .

# 6. Открываем порт 8000
EXPOSE 8000

# 7. Команда для запуска сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]