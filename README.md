# Yatube - социальная сеть для блогеров

## Описание проекта

Yatube - это социальная сеть для публикации личных дневников. Это платформа, где пользователи могут:
- Создавать учетную запись
- Публиковать записи
- Просматривать записи других пользователей
- Подписываться на любимых авторов
- Комментировать записи

Проект реализован на Django и включает REST API для взаимодействия с сервисом.

## Установка

1. Клонируйте репозиторий:
https://github.com/senia753/api_final_yatube.git

2. Создайте и активируйте виртуальное окружение:
python -m venv venv
source venv/bin/activate  # для Linux/MacOS
venv\Scripts\activate  # для Windows


3. Установите зависимости:
pip install -r requirements.txt

4. Примените миграции:
python manage.py migrate

5. Запустите сервер:
python manage.py runserver

## Примеры запросов к API

### Получение списка постов

GET /api/v1/posts/

Пример ответа:
[
    {
        "id": 2,
        "text": "Вечером собрались в редакции «Русской мысли», чтобы поговорить о народном театре. Проект Шехтеля всем нравится.",
        "author": "root",
        "image": null,
        "group": 1,
        "pub_date": "2025-05-16T18:29:41.905245+03:00"
    },
    {
        "id": 3,
        "text": "Утром собрались в редакции «Русской мысли», чтобы поговорить о народном театре. Проект Шехтеля всем нравится.",
        "author": "root",
        "image": null,
        "group": 1,
        "pub_date": "2025-05-16T18:34:14.775571+03:00"
    },
]


### Создание нового поста

POST /api/v1/posts/

Тело запроса:

{
    "text": "Текст нового поста",
    "group": 1
}


### Получение списка комментариев

GET /api/v1/posts/{post_id}/comments/

Пример ответа:

[
    {
        "id": 6,
        "author": "regular_user",
        "post": 13,
        "text": "Тестовый комментарий",
        "created": "2025-05-17T14:48:11.161067+03:00"
    }
]

### Подписка на автора

POST /api/v1/follow/

Тело запроса:

{
    "following": "username"
}


## Технологии
- Python 3.7+
- Django 2.2.16
- Django REST Framework
- Simple JWT
- Pillow
- Sorl-thumbnail

## Авторы
Senia Babenko