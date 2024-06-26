[![Pipeline Status](https://gitlab.crja72.ru/django/2024/spring/course/projects/team-6/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django/2024/spring/course/projects/team-6/pipelines)


# Запуск приложения 🚀
Чтобы запустить приложение локально, выполните следующие шаги:

Откройте терминал.

1. Перейдите в каталог "projects": `cd ~/projects` (чтобы выбрать эту папку, создайте ее в своем каталоге или укажите любую из ранее созданных)
2. Клонируйте репозиторий: `git clone {repository_url}`
3. Перейдите в каталог проекта: `cd virtual_cemetery`
4. Создайте и активируйте виртуальное окружение:

   `Linux/macOS: python3 -m venv venv && source venv/bin/activate`

   `Windows: python -m venv venv && venv\Scripts\activate`
5. Установите основные зависимости для продакшена: 

   `pip3 install -r requirements/production.txt`
6. Настройте базу данных: `python3 manage.py migrate` `Важно:` перед этим посмотрите пункт про базу данных ниже
7. Создайте суперпользователя: `python3 manage.py createsuperuser`
8. Создайте файл .env в корне вашего проекта и определите ваши переменные окружения (см. ниже пример переменных)
9. Запустите сервер разработки:` python3 manage.py runserver`
10. Перейдите к приложению по адресу `http://127.0.0.1:8000/` в вашем браузере.

## Важное примечание
Обратите внимание, что все следующие шаги ниже выполняются строго в базовом каталоге проекта, в котором вы ранее скомпилировали репозиторий в параграфе выше

## База данных
Для того, чтобы проект корректно работал, вам необходимо создать базу данных `PostgreSQL`. Для этого можно использовать различные удобные инструменты (PGAdmin и прочие)
После чего необходимо записать данные созданной базы данных в созданный `.env` файл по примеру из `.env.example`

Откройте ваш терминал.

Выполните миграции базы данных:
```
python3 manage.py migrate
```


## Статические файлы

Для корректной работы и отображения статических файлов в режиме продакшн необходимо выполнить несколько процедур перед запуском проекта

Сгенерируйте статические файлы

```
python3 manage.py collectstatic
```

`Примечание:` обратите внимание, что папка, в которой будут собраны статические файлы, указывается в настройках проекта константы "STATIC_ROOT"

## Переменные окружения

Проект использует файл `.env` для хранения конфиденциальных или переменных окружения, необходимых для запуска приложения. Ниже приведен формат файла `.env.`
Для начала работы с проектом вам нужно скопировать файл `.env.example` и настроить его соответственно.

1. Скопируйте `.env.example` файл:
   
   Linux:
   ```bash
   cp .env.example .env
   ```
   Windows:
   ```cmd
   copy .env.example .env
   ```

2. Откройте файл `.env` и установите там свои значения

## Фикстуры

Чтобы использовать фикстуры в вашем проекте Django, выполните следующие шаги:

1. Создайте файлы фикстур, содержащие сериализованные данные для ваших моделей. Вы можете сгенерировать файлы фикстур с помощью команды управления `dumpdata`:

   Windows:
   ```
   python -Xutf8 manage.py dumpdata animals feedback event homepage faq --indent 2 -o fixtures/data.json
   ```
   Linux:
   ```
   python3 manage.py dumpdata dumpdata animals feedback event homepage faq --indent 2 -o fixtures/data.json 
   ```
   
2. Загрузите данные фикстуры в вашу базу данных, используя команду управления `loaddata`:

   Windows:
   ```
   python manage.py loaddata fixtures/data.json 
   ```
   Linux:
   ```
   python3 manage.py loaddata fixtures/data.json 
   ```

`Примечание:` если желаете, вы также можете указать `fixtures/data` вместо `name.json` вашей папки. Но она должна находиться по пути: `BASE_DIR / dir_name`

## ER Диаграмма
Вот визуальная ER-диаграмма базы данных существующего проекта

![ER Diagram](ER.png)