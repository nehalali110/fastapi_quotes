import sqlite3, os
import utils.helpers
import Database.schema
from Database.hash import hash_password
import bcrypt
import jwt



def get_quotes_from_db(cur, user_id, author, search, limit):
    if not author and not search and not limit:
        return cur.execute("SELECT * FROM quotes_temp WHERE user_id=?",(user_id,)).fetchall()

    query = "SELECT * FROM quotes_temp"
    params = ["user_id=?"]
    values = [user_id]
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



def post_quotes_to_db(cur, user_id, quotation, author):
    cur.execute("""
        INSERT INTO quotes_temp(quotation, author, created_at, user_id) VALUES(?, ?, ?, ?)
""",(quotation, author, utils.helpers.add_timestamp(), user_id))


def update_quotes_to_db(cur, user_id, quote_id, quotation, author):
    params = {
        "quotation" : quotation,
        "author" : author
    }
    for key,value in params.items():
        if value:
            cur.execute(f"UPDATE quotes_temp SET {key}=?, modified_at=? WHERE id=? AND user_id=?", (value, utils.helpers.add_timestamp(), quote_id, user_id))


def delete_quotes_from_db(cur, user_id, quote_id):
    cur.execute("UPDATE quotes_temp SET deleted_at=? WHERE id=? AND user_id=?", (utils.helpers.add_timestamp(), quote_id, user_id))



def create_user(cur, user_email, user_pass):
    hash = hash_password(user_pass)
    cur.execute("INSERT INTO users(email, password) VALUES(?,?);", (user_email, hash))


def verify_user(cur, user_email, user_pass):
    search_user_query = "SELECT * FROM users WHERE email = ?"
    result = cur.execute(search_user_query, (user_email,)).fetchall()
   

    # checking if the password hash matches too
    if result:
        db_user_id = result[0][0]
        db_user_email = result[0][1]
        db_user_password_hash = result[0][2]
        if bcrypt.checkpw(user_pass.encode(), db_user_password_hash.encode()):
            user_jwt_token = utils.helpers.generate_token(db_user_id, db_user_email)
            return user_jwt_token

    else:        
        return []
   
if __name__ == "__main__":
    main()