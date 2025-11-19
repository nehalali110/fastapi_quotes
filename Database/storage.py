import sqlite3, os
import utils.helpers
import Database.schema
from Database.hash import hash_password
import bcrypt
        
def main():
    Database.schema.initial_run()
    get_quotes_from_db(None, "i", None)


def get_quotes_from_db(cur, author, search, limit):
    if not author and not search and not limit:
        return cur.execute("SELECT * FROM quotes_temp").fetchall()

    query = "SELECT * FROM quotes_temp"
    params = []
    values = []
    if author:
        params.append("LOWER(author)=?")
        values.append(author.lower())

    if search:
        params.append("LOWER(quotation) LIKE ?")
        values.append(f"%{search.lower()}%")

    if author or search:
        query += " WHERE " + " AND ".join(params)

    if limit:
        query += " LIMIT ?"
        values.append(limit)

    get_results = cur.execute(query, tuple(values))
    return get_results.fetchall()



def post_quotes_to_db(cur, quotation, author):
    cur.execute("""
        INSERT INTO quotes_temp(quotation, author, created_at) VALUES(?, ?, ?)
""",(quotation, author, utils.helpers.add_timestamp()))


def update_quotes_to_db(cur, quote_id, quotation, author):
    params = {
        "quotation" : quotation,
        "author" : author
    }
    for key,value in params.items():
        if value:
            cur.execute(f"UPDATE quotes_temp SET {key}=?, modified_at=? WHERE id=?", (value, utils.helpers.add_timestamp(), quote_id))


def delete_quotes_from_db(cur, quote_id):
    cur.execute("UPDATE quotes_temp SET deleted_at=? WHERE id=?", (utils.helpers.add_timestamp(), quote_id))



def create_user(cur, user_email, user_pass):
    hash = hash_password(user_pass)
    cur.execute("INSERT INTO users(email, password) VALUES(?,?);", (user_email, hash))


def verify_user(cur, user_email, user_pass):
    search_user_query = f"SELECT * FROM users WHERE email = ? AND TRUE"
    result = cur.execute(search_user_query, (user_email))
    return result.fetchall()

if __name__ == "__main__":
    main()

