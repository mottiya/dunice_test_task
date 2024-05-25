# Dunice Test Task
Приложение опросы.

Реализованы следующие эндпоинты:
1. Получить все опросы, которые проходил пользователь с заданным id
2. Получить наиболее часто проходимые опросы. Использовать query параметр
count для лимитирования полученных записей. Значение по умолчанию - 5
3. Получить все ответы пользователя с заданным id по опросу с заданным id
4. Создать опрос (с вопросами и ответами к вопросам). Использовать транзакцию
для единоразового создания всех связанных сущностей.

Соблюдены нефукциональные требования:

● Код должен соответствовать конвенции PEP8. Допускается длина строки в 120
символов.

● Необходимо использовать Django + Django REST Framework.

● База данных - postgres.

● Бизнес-логика должны быть реализована в отдельных сервисах.

● Все запросы к БД должны быть выполнены посредством Django ORM.

● Все секреты, а также конфиги должны быть вынесены в переменные окружения.

● Приложение должно содержать скрипт заполнения базы данных. Реализовать с
помощью механизма Django commands.

● Приложение должно быть обернуто в Docker. Рекомендуется использовать
docker-compose. Достаточно реализовать запуск приложения только в
dev-режиме.

● Необходимо подключить swagger по роуту /docs.

## Installation
Установить Docker https://docs.docker.com/engine/install/

Установить Git https://git-scm.com/downloads

Клонировать репозиторий и перейти в рабочую директорию
```bash
git clone https://github.com/teekzaur/dunice_test_task
cd dunice_test_task
```
Переименовать .env.example в .env

Собрать и запустить контейнеры с приложением и базой данных (загружаются тестовые данные)
```bash
docker compose build
docker compose up
```


