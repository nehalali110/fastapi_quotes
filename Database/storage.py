import sqlite3

with sqlite3.connect("database.db") as con:
    cur = con.cursor()
    cur2 = con.cursor()

    create_tables = cur.execute("""
        CREATE TABLE IF NOT EXISTS quotes_temp2(
            id INTEGER PRIMARY KEY,
            quotation TEXT,
            author TEXT,
            created_at TEXT,
            modified_at TEXT,
            deleted_at TEXT                
                                )
""")
    
    check_Table = cur.execute("SELECT name from sqlite_master where name = 'quotes_temp2'")
    
    insert_data = cur2.execute("""
        INSERT INTO quotes_temp2(quotation, author)
        VALUES("this is the first delusional quote", "chris nolan"),
              ("Second quote is also delusional", "henry matt")
""")
    
    retrieve_tables = cur2.execute("SELECT * FROM quotes_temp")
    print(retrieve_tables.fetchall())