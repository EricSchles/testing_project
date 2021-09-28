import sqlite3 as sql
from num2words import num2words
from clean_data import get_table_name, create_db_connection, clean_string
import random
import pandas as pd

def test_check_sqlconn():
    try:
        connection = sql.connect('example.db')
        connection.cursor()
        assert True
    except:
        assert False
    

def test_file_exists():
    try:
        with open("example.db", "rb") as f:
            text = f.read()
        assert text != ''
    except:
        assert False

# not an exercise, this is just to show you stuff.
def test_other_files_dont_exist():
    try:
        with open("whatever.txt", "r") as f:
            text = f.read()
        assert False
    except:
        assert True

def test_database_connection():
    connection = create_db_connection("example.db")
    engine = connection.cursor()
    table = num2words(random.randint(1, 10)) + "_table"
    result = engine.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    assert result > 0

def test_database_connection_pd():
    connection = create_db_connection("example.db")
    table = num2words(random.randint(1, 10)) + "_table"
    df = pd.read_sql_query(f"SELECT * FROM {table} LIMIT 1", connection)
    assert df is not None

def test_all_columns_exist_pd():
    connection = create_db_connection("example.db")
    num_tables = 10
    columns = [
        "id", "col_one", "col_two", "col_three",
        "col_four", "col_five"
    ]
    size = None
    for table_index in range(1, num_tables+1):
        table = get_table_name(table_index)
        df = pd.read_sql_query(f"SELECT * FROM {table}", connection)
        assert df.columns.tolist() == columns
        if size is None:
            size = df.shape[0]
        assert size == df.shape[0]
        
def test_all_columns_exist():
    connection = create_db_connection("example.db")
    engine = connection.cursor()
    num_tables = 10
    columns = [
        "col_one", "col_two", "col_three",
        "col_four", "col_five"
    ]
    for table_index in range(1, num_tables+1):
        table_name = get_table_name(table_index)
        not_first = False
        for column in columns:
            result = engine.execute(f"""
            SELECT COUNT({column})
            FROM {table_name}
            """).fetchone()[0]
            assert result > 0
            if not_first:
                assert result == prev_result
            not_first = True
            prev_result = result
        result = 0

def test_null_uniqueness_pd():
    connection = create_db_connection("example.db")
    num_tables = 10
    null_values = [
        "nill", "null",
        "nil"
    ]
    for table_index in range(1, num_tables+1):
        table = get_table_name(table_index)
        df = pd.read_sql_query(f"SELECT * FROM {table}", connection)
        for column in df.select_dtypes(["object"]):
            unique_values = df[column].str.lower().unique()
            assert not any([
                null_value in unique_values
                for null_value in null_values
            ])
            
def test_null_uniqueness():
    con = sql.connect("example.db")
    cur = con.cursor()
    results = cur.execute("SELECT * FROM one_table").fetchall()
    null_values = [
        "none", "nill", "null",
        "nil"
    ]
    for result in results:
        for val in result:
            if isinstance(val, str):
                if val.lower() in null_values and val != "none":
                    assert False
    assert True

if __name__ == '__main__':
    test_null_uniqueness_pd()
