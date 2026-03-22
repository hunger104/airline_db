import os
from sqlmodel import create_engine, Session
from dotenv import load_dotenv

load_dotenv()

# Параметры подключения к вашей базе авиакомпании
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "airline_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "agent")

# Формируем строку подключения (URL)
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Создаем движок
engine = create_engine(DATABASE_URL, echo=True)

# Функция для получения сессии (нужна для записи и чтения данных)
def get_session():
    with Session(engine) as session:
        yield session

# Функция инициализации (создания таблиц)
def init_db():
    from sqlmodel import SQLModel
    import models
    SQLModel.metadata.create_all(engine)
    print("Таблицы авиакомпании успешно инициализированы!")
