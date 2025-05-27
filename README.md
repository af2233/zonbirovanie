# Определение нефтяных загрязнений на поверхности морей по данным снимков ДЗЗ

### IT-проект по программе "Методы искусственного интеллекта в задачах обработки результатов дистанционного зондирования Земли"

## Ссылки:

### Архитектура проекта:

> [Miro](https://miro.com/app/board/uXjVL3nBOTY=/)

### Цели и задачи:

> [Kaiten](https://crazycat.kaiten.ru/space/504576) (закрытый доступ)

### Исследовательский документ:

> [Google Docs](https://docs.google.com/document/d/15Ir2Jy6CUUlSSOhgtOxafPfndpLTomrx/edit?usp=sharing&ouid=105804023758653627289&rtpof=true&sd=true)

### Паспорт проекта:

> [Google Docs](https://docs.google.com/document/d/1SV79vvJkNpgTme1g-ek9hIL226nv9I9Ph7Nac1cJZiE/edit?tab=t.0)

### Документация системы:

> [Google Docs](https://docs.google.com/document/d/1kaDwcIGbTPgFN-i_oswDtNHIyiXyrbueS-RU578EWPE/edit?tab=t.0)


## Запуск проекта:
Создайте файл переменных окружения .env в директории backend:
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
| POSTGRES_DB | untitled |

Чтобы развернуть проект локально, следуйте инструкциям в каждой из трёх директорий сервисов. Для запуска понадобятся: python, npm, postgres.
