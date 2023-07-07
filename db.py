import sqlite3 as sql



db = sql.connect('DataBase.db')
with db:
    cur = db.cursor()
    cur.execute("""CREATE TABLE if not exists passwords (
        chatid TEXT,
        name TEXT,
        password TEXT
        )""")
    cur.execute("""CREATE TABLE if not exists users (
        chatid TEXT
        )""")
    db.commit()

class database:
    def new_pass_name(self, user_id : str, name : str, password : str) -> dict:
        cur.execute(""" INSERT INTO passwords ("chatid", "name", "password") VALUES (?,?,?) """, (user_id, name, password))
        db.commit()
        return {"status" : True}
    
    def new_user(self, user_id : str) -> dict:
        cur.execute(""" SELECT chatid FROM users WHERE chatid = ? """, (user_id,))
        f = cur.fetchall()
        if len(f) > 0: pass
        else:  cur.execute(""" INSERT INTO users ("chatid") VALUES (?) """, (user_id,))
        db.commit()
        return {"status" : True}

    def select_all_users(self) -> dict:
        cur.execute(""" SELECT chatid FROM users """)
        users = cur.fetchall()
        return {"number" : len(users), "id" : users}

    def select_name_from_id(self, user_id : str) -> dict:
        cur.execute(""" SELECT name FROM passwords WHERE chatid = ? """, (user_id,))
        result = cur.fetchall()

        return {"status" : True, "result" : result}
    
    def select_name_from_name(self, user_id : str, name : str) -> dict:
        cur.execute(""" SELECT password FROM passwords WHERE chatid = ? AND name = ? """, (user_id, name))
        result = cur.fetchall()

        return {"status" : True, "result" : result}

    def delate_name_from_name(self, user_id : str, name : str) -> dict:
        print(name)
        cur.execute(""" DELETE FROM passwords WHERE chatid = ? AND name = ? """, (user_id, name))
        db.commit()
        return {"status" : True}