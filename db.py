import os
import sqlite3
import time


class DatabaseManager(object):
    def __init__(self, db, schema_filename):
        self.conn = sqlite3.connect(db)
        if not os.path.exists(db):
            self.create_schema(schema_filename)
        self.conn.commit()
        self.cur = self.conn.cursor()

    def execute(self, arg):
        self.cur.execute(arg)
        self.conn.commit()
        return self.cur

    def execute(self, sql, args):
        self.cur.execute(sql, args)
        self.conn.commit
        return self.cur

    def create_schema(self, schema_filename):
        print('Creating schema')
        with open(schema_filename, 'rt') as f:
            schema = f.read()
            self.conn.executescript(schema)

    def __del__(self):
        self.conn.close()


def create_schema():
    db_filename = 'bigice.db'
    schema_filename = 'schema.sql'

    with sqlite3.connect(db_filename) as conn:
        print('Creating schema')
        with open(schema_filename, 'rt') as f:
            schema = f.read()
        conn.executescript(schema)


def insert_text_message(db_filename, msg):
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        insert_message = "insert into message (msg_type,from_user_name,to_user_name,content,timestamp)\
 values(:msg_type,:from_user_name,:to_user_name,:content,:timestamp)"
        cursor.execute(insert_message, {
            'msg_type': msg['MsgType'],
            'from_user_name': msg['FromUserName'],
            'to_user_name': msg['ToUserName'],
            'content': msg['Text'],
            'timestamp': time.time()})


if __name__ == "__main__":
    create_schema()
