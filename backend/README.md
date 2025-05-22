### Запуск сервера backend
Из корня проекта перейдите в папку backend:
```
cd backend
```
Создайте файл переменных окружения .env:
| Переменная | Пример значения |
| ------------- | ------------- |
| SECRET_KEY | secret |
| DEBUG | 1 |
| ALLOWED_HOSTS | * |
| POSTGRES_ENGINE | django.db.backends.postgresql |
| POSTGRES_NAME | untitled |
| POSTGRES_USER | postgres |
| POSTGRES_PASSWORD | 1234 |
| POSTGRES_HOST | localhost |
| POSTGRES_PORT | 5432 |

Установите виртуальную среду python - venv:
```
python -m venv .venv
```
Активируйте виртуальную среду (Windows):
```
source .venv/Scripts/activate
```
Выполните установку зависимостей:
```
pip install -r requirements.txt
```
Перейдите в папку приложения:
```
cd django_app
```
Выполните миграции:
```
python manage.py migrate
```
Запустите сервер:
```
python manage.py runserver ИЛИ gunicorn --bind 0.0.0.0:8000 django_app.wsgi
```
### Запуск с помощью Docker
Из корня проекта перейдите в папку backend:
```
cd backend
```
Создайте образ:
```
docker build . -t django_app
```
Запустите контейнер:
```
docker run -p 8000:8000 --name backend -d django_app
```
