import os
import sqlite3
import time

DB_FILENAME = 'bigice.db'
SCHEMA_FILENAME = 'schema.sql'


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
    # db_filename = 'bigice.db'
    # schema_filename = 'schema.sql'

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


def query_all_messages(db_filename=DB_FILENAME):
    results = []
    with sqlite3.connect(db_filename) as conn:
        # Change the row factory to use Row
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
        select id, from_user_name, to_user_name,content,timestamp 
        from message order by timestamp
        """)

        print('\nall message:')
        for row in cursor.fetchall():
            result = dict()
            result['id'] = row['id']
            result['from_user_name'] = row['from_user_name']
            result['to_user_name'] = row['content']
            result['timestamp'] = row['timestamp']
            result['content'] = row['content']
            results.append(result)
        return results


def query_ten_messages(db_filename):
    results = []
    with sqlite3.connect(db_filename) as conn:
        # Change the row factory to use Row
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
        select id, from_user_name, to_user_name,content,timestamp 
        from message order by timestamp
        """)

        print('\nten messages:')
        for row in cursor.fetchmany(10):
            result = dict()
            result['id'] = row['id']
            result['from_user_name'] = row['from_user_name']
            result['to_user_name'] = row['to_user_name']
            result['timestamp'] = row['timestamp']
            result['content'] = row['content']
            results.append(result)
        return results


if __name__ == "__main__":
    create_schema()
