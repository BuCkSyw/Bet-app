# Bet app

## Корневая директория содержит следующее

    bet_maker - сервис bet_maker
    line_provider - сервис line_provider
    .env-non-dev - файл переменных окружения
    .flake8
    docker-compose.yaml
    init.sql - sql скрипт для инициализации в docker-compose
    pyproject.toml 

### line_provder и bet_maker имеют следующую структуру

    app - директория приложения
    .env - файл с переменными окружения
    alembic.ini - файл конфигурации для Alembic
    Dockerfile - файл конфигурации Docker для контейнеризации приложения
    pytest.ini -  файл конфигурации для Pytest
    requirements.txt - файл с зависимостями python 

#### папка app

    migrations - каталог миграций созданный Alembic
    tests - каталог с тестами
    config.py - конфигурационный файл приложения
    conftest.py - конфигурационный файл для настройки тестов
    dao.py - файл для работы с БД (Data Access Object)
    database.py - файл подключения БД
    main.py - файл основной точки входа для приложения
    models.py - файл с моделями
    router.py - файл с маршрутами и конечными точками API
    schemas.py - файл со схемами

### line_provder API

#### В приложении line_provider есть следующие API

#### GET events/all
    
    Эндпоинт для получения всех событий из БД
    Если событий нет, в ответе статус 404 с сообщением:
    "Events not found"

#### GET events/ 

    Эндпоинт для получения всех актуальных событий из БД
    Если таких событий нет, в ответе статус 404 с сообщением:
    "Events not found"

#### GET events/{id}

    Эндпоинт для получения информации по заданному событию
    В параметры запроса передается id, если такой id есть в БД
    возвращает информацию по событию, если такого id нет - возвращает
    в ответе статус 404 с сообщением: "Event {id} not found"

#### PUT events/change_event/{id}

    Эндпоинт для изменения существующих событий, в параметрах
    задается id события, которое необходимо поменять, в теле запроса
    задаются остальные поля, которые являются необязательными

    При корректном заполнении изменяет запись в БД и возвращает сообщение со статусом 200:
    "Event {id} has been change"

    При изменении статуса события отправляется запрос в сервис bet_maker на эндпоинт:
    http://bet_maker/bets/callback_change_status:8001

    Ограничения на параметры запроса:

    При попытке изменить событие, id которого нет в БД вернется ошибка со статусом 404
    с сообщением: "Event doesn`t found"

    Ограничения на значения в теле запроса:

    При попытке передать bet_coef отрицательным числом вернется ошибка со статусом 404
    с сообщением "bet_coef must be greater than 0"

    При попытке передать event_status="unfinished" и даты bet_deadline, которая 
    меньше текущей даты (или дата изначально меньше текущей даты в БД)
    вернется ошибка 404 с сообщением
    "event is over, status_event can be only team_1_won or team_2_won"

    При попытке передать event_status="team_1_won" или 
    event_status="team_2_won" и даты bet_deadline, которая больше текущей
    даты (или дата изначально больше текущей даты в БД)
    вернется ошибка 404 с сообщением
    "event is not over, status_event can be only unfinished"

#### POST events/add_new_event

    Эндпоинт для добавления нового события, все параметры запроса
    обязательные
    При успешном выполнении возвращает сообщение со статусом 200: "Event has been added"

    Ограничения на значения в теле запроса:

    При попытке передать bet_coef отрицательным числом вернется ошибка 404
    с сообщением "bet_coef must be greater than 0"

    При попытке передать event_status="unfinished" и даты bet_deadline, которая 
    меньше текущей даты вернется ошибка 404 с сообщением:
    "event is over, status_event can be only team_1_won or team_2_won"

    При попытке передать event_status="team_1_won" или
    event_status="team_2_won" и даты bet_deadline, которая больше текущей даты
    вернется ошибка 404 с сообщением:
    "event is not over, status_event can be only unfinished"

#### DELETE events/delete_event/{id}

    Эндпоинт для удаления события из БД
    В параметре передается id события, которое необходимо удалить
    При успешном выполнении возвращает статус 200 с сообщением:
    "Event with id {id} delete"
    При попытке удалить событие, которого нет в БД возвращает ошибку 404 сообщение:
    "Event not found"

### bet_maker API

#### В приложении bet_maker есть следующие API

#### POST /bets/bet

    Эндпоинт для совершения ставки, в теле запросе необходимо указать
    event_id и amount, при успешном выполнении возвращается 200 с сообщением:
    "bet with an amount {amount} on the event {event_id} is made"

    Ограничения на тело запроса:

    При попытке передать amount отрицательным числом вернется ошибка 422
    с сообщением "Value error, amount must be a strictly positive number"

#### GET /bets

    Эндпоинт для получения всех ставок из БД
    Если ставок нет, вернется ошибка 404 с сообщением:
    "Bets not found"

#### PUT /bets/callback_change_status

    Эндпоинт для изменения статуса ставок при изменении статуса событий
    Вызывается из приложения line_provider при изменении статуса события
    Заменяет статусы по event_id 

#### GET /events

    Эндпоинт для получения всех актуальных событий из приложения line_provider
    Если таких событий нет, вернется ошибка 404 с сообщением:
    "Events not found"

### Для запуска приложения

Необходимо запустить команду docker-compose up --build в директории с docker-compose.yml,
после успешной сборки, сервис line_provider будет доступен по ссылке http://localhost:8000
сервис bet_maker будет доступен по ссылке http://localhost:8001

