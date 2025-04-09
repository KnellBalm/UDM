############### sample use ####################
# from PostgreSQL_Connection import DB_conn
# conn = DB_conn(db_key='suwon', config_file = 'db_conn_config.json')
# query = 'SELECT * FROM public.test;'
# df = db.execute_query_df(query) 
# del db 
###############################################
import pandas as pd
import psycopg2
from psycopg2 import sql
import json

class DB_conn:
    def __init__(self, db_key, config_file='db_conn_config.json'):
        try:
            # 외부 config 파일에서 모든 DB 연결 정보 로드
            with open(config_file, 'r') as f:
                config_data = json.load(f)
            
            # 여러 DB 중 선택된 db_key의 연결 정보 사용
            conn_dict = config_data['databases'][db_key]

            self.db = psycopg2.connect(
                host=conn_dict['host'],
                port=conn_dict['port'],
                dbname=conn_dict['dbname'],
                user=conn_dict['user'],
                password=conn_dict['passwd']
            )
            self.cursor = self.db.cursor()
        except KeyError:
            print(f"Database configuration for '{db_key}' not found.")
        except Exception as e:
            print("Database connection failed: ", e)

    def __del__(self):
        try:
            self.cursor.close()
            self.db.close()
        except Exception as e:
            print("Error closing database connection: ", e)

    def execute_query(self, query, args=None):
        try:
            self.cursor.execute(query, args)
            rows = self.cursor.fetchall()
            return rows
        except Exception as e:
            print(f"Error executing query: {e}")
            return None

    def execute_query_df(self, query, args=None, columns=None):
        try:
            self.cursor.execute(query, args)
            rows = self.cursor.fetchall()
            if columns:
                return pd.DataFrame(rows, columns=columns)
            return pd.DataFrame(rows)
        except Exception as e:
            print(f"Error executing query and fetching data: {e}")
            return pd.DataFrame()

    def execute_and_commit(self, query, args=None):
        try:
            self.cursor.execute(query, args)
            self.db.commit()
        except Exception as e:
            print("Error executing and committing query: ", e)
            self.db.rollback()

    def insert(self, schema, table, columns, values):
        query = sql.SQL("INSERT INTO {}.{} ({}) VALUES (%s);").format(
            sql.Identifier(schema),
            sql.Identifier(table),
            sql.SQL(', ').join(map(sql.Identifier, columns))
        )
        self.execute_and_commit(query, (values,))

    def read(self, schema, table, columns):
        query = sql.SQL("SELECT {} FROM {}.{};").format(
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.Identifier(schema),
            sql.Identifier(table)
        )
        rows = self.execute_query(query)
        if rows:
            return pd.DataFrame(rows, columns=columns)
        return pd.DataFrame()

    def update(self, schema, table, column, value, condition):
        query = sql.SQL("UPDATE {}.{} SET {} = %s WHERE {};").format(
            sql.Identifier(schema),
            sql.Identifier(table),
            sql.Identifier(column),
            sql.SQL(condition)
        )
        self.execute_and_commit(query, (value,))

    def delete(self, schema, table, condition):
        query = sql.SQL("DELETE FROM {}.{} WHERE {};").format(
            sql.Identifier(schema),
            sql.Identifier(table),
            sql.SQL(condition)
        )
        self.execute_and_commit(query)
