import sqlite3


class Dbase:
    def __init__(self, db_name):
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()

    async def new_courier(self, id_user, username, data):
        self.cur.execute("""INSERT INTO dbase_expectation_courier (id_user, username_telegtam, name, number_phone, type_amusement, description) VALUES (?, ?, ?, ?, ?, ?)""",
                         (id_user, username, data['name'], data['phone'], data['type'], data['description']))
        self.con.commit()

    async def get_all(self):
        return self.cur.execute("""SELECT (id_user) FROM dbase_courier""").fetchall()

    async def get_expectation_all(self):
        return self.cur.execute("""SELECT (id_user) FROM dbase_expectation_courier""").fetchall()

    async def get_courier(self, id):
        return self.cur.execute("""SELECT (id_user)  FROM dbase_courier WHERE id_user = ?""", (id,)).fetchone()

    async def delete(self, id):
        self.cur.execute("""DELETE FROM dbase_expectation_courier WHERE id_user = ?""", (id,))
        self.con.commit()