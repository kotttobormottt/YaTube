Социальная сеть YaTube для публикации постов и картинок (Яндекс.Практикум)
=====

Описание проекта
----------
Данный проект создан в рамках учебного курса Яндекс.Практикум.

Социальная сеть для авторов и подписчиков. Пользователи могут подписываться на избранных авторов, оставлять комментари к постам, оставлять новые посты на главной странице и в тематических группах, прикреплять изображения к публикуемым постам. 

Проект реализован на MVT-архитектуре, реализована система регистрации новых пользователей, восстановление паролей пользователей через почту, система тестирования проекта на unittest, пагинация постов и кэширование страниц.

Системные требования
----------
* Python 3.8+
* Linux, Windows, macOS

Стек технологий
----------
* Python 3.8
* Django 2.2 
* Unittest
* Pytest
* SQLite3
* CSS
* JS
* HTML
* Bootstrap

Установка проекта из репозитория (Windows)
----------
1. Клонируем проект:
```bash
git clone https://github.com/kotttobormottt/hw05_final.git
```

2. Переходим в папку с проектом:
```bash
cd hw05_final/
```

3. Устанавливаем виртуальное окружение:
```bash
python -m venv venv
```

4. Активируем виртуальное окружение:
```bash
source venv/Scripts/activate
```

! Для деактивации виртуального окружения выполним (после работы):
```bash
deactivate
```

5. Устанавливаем зависимости из файла ```requirements.txt```:
```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

6. Применяем миграции:
```bash
python yatube/manage.py makemigrations
```
```bash
python yatube/manage.py migrate
```

7. Запускаем сервер:
```bash
python manage.py runserver
```

> В проекте есть тесты, для запуска в папке с файлом ```manage.py``` выполните команду:
> ```
> py manage.py test
> ```

Установка проекта из репозитория (Linux и macOS)
----------

1. Клонируем проект:
```bash
git clone https://github.com/kotttobormottt/hw05_final.git
```

2. Переходим в папку с проектом:
```bash
cd hw05_final/
```

3. Устанавливаем виртуальное окружение:
```bash
python3 -m venv env
source env/bin/activate
```

4. Устанавливаем зависимости из файла ```requirements.txt```:
```bash
python3 -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

5. Применяем миграции:
```bash
python3 yatube/manage.py makemigrations
```
```bash
python3 yatube/manage.py migrate
```

6. Запускаем сервер:
```bash
python3 manage.py runserver
```

### Авторы:
Андрей Жаров
