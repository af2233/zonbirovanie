### Запуск сервера frontend
Из корня проекта перейдите в папку frontend, затем в папку приложения:
```
cd frontend && cd react_app
```
Выполните установку зависимостей:
```
npm install
```
Запустите сервер:
```
npm start
```
### Запуск с помощью Docker
Из корня проекта перейдите в папку frontend:
```
cd frontend
```
Создайте образ:
```
docker build . -t react_app
```
Запустите контейнер:
```
docker run -p 3000:3000 --name frontend -d react_app
```
