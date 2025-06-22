### Запуск сервера backend
Из корня проекта перейдите в папку backend:
```
cd backend
```
Установите виртуальную среду python - venv:
```
python -m venv .venv
```
Активируйте виртуальную среду:
```
.venv\Scripts\activate
```
Обновите pip:
```
python -m pip install --upgrade pip
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
python manage.py runserver
```
