### Запуска сервера backend
Из корня проекта перейдите в папку backend:
```
cd backend
```
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
Перейдите в папку проекта:
```
cd django_app
```
Выполните миграции:
```
python manage.py migrate
```
Запустите сервер:
```
python manage.py runserver
```
