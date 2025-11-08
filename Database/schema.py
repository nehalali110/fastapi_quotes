import sqlite3, os

def create_quotes_table():
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("""
                CREATE TABLE IF NOT EXISTS quotes_temp(
                        id INTEGER PRIMARY KEY,
                        quotation TEXT,
                        author TEXT,
                        created_at TEXT,
                        modified_at TEXT,
                        deleted_at TEXT
                    );
            """)
        cur.execute("""
                INSERT INTO quotes_temp(quotation, author)
                VALUES("In the end only one thing matters, who stands at the top", "Sosuke Aizen"),
                       ("Until I meet him not even death himself could touch me", "Roranoa Zoro");
            """)


def initial_run():
    if not os.path.exists("C:\\Windows\\Temp\\First_run.txt"):
        print("Running first time!")
        create_quotes_table()
        with open("C:\\Windows\\Temp\\First_run.txt", "w") as f:
            f.write("File has been ran!")
    else:
        print("Not running first time!")


def clear_database():
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("DELETE FROM quotes_temp")

def drop_table(table_name):
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute(f"DROP TABLE {table_name}")