FROM python:3.12-slim

# Устанавливаем зависимости
WORKDIR /app
COPY pyproject.toml poetry.lock ./

# Обновляем pip и устанавливаем poetry
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

# Копируем остальные файлы приложения
COPY . .

# Устанавливаем переменную окружения для Django
ENV PYTHONUNBUFFERED=1

# запускаем команду в Unix, которая принимает тест "-с" и передаем команду на запуск сервера. Без миграций
# CMD ["sh", "-c", "python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
