import sqlite3
import hashlib
import platform
import os
import uuid



STATUSES = [
    "❌Не начато",
    "▶В работе",
    "⏸На паузе",
    "✅Завершено"
]


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('./resources/data/diary.db')


        # Переопределение функции преобразования к нижнему регистру https://docs-python.ru/standart-library/modul-sqlite3-python/sravnenie-kirillitsy-sqlite-ucheta-registra/
        def sqlite_lower(value_):
            return value_.lower()
        def sqlite_upper(value_):
            return value_.upper()

        # Переопределение правила сравнения строк
        def ignore_case_collation(value1_, value2_):
            if value1_.lower() == value2_.lower():
                return 0
            elif value1_.lower() < value2_.lower():
                return -1
            else:
                return 1

        self.conn.create_collation("NOCASE", ignore_case_collation)
        self.conn.create_function("LOWER", 1, sqlite_lower)
        self.conn.create_function("UPPER", 1, sqlite_upper)


        self.c = self.conn.cursor()


        # проверяем что таблицы существуют, чтобы не добавлять данные лишний раз
        self.c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='diary' ''')


        if self.c.fetchone()[0] == 1:
            return

        self.c.execute('''
                       CREATE TABLE IF NOT EXISTS
                       diary (
                           id INTEGER PRIMARY KEY,
                           starts_at TEXT,
                           ends_at TEXT,
                           description TEXT,
                           type_id INTEGER,
                           priority INTEGER DEFAULT 1,
                           status INTEGER DEFAULT 0,
                           user_id INTEGER,
                           FOREIGN KEY(user_id) REFERENCES user(id),
                           FOREIGN KEY(type_id) REFERENCES type(id)
                           )''') #starts_at и ends_at -- datetime, в sqlite хранятся как text
                                    # status -- номер статуса в константном списке STATUSES
                                    # priority -- важность от 1 (наименее важное) до 5 (важнейшее)
        self.c.execute('''
                       CREATE TABLE IF NOT EXISTS
                       user (
                           id INTEGER PRIMARY KEY,
                           name TEXT,
                           password_hash TEXT
                           )''')
        self.c.execute('''
                       CREATE TABLE IF NOT EXISTS
                       type (
                           id INTEGER PRIMARY KEY,
                           name TEXT
                           )''')

        self.c.execute('''
                       CREATE TABLE IF NOT EXISTS
                       saved_users (
                           pc_hash TEXT PRIMARY KEY,
                           user_id INTEGER,
                           FOREIGN KEY(user_id) REFERENCES user(id),
                           )''')

        self.add_data_type("")
        self.add_data_type("Учёба")
        self.add_data_type("Работа")
        self.add_data_type("Развлечения")
        self.add_data_type("Спорт")
        self.add_data_type("Другое")

        from datetime import datetime as dt, timedelta as td

        from random import randint as r

        for i in range(22):
            self.c.execute('''INSERT INTO diary(user_id, starts_at, ends_at, description, priority, type_id, status) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                       (r(1, 10), dt.today() - td(days=r(0, 11)), dt.now() + td(days=r(0, 11)), f"Задача {i+1}", r(1, 5), r(2, 6), r(0, 3)))


        self.conn.commit()



    def insert_data(self, user_id, starts_at, ends_at, description, type_id, priority) -> int:
        params = (user_id, starts_at, ends_at, description, type_id, priority)
        self.c.execute('''INSERT INTO diary(user_id, starts_at, ends_at, description, type_id, priority) VALUES (?, ?, ?, ?, ?, ?)''', params)
        self.conn.commit()
        self.c.execute('''SELECT id FROM diary ORDER BY id DESC LIMIT 1;''')
        return self.c.fetchone()


    def remove_data(self, id):
        self.c.execute('''DELETE FROM diary WHERE id=?''', (id,))
        self.conn.commit()


    def fetch_all_data(self, user_id):
        self.c.execute('''SELECT * FROM diary WHERE user_id=?''', (user_id,))
        return self.c.fetchall()


    def get_data_types(self):
        self.c.execute('''SELECT * FROM type''')
        return self.c.fetchall()


    def add_data_type(self, name):
        self.c.execute('''INSERT INTO type(name) VALUES (?)''', (name,))
        self.conn.commit()


    def remove_data_type(self, id):
        self.c.execute('''DELETE FROM type WHERE id=?''', (id,))
        self.conn.commit()


    def filter_data(self, user_id,
                    starts_from=None, starts_to=None,
                    ends_from=None, ends_to=None,
                    description=None, types_ids=None,
                    min_priority=None, statuses_ids=None) -> list:

        filters = []

        if starts_from:
            filters.append(self.append_starts_at_filter(starts_from, ">="))
        if starts_to:
            filters.append(self.append_starts_at_filter(starts_to, "<="))
        if ends_from:
            filters.append(self.append_ends_at_filter(ends_from, ">="))
        if ends_to:
            filters.append(self.append_ends_at_filter(ends_to, "<="))
        if description:
            filters.append(self.append_description_filter(description))
        if types_ids:
            filters.append(self.append_types_ids_filter(types_ids))
        if min_priority:
            filters.append(self.append_priority_filter(min_priority))
        if statuses_ids:
            filters.append(self.append_statuses_ids_filter(statuses_ids))

        if not filters:
            return self.fetch_all_data(user_id)

        query = f"SELECT * FROM diary WHERE user_id=? "
        parameters = [user_id]

        for filter in filters:
            query += f" AND {filter[0]}"
            if isinstance(filter[1], list):
                parameters.extend(filter[1])
            else:
                parameters.append(filter[1])

        print(query)
        print(parameters)
        self.c.execute(query, parameters)
        return self.c.fetchall()


    def append_starts_at_filter(self, starts_at, starts_predicate):
        return self.append_filter("starts_at", starts_at, starts_predicate)

    def append_ends_at_filter(self, ends_at, ends_predicate):
        return self.append_filter("ends_at", ends_at, ends_predicate)

    def append_description_filter(self, description):
        return self.append_filter("description", description, "like")

    def append_types_ids_filter(self, types_ids):
        return self.append_filter("type_id", types_ids, "in")

    def append_priority_filter(self, min_priority):
        return self.append_filter("priority", min_priority, ">=")

    def append_statuses_ids_filter(self, statuses_ids):
        return self.append_filter("status", statuses_ids, "in")

    @staticmethod
    def append_filter(column, value, predicate="=="):
        if predicate == "<=":
            return f"{column} <= ?", value
        if predicate == "==":
            return f"{column} = ?", value
        if predicate == ">=":
            return f"{column} >= ?", value
        if predicate == "in":
            return f"{column} IN (%s)"  % ','.join('?' for _ in value), value 
        if predicate == "like":
            return f"LOWER({column}) LIKE ?", f"%{value.lower()}%"


    def update_starts_at(self, id, new_data):
        self.update_column(id, "starts_at", new_data)

    def update_ends_at(self, id, new_data):
        self.update_column(id, "ends_at", new_data)

    def update_description(self, id, new_data):
        self.update_column(id, "description", new_data)

    def update_type_id(self, id, new_data):
        self.update_column(id, "type_id", new_data)

    def update_priority(self, id, new_data):
        self.update_column(id, "priority", new_data)

    def update_status(self, id, new_data):
        self.update_column(id, "status", new_data)

    def update_column(self, id, coulmn_name, new_data):
        self.c.execute(f'''UPDATE diary SET {coulmn_name}=? WHERE ID=?''',
            (new_data, id))
        self.conn.commit()


    @staticmethod
    def get_hash(s: str):
        encoded = s.encode('utf-8')
        return hashlib.sha256(encoded).hexdigest()

    @staticmethod
    def get_host_pc_hash():
        uname = platform.uname()
        platform_info = f"{os.getlogin()}-{uname.system}-{uname.node}-{uname.machine}-{platform.processor()}"
        return DB.get_hash(platform_info)


    def get_saved_user(self):
        pc_hash = self.get_host_pc_hash()

        self.c.execute('''SELECT * FROM saved_users WHERE pc_hash=?''', (pc_hash,))

        saved_user = self.c.fetchone()
        if not saved_user: return None

        user_id = saved_user[1]

        self.c.execute('''SELECT * FROM user WHERE id=?''', (user_id,))

        user = self.c.fetchone()
        return (user[0], user[1])


    def get_user_id(self, username):
        self.c.execute('''SELECT * FROM user WHERE name=?''', (username,))
        user = self.c.fetchone()

        return (user is not None) and user[0]


    def register_user(self, username, password) -> int:
        self.c.execute('''INSERT INTO user(name, password_hash) VALUES (?, ?)''', (username, self.get_hash(password)))
        self.conn.commit()

        self.c.execute('''SELECT * FROM user WHERE name=?''', (username,))
        user = self.c.fetchone()
        return user[0]




    def save_user(self, user_id):
        pc_hash = self.get_host_pc_hash()
        self.c.execute('''SELECT * FROM saved_users WHERE pc_hash=?''', (pc_hash,))
        entry = self.c.fetchone()

        if entry:
            self.c.execute('''UPDATE saved_users SET user_id=? where pc_hash=?)''', (user_id, pc_hash))
        else:
            self.c.execute('''INSERT INTO saved_users(pc_hash, user_id) VALUES (?, ?)''', (pc_hash, user_id))
        self.conn.commit()

    def unsave_user(self):

        pc_hash = self.get_host_pc_hash()
        self.c.execute('''DELETE FROM saved_users WHERE pc_hash=?''', (pc_hash,))
        self.conn.commit()


    def username_match_password(self, username, password):
        self.c.execute('''SELECT * FROM user WHERE name=?''', (username,))
        user = self.c.fetchone()
        return user[2] == self.get_hash(password)







db = DB()
