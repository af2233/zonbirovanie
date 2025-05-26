### Запуск сервера ML
Из корня проекта перейдите в папку ML:
```
cd ML
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
Перейдите в папку приложения:
```
cd app
```
Запустите сервер:
```
uvicorn main:app --host 0.0.0.0 --port 4000
```
