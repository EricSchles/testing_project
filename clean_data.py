import sqlite3 as sql
from num2words import num2words
from typing import List
import pandas as pd

def clean_string(string: str) -> str:
    return "_".join(string.split("-"))

def get_table_name(num: int) -> str:
    base_table_name = "_table"
    word_number = num2words(str(num))
    word_number = clean_string(word_number)
    return word_number+base_table_name

def create_db_connection(db_name: str) -> sql.Connection:
    return sql.connect(db_name)

def insert_row(connection, engine, table, row):
    index, col_one, col_two, col_three, col_four, col_five = row
    engine.execute(f"""
    INSERT INTO {table} VALUES (
    {index}, '{col_one}', '{col_two}',
    '{col_three}', {col_four},
    {col_five})
    """)
    connection.commit()

def get_table_pd(table: str, connection: sql.Connection) -> pd.DataFrame:
    query = f"""
    SELECT *
    FROM {table}
    """
    return pd.read_sql_query(query, connection)
    
def get_rows(table: str) -> List:
    return engine.execute(
    f"""
    SELECT *
    FROM {table}
    """).fetchall()

def dedupe_nulls_pd(table: str, connection, replace_value) -> pd.DataFrame:
    null_values = [
        "nill", "null",
        "nil"
    ]
    for value in null_values:
        null_values.append(value.capitalize())
        null_values.append(value.upper())
    df = get_table_pd(table, connection)
    for null_value in null_values:
        df = df.replace(to_replace=f"{null_value}", value="none")
    return df
        
def dedupe_nulls(rows):
    null_values = [
        "none", "nill", "null",
        "nil"
    ]
    new_rows = []
    for row in rows:
        new_row = []
        for val in row:
            if isinstance(val, str) and val.lower() in null_values:
                val = "none"
            new_row.append(val)
        new_rows.append(tuple(new_row))
    return new_rows

def drop_table(engine, table):
    engine.execute(f"""
    DROP TABLE IF EXISTS {table}
    """)

def recreate_table(engine, table):
    engine.execute(f'''
    CREATE TABLE {table}
    (id int PRIMARY KEY, col_one text, 
    col_two text, col_three text,
    col_four real, col_five real)
    ''')

def main(database_name):
    connection = create_db_connection(database_name)
    engine = connection.cursor()
    num_tables = 10
    
    for table_index in range(1, num_tables+1):
        table = get_table_name(table_index)
        rows = get_rows(table)
        new_rows = dedupe_nulls(rows)
        drop_table(engine, table)
        recreate_table(engine, table)
        for row in new_rows:
            insert_row(connection, engine, table, row)
    engine.close()

def main_pd(database_name):
    connection = create_db_connection(database_name)
    num_tables = 10
    for table_index in range(1, num_tables+1):
        table = get_table_name(table_index)
        df = dedupe_nulls_pd(table, connection, replace_value)
        df.to_sql(table, connection, if_exists="replace")
    
if __name__ == '__main__':
    main("example.db")
    
