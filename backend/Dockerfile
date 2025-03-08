# Стартовый образ
FROM python:3.11-alpine

# Рабочая директория
WORKDIR /usr/src/app

# Переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# Обновление pip
RUN pip install --upgrade pip

# Скопируем и установим зависимости
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё, что осталось
COPY . .

EXPOSE 8000

WORKDIR /usr/src/app/django_app

# Применяем миграции и запускаем сервер
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
