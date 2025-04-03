# Стартовый образ
FROM python:3.11-alpine

# Рабочая директория
WORKDIR /usr/src/app

# Переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONOPTIMIZE=2

# Обновление pip
RUN pip install --no-cache-dir --upgrade pip

# Копирование и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

# Рабочая директория проекта
WORKDIR /usr/src/app/django_app

# Открытие порта
EXPOSE 8000

# Запуск миграций и сервера
RUN python manage.py migrate
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "django_app.wsgi:application"]
