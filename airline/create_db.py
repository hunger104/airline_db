# Создаем базу данных Авиакомпании

from dotenv import load_dotenv
import os
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Загружаем переменные из файла .env (если он есть)
load_dotenv()

# Параметры для подключения к PostgreSQL
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "airline_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "agent")

# Функция создания БД
def create_database(dbname: str):
    # Подключаемся к системной базе "postgres", чтобы создать новую базу
    conn = psycopg2.connect(
        dbname='postgres',
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    try:
        # Пытаемся создать базу данных
        cur.execute(sql.SQL('CREATE DATABASE {}').format(sql.Identifier(dbname)))
        print(f"База данных '{dbname}' успешно создана!")
    except psycopg2.errors.DuplicateDatabase:
        # Если база уже есть, выводим сообщение
        print(f"База данных '{dbname}' уже существует")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    create_database(DB_NAME)
