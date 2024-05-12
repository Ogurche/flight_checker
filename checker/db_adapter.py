# DB
import sqlite3 as sq
import pandas as pd 
import os

class DbConnection:
    def __init__(self):
        self.connection = sq.connect('my_database.db')
        self.cursor = self.connection.cursor()
    def __del__(self):
        self.cursor.close()
        self.connection.close()
    def execute_qr(self, query):
        self.cursor.execute(query)
        self.connection.commit()
    def select_qr(self, query, param = None):
        if param is not None:
            self.cursor.execute(query, (param,))
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()
    
class db_usage:
    def __init__(self,db_con :DbConnection):
        self.db_connection =db_con
    def decode(self, data:str):
        """
        API принимает название аэропорта отдает код. 
        Получает строку, отдает код 
        return short_code of airport
        """
        data = f'%{data.strip().title()}%'
        result = self.db_connection.select_qr('SELECT code FROM airports WHERE name LIKE ? ORDER BY code',data)
        if len(result) == 0:
            return None
        elif len(result) == 1:
            return result[0]
        else:
            if len(result) > 5: 
                return result[0:5]
            else:
                return result[0]
    def save_request(self, data: dict):
        """
        Сохранение запроса в БД
        """
        self.db_connection.execute_qr(f"INSERT INTO requests (origin, destination, dep_date, person_id) VALUES ({data['origin']}, {data['destination']}, '{data['dep_date']}', {data['person_id']})")

def init_db(db_:DbConnection):

    # Создаем таблицы в БД 
    # Airports: для определения shortcodes аэропорта по названию города/аэропорта

    db_.execute_qr('CREATE TABLE IF NOT EXISTS airports (id INTEGER PRIMARY KEY AUTOINCREMENT, city_code varchar\
                       , country_code varchar, code vacrchar, name varchar);')
                       
    # Tickets: сохранение билеов в БД (request_id - id запроса для связки сложных маршрутов)
    db_.execute_qr('CREATE TABLE IF NOT EXISTS tickets (id INTEGER PRIMARY KEY AUTOINCREMENT, origin INTEGER\
                       , destination INTEGER, dep_date date, price float4, num_of_flights INTEGER, request_id INTEGER);')
    
    # Requests: сохранение запросов в БД 
    db_.execute_qr('CREATE TABLE IF NOT EXISTS requests (id INTEGER PRIMARY KEY AUTOINCREMENT, origin INTEGER\
                   , destination INTEGER,dep_date date, person_id INTEGER);')

    # Airlines: справочник авиакомпаний 
    db_.execute_qr('CREATE TABLE IF NOT EXISTS airlines (id INTEGER PRIMARY KEY AUTOINCREMENT, code vacrchar, name varchar);')
    

def full_tables(db_:DbConnection):
    path = os.environ.get('PATH')
    # Создаем df для заполнения таблицы
    csv_ = pd.read_json(path + 'airports.json')
    df = pd.concat([csv_['city_code'], csv_['country_code'],csv_['code'], csv_['name']], axis=1)
    df.to_sql('airports', db_.connection, if_exists='replace', index=True)

    csv_airlines = pd.read_json(path + 'airlines.json')
    df = pd.concat([csv_airlines['code'], csv_airlines['name_translations'].map(lambda x: x['en'])], axis=1)
    df.to_sql('airlines', db_.connection, if_exists='replace', index=True)

def main():
    db_ = DbConnection()
    init_db(db_)
    full_tables(db_)
