# API-сервис бронирования столиков в ресторане

##  Цель
Разработать REST API для бронирования столиков в ресторане. Сервис должен позволять создавать, просматривать и удалять брони, а также управлять столиками и временными слотами.

##  Функциональные требования

### Модели

#### `Table` – столик в ресторане:
- **id**: int — уникальный идентификатор столика.
- **name**: str — название столика (например, "Table 1").
- **seats**: int — количество мест за столиком.
- **location**: str — местоположение столика (например, "зал у окна", "терраса").

#### `Reservation` – бронь:
- **id**: int — уникальный идентификатор брони.
- **customer_name**: str — имя клиента.
- **table_id**: int — внешний ключ на `Table`.
- **reservation_time**: datetime — время начала брони.
- **duration_minutes**: int — продолжительность брони в минутах.


## Как запустить проект

Для запуска проекта на локальной машине необходимо выполнить следующие шаги:

### 1. Установите зависимости:
1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/Genek91/table_reserve_service.git
    cd <папка_с_репозиторием>
    ```

2. Создайте и активируйте виртуальное окружение:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Linux/MacOS
    venv\Scripts\activate     # Для Windows
    ```

3. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

### 2. Настройка Docker:

Проект использует Docker для контейнеризации и docker-compose для организации работы всех компонентов.

1. Убедитесь, что у вас установлен **Docker** и **docker-compose**.

2. Сборка и запуск контейнеров:
    ```bash
    docker-compose up --build
    ```

3. После запуска, приложение будет доступно по адресу: [http://localhost:8000/docs/](http://localhost:8000/docs/).

### 3. Миграции базы данных:
Если вы хотите применить миграции, используйте команду:
```bash
docker-compose exec app alembic upgrade head
```

### 4. Запуск тестов:
Для запуска тестов с использованием pytest выполните команду:

```bash
pytest
```

Или запустить тесты в контейнере:

```bash
docker-compose exec app pytest
```

###  Пример запросов API
Получить список всех столиков:
```bash
GET /tables/
```
## Создать новый столик:
```bash
POST /tables/
{
  "name": "Table 1",
  "seats": 4,
  "location": "зал у окна"
}
```
## Удалить столик:
```bash
DELETE /tables/{id}
```
## Получить список всех броней:
```bash
GET /reservations/
```
## Создать новую бронь:
```bash
POST /reservations/
{
  "customer_name": "Иван Иванов",
  "table_id": 1,
  "reservation_time": "2025-04-08T18:00:00",
  "duration_minutes": 90
}
```
## Удалить бронь:
```bash
DELETE /reservations/{id}
```
