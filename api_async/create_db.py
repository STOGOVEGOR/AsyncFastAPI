from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Data1, Data2, Data3
from database import Base
import psycopg2

DB_USER = 'pgadmin'
DB_PASSWORD = 'pgadmin'
# DB_HOST = '127.0.0.1'
DB_HOST = 'db'
DB_PORT = '5432'
DB_NAME = 'apitest'

DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}'


def create_database():
    conn = psycopg2.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT, database='postgres')
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
    exists = cursor.fetchone()

    if not exists:
        cursor.execute(f"CREATE DATABASE {DB_NAME}")

    cursor.close()
    conn.close()


def create_tables(engine):
    Base.metadata.create_all(engine)


def populate_data(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    if not session.query(Data1).first():
        data1_entries = [Data1(id=i, name=f"Test {i}") for i in range(1, 11)] + \
                        [Data1(id=i, name=f"Test {i}") for i in range(31, 41)]
        session.add_all(data1_entries)

    if not session.query(Data2).first():
        data2_entries = [Data2(id=i, name=f"Test {i}") for i in range(11, 21)] + \
                        [Data2(id=i, name=f"Test {i}") for i in range(41, 51)]
        session.add_all(data2_entries)

    if not session.query(Data3).first():
        data3_entries = [Data3(id=i, name=f"Test {i}") for i in range(21, 31)] + \
                        [Data3(id=i, name=f"Test {i}") for i in range(51, 61)]
        session.add_all(data3_entries)

    session.commit()
    session.close()


def main():
    create_database()
    engine = create_engine(f'{DATABASE_URL}/{DB_NAME}')
    create_tables(engine)
    populate_data(engine)


if __name__ == "__main__":
    main()
