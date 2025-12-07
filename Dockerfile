# Dockerfile
FROM python:3.12-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Создаем непривилегированного пользователя с UID 1000
RUN adduser --disabled-password --uid 1000 --gecos "" appuser

# Копируем проект
COPY . .

# Установим пользователя
USER appuser

# Команда для запуска Django
CMD ["gunicorn", "habit_tracker.wsgi:application", "--bind", "0.0.0.0:8000"]
