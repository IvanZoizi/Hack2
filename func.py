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

    async def new_user(self, id):
        user = self.cur.execute("""SELECT * FROM dbase_userstelegram WHERE id_user_telegram = ?""", (id,)).fetchone()
        if not user:
            self.cur.execute("""INSERT INTO dbase_userstelegram(id_user_telegram) VALUES(?)""", (id,))
            self.con.commit()

    async def get_food_type(self, type_):
        return self.cur.execute("""SELECT * FROM dbase_food WHERE type_food = ?""", (type_,)).fetchall()

    async def get_business(self):
        return self.cur.execute("""SELECT * FROM dbase_business""").fetchall()

    async def new_feedback(self, username, data):
        food = self.cur.execute("""SELECT * FROM dbase_food WHERE id_food = ?""", (data['ref'],)).fetchone()
        self.cur.execute("""INSERT INTO dbase_feedback(username, food_title, stars, description) VALUES(?, ?, ?, ?) """,
                         (username, food[1], data['stars'], data['des']))
        self.con.commit()

    async def new_feedback_business(self, username, data):
        food = self.cur.execute("""SELECT * FROM dbase_business WHERE id = ?""", (data['ref'],)).fetchone()
        self.cur.execute("""INSERT INTO dbase_feedback(username, food_title, stars, description) VALUES(?, ?, ?, ?) """,
                         (username, food[1], data['stars'], data['des']))
        self.con.commit()

    async def get_order(self):
        return self.cur.execute("""SELECT * FROM dbase_neworders WHERE delivery = ?""", ('Да',)).fetchone()

    async def get_order_id(self):
        return self.cur.execute("""SELECT * FROM dbase_neworders WHERE delivery = ?""", ('Да',)).fetchall()

    async def new_delivery(self, id_order, username_order, phone):
        self.cur.execute("""INSERT INTO dbase_deliveryorders(id_order, courier_username, courier_phone) VALUES (?, ?, ?)""",
                         (id_order, username_order, phone))
        self.con.commit()

    async def send(self, id_courier, id_order):
        self.cur.execute("""INSERT INTO dbase_send(id_order, id_courier) VALUES(?, ?)""", (id_order, id_courier))
        self.con.commit()

    async def get_send(self, id_courier, id_order):
        return self.cur.execute("""SELECT * FROM dbase_send WHERE id_order = ? AND id_courier = ?""", (id_order, id_courier)).fetchone()