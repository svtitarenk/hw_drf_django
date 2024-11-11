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
