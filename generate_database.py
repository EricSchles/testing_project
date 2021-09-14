import sqlite3 as sql
from random import choice, randint, random
from num2words import num2words

def clean_string(string: str) -> str:
    return "_".join(string.split("-"))

def get_table_name(num: int) -> str:
    base_table_name = "_table"
    word_number = num2words(str(num))
    word_number = clean_string(word_number)
    return word_number+base_table_name

def create_db_connection(db_name: str) -> sql.Connection:
    return sql.connect(db_name)

def generate_tables(connection: sql.Connection, num_tables: int):
    engine = connection.cursor()
    for table_index in range(1, num_tables+1):
        table_name = get_table_name(table_index)
        engine.execute(f'''
        CREATE TABLE {table_name}
        (id int PRIMARY KEY, col_one text, 
        col_two text, col_three text,
        col_four real, col_five real)
        ''')
        connection.commit()
    engine.close()
        
def generate_data(connection: sql.Connection, num_tables: int):
    engine = connection.cursor()
    col_one = [
        "Asked", "Assisted client in",
        "Acknowledged", "Affirmed",
        "Challenged", "Clarified",
        "Coached", "Collaborated", "De-escalated",
        "Demonstrated", "Developed", "Directed",
        "Discussed", "Encouraged", "Explained",
        "Examined", "Explored", "Evaluated",
        "Facilitated", "Focused on", "Gave homework",
        "Guided", "Instructed", "Interpreted",
        "Introduced", "Inquired about", "Listened"
        "Paraphrased", "Performed", "Planned",
        "Practiced", "Praised", "Prompted",
        "Provided", "Redirected",
        "Reflected back", "Reframed",
        "Refocused", "Reinforced", "Responded to",
        "Reviewed", "Role played"
        "Set boundaries",
        "Shared", "Supported", "Trained",
        "Validated", "NULL"
    ]
    col_two = ["alive", "dead", "comma", "NULL", "NILL", "NIL"]
    col_three = [
        "minor", "moderate", "severe",
        "extreme", "NONE", "none",
        "None", "NILL", "NIL"
    ]
    for table_index in range(1, num_tables+1):
        num_rows = randint(10, 10000)
        table_name = get_table_name(table_index)
        for row_index in range(num_rows):
            col_one_choice = choice(col_one)
            col_two_choice = choice(col_two)
            col_three_choice = choice(col_three)
            col_four_choice = randint(0, 10) + random()
            col_five_choice = randint(0, 3) + random()
            engine.execute(f"""
            INSERT INTO {table_name} VALUES (
            {row_index}, '{col_one_choice}', '{col_two_choice}',
            '{col_three_choice}', {col_four_choice},
            {col_five_choice})
            """)

            connection.commit()
    engine.close()

if __name__ == '__main__':
    connection = create_db_connection("example.db")
    number_of_tables = 10
    generate_tables(connection, number_of_tables)
    generate_data(connection, number_of_tables)
