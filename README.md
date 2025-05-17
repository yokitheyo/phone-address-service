# Phone-Address Service

RESTful сервис для хранения и получения адресов по номеру телефона

## Описание проекта

Сервис предоставляет API для:
- Сохранения и обновления адресов по номеру телефона
- Получения адреса по номеру телефона


## Требования

- Docker и Docker Compose
- Python 3.11+ (для локальной разработки) 

## Установка и запуск

### С использованием Docker 

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/yokitheyo/phone-address-service.git
   cd phone-address-service
   ```

2. Создайте файл `.env` на основе примера или используйте значения по умолчанию.

3. Запустите сервис с помощью Docker Compose:
   ```bash
   docker-compose up -d
   ```

4. Сервис будет доступен по адресу: http://localhost:8000


## Документация API

После запуска сервиса документация Swagger доступна по адресу:
- http://localhost:8000/docs

Альтернативная документация ReDoc:
- http://localhost:8000/redoc

