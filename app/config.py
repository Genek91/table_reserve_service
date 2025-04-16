import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Класс настроек приложения.

    Methods:
        model_config: Конфигурация загрузки переменных окружения из файла .env.
    """
    app_title: str = "API-сервис бронирования столиков в ресторане"
    description: str = (
        "Разработать REST API для бронирования столиков в ресторане. "
        "Сервис должен позволять создавать, просматривать и удалять брони, "
        "а также управлять столиками и временными слотами."
    )

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", ".env"
        )
    )


settings = Settings()


def get_db_url():
    """
    Возвращает строку подключения к базе данных PostgreSQL с использованием
    asyncpg драйвера.

    Returns:
        str: Строка подключения.
    """
    return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
