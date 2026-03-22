# Инициализация таблиц в БД

from sqlmodel import SQLModel
from db import engine
import models

def init_tables():
    # Эта команда берет все классы, унаследованные от SQLModel,
    # и создает соответствующие таблицы в базе данных.
    SQLModel.metadata.create_all(engine)
    print("Успех: Таблицы авиакомпании созданы (если их не было).")

if __name__ == '__main__':
    init_tables()
