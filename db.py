import sqlite3 as sql



db = sql.connect('DataBase.db')
with db:
    cur = db.cursor()
    cur.execute("""CREATE TABLE if not exists passwords (
        chatid TEXT,
        name TEXT,
        password TEXT
        )""")
    db.commit()

class database:
    def new_pass_name(self, user_id : str, name : str, password : str) -> dict:
        cur.execute(""" INSERT INTO passwords ("chatid", "name", "password") VALUES (?,?,?) """, (user_id, name, password))
        db.commit()
        return {"status" : True}

    def select_name_from_id(self, user_id : str) -> dict:
        cur.execute(""" SELECT name FROM passwords WHERE chatid = ? """, (user_id,))
        result = cur.fetchall()

        return {"status" : True, "result" : result}
    
    def select_name_from_name(self, user_id : str, name : str) -> dict:
        cur.execute(""" SELECT password FROM passwords WHERE chatid = ? AND name = ? """, (user_id, name))
        result = cur.fetchall()

        return {"status" : True, "result" : result}