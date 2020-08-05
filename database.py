import sqlite3


class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS items (item text PRIMARY KEY, price integer)")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS machines (number integer)")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS users (username text PRIMARY KEY, password text)")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS prices (name text PRIMARY KEY, price integer)")
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS calculations (day integer, month integer, price integer,
                    starthour integer, startminute integer, endhour integer, endminute integer,
                    items text, machine integer, calculation integer)""")
        self.conn.commit()

    def fetch_items(self):
        self.cur.execute("SELECT * FROM items")
        rows = self.cur.fetchall()
        return rows

    def fetch_machines(self):
        self.cur.execute("SELECT * FROM machines")
        row = self.cur.fetchone()
        return row

    def fetch_users(self):
        self.cur.execute("SELECT * FROM users")
        rows = self.cur.fetchall()
        return rows

    def fetch_prices(self):
        self.cur.execute("SELECT * FROM prices")
        rows = self.cur.fetchall()
        return rows

    def fetch_calculations(self):
        # Will need a date parameter
        self.cur.execute("SELECT * FROM calculations")
        rows = self.cur.fetchall()
        return rows

    def fetch_needed_data(self):
        # self.conn = sqlite3.connect(db)
        # self.cur = self.conn.cursor()
        items = self.fetch_items()
        machines = self.fetch_machines()
        users = self.fetch_users()
        prices = self.fetch_prices()

        return items, machines, users, prices

    def insert_into_items(self, item, price):
        self.cur.execute("INSERT INTO items VALUES (?, ?)",
                         (item, price))
        self.conn.commit()

    def insert_into_machines(self, number):
        self.cur.execute("INSERT INTO machines VALUES (?)",
                         (number,))
        self.conn.commit()

    def insert_into_users(self, username, password):
        self.cur.execute("INSERT INTO users VALUES (?, ?)",
                         (username, password))
        self.conn.commit()

    def insert_into_prices(self, name, price):
        self.cur.execute("INSERT INTO prices VALUES (?, ?)",
                         (name, price))
        self.conn.commit()

    def insert_into_calculations(self, day, month, year, sh, sm, eh, em, items, machine, calculation):
        self.cur.execute("INSERT INTO calculations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                         (day, month, year, sh, sm, eh, em, items, machine, calculation))
        self.conn.commit()

    def remove_from_items(self, item):
        self.cur.execute("DELETE FROM items WHERE item=?", (item,))
        self.conn.commit()

    def remove_from_machines(self, number):
        self.cur.execute("DELETE FROM machines WHERE number=?", (number,))
        self.conn.commit()

    def remove_from_users(self, username):
        self.cur.execute("DELETE FROM users WHERE username=?", (username,))
        self.conn.commit()

    def remove_from_prices(self, name):
        self.cur.execute("DELETE FROM prices WHERE name=?", (name,))
        self.conn.commit()

    def remove_from_calculations(self, calculation_id):
        self.cur.execute("DELETE FROM calculations WHERE oid=?", (calculation_id,))
        self.conn.commit()

    def update_item(self, item, price, item_id):
        self.cur.execute("UPDATE items SET item = ?, price = ? WHERE oid = ?",
                         (item, price, item_id))
        self.conn.commit()

    def update_machine(self, number, machine_id):
        self.cur.execute("UPDATE machines SET number = ? WHERE oid = ?",
                         (number, machine_id))
        self.conn.commit()

    def update_user(self, username, password, user_id):
        self.cur.execute("UPDATE users SET  username = ?, password = ? WHERE oid = ?",
                         (username, password, user_id))
        self.conn.commit()

    def update_price(self, name, price, name_id):
        self.cur.execute("UPDATE prices SET name = ?, price = ? WHERE oid = ?",
                         (name, price, name_id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

# db = Database('configurations.db')
