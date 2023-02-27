## REST API YamDB - база отзывов о фильмах, музыке и книгах
[![API YaMDb Project CI/CD](https://github.com/ZloyShadow/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/ZloyShadow/yamdb_final/actions/workflows/yamdb_workflow.yml)
### Стек

- Python 3.7.0
- Django 2.2.16
- DRF 3.12.4
- Nginx
- Docker (на сервере)
- docker-compose

### Описание

Это практическое задание, выполненное в ходе развёртывания CI/CD YamDb, с отправкой сообщения в Telegram.
Дополнительно добавлен статус воркфлоу в Readme.MD.

### Результат

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку. В каждой категории есть произведения: книги, фильмы или музыка. Произведению может быть присвоен жанр (Genre) из списка предустановленных. Новые жанры может создавать только администратор. Пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти; из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. На одно произведение пользователь может оставить только один отзыв.

### Ресурсы API YaMDb

- Ресурс ***auth***: аутентификация.
- Ресурс ***users***: пользователи.
- Ресурс ***titles***: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
- Ресурс ***categories***: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
- Ресурс ***genres***: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- Ресурс ***reviews***: отзывы на произведения. Отзыв привязан к определённому произведению.
- Ресурс ***comments***: комментарии к отзывам. Комментарий привязан к определённому отзыву.

Каждый ресурс описан в документации: указаны эндпоинты (адреса, по которым можно сделать запрос), разрешённые типы запросов, права доступа и дополнительные параметры, если это необходимо.
***Путь к документации (redoc) в блоке описания запуска проекта***.

### Самостоятельная регистрация пользователя

1. Пользователь отправляет POST-запрос с параметрами "email" и "username" на эндпоинт:
```
/api/v1/auth/signup/
```
2. Сервис YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на указанный адрес email.
3. Пользователь отправляет POST-запрос с параметрами "username" и "confirmation_code" на эндпоинт:
```
/api/v1/auth/token/
```
4. В ответе на запрос ему приходит token (JWT-токен).

В результате пользователь получает токен и может работать с API проекта, отправляя этот токен с каждым запросом. После регистрации и получения токена пользователь может отправить PATCH-запрос на эндпоинт:
```
/api/v1/users/me/
```
и заполнить поля в своём профайле (описание полей — в документации).

### Создание пользователя администратором

Пользователя может создать администратор — через админ-зону сайта или через POST-запрос на специальный эндпоинт:
```
/api/v1/users/
```
Описание полей запроса для этого случая — в документации. После этого пользователь должен самостоятельно отправить свой email и username на эндпоинт (письмо с кодом подтверждения пользователю не отправляется):
```
/api/v1/auth/signup/
```
В ответ должно прийти письмо с кодом подтверждения.
Далее пользователь отправляет POST-запрос с параметрами "username" и "confirmation_code" на эндпоинт:
```
/api/v1/auth/token/
```
В ответе на запрос приходит token (JWT-токен), как и при самостоятельной регистрации.

### Как запустить проект:

* Для подключения GitHub Actions в ```api_yamdb```, необходимо создать директорию 
```.github/workflows``` и скопировать в неё файл ```yamdb_workflow.yml``` из
директории проекта.

* Для прохождения тестов, в директории ```infra```, создать файл ```.env``` с
переменными окружения:
```
# settings.py
SECRET_KEY='<secret_key>'      # стандартный ключ, который создается при старте проекта
DEBUG=False                    # опция отладчика True/False
ALLOWED_HOSTS                  # список хостов/доменов, для которых дотсупен текущий проект

ENGINE=django.db.backends.postgresql
DB_NAME                        # имя БД - postgres (по умолчанию)
POSTGRES_USER                  # логин для подключения к БД - postgres (по умолчанию)
POSTGRES_PASSWORD              # пароль для подключения к БД (установите свой)
DB_HOST=db                     # название сервиса (контейнера)
DB_PORT=5432                   # порт для подключения к БД

# default.conf.template
LOCALHOST                      # имя хоста/домена
PORT                           # порт для подключения
UPSTREAM                       # название сервиса (контейнера) в формате: <название сервиса>:<порт>
```

* В директории проекта ```api_yamdb```, запустить ```pytest```:
```
SECRET_KEY='<secret_key>' pytest
```

## Workflow

Для использования Continuous Integration (CI) и Continuous Deployment (CD): в
репозитории GitHub Actions ```Settings/Secrets/Actions``` прописать Secrets -
переменные окружения для доступа к сервисам:

```
SECRET_KEY                     # стандартный ключ, который создается при старте проекта
DEBUG=False                    # опция отладчика True/False
ALLOWED_HOSTS                  # список хостов/доменов, для которых дотсупен текущий проект

ENGINE=django.db.backends.postgresql
DB_NAME                        # имя БД - postgres (по умолчанию)
POSTGRES_USER                  # логин для подключения к БД - postgres (по умолчанию)
POSTGRES_PASSWORD              # пароль для подключения к БД (установите свой)
DB_HOST=db                     # название сервиса (контейнера)
DB_PORT=5432                   # порт для подключения к БД

LOCALHOST                      # имя хоста/домена
PORT                           # порт для подключения
UPSTREAM                       # название сервиса (контейнера) в формате: <название сервиса>:<порт>

DOCKER_USERNAME                # имя пользователя в DockerHub
DOCKER_PASSWORD                # пароль пользователя в DockerHub
HOST                           # ip_address сервера
USER                           # имя пользователя
SSH_KEY                        # приватный ssh-ключ (cat ~/.ssh/id_rsa)
PASSPHRASE                     # кодовая фраза (пароль) для ssh-ключа

TELEGRAM_TO                    # id телеграм-аккаунта (можно узнать у @userinfobot, команда /start)
TELEGRAM_TOKEN                 # токен бота (получить токен можно у @BotFather, /token, имя бота)
```

При push в ветку main автоматически отрабатывают сценарии:
* *tests* - проверка кода на соответствие стандарту PEP8 и запуск pytest.
Дальнейшие шаги выполняются только если push был в ветку main;
* *build_and_push_to_docker_hub* - сборка и доставка докер-образов на DockerHub
* *deploy* - автоматический деплой проекта на боевой сервер. Выполняется
копирование файлов из DockerHub на сервер;
* *send_message* - отправка уведомления в Telegram.

## Подготовка удалённого сервера
* Войти на удалённый сервер, для этого необходимо знать адрес сервера, имя
пользователя и пароль. Адрес сервера указывается по IP-адресу или по доменному
имени:
```
ssh <username>@<ip_address>
```

* Остановить службу ```nginx```:
```
sudo systemctl stop nginx
```

* Установить Docker и Docker-compose:
```
sudo apt update
sudo apt upgrade -y
sudo apt install docker.io
sudo apt install docker-compose -y
```

* Проверить корректность установки Docker-compose:
```
sudo docker-compose --version
```
* На сервере создать директорию ```nginx/templates/``` :
```
mkdir -p nginx/templates/
```

* Скопировать файлы ```docker-compose.yaml``` и
```nginx/templates/default.conf.template``` из проекта (локально) на сервер в
```home/<username>/docker-compose.yaml``` и
```home/<username>/nginx/templates/default.conf.template``` соответственно:
  * перейти в директорию с файлом ```docker-compose.yaml``` и выполните:
  ```
  scp docker-compose.yaml <username>@<ip_address>:/home/<username>/docker-compose.yaml
  ```
  * перейти в директорию с файлом ```default.conf.template``` и выполните:
  ```
  scp default.conf.template <username>@<ip_address>:/home/<username>/nginx/templates/default.conf.template
  ```

## После успешного деплоя
* Создать суперпользователя:
```
docker-compose exec web python manage.py createsuperuser
```

* Для проверки работоспособности приложения, перейти на страницу:
```
http:/<ip_address>/admin/
```

## Документация для YaMDb доступна по адресу:
```
http:/<ip_address>/redoc/
```