import flask
from db import query_all_messages

db_filename = 'bigice.db'
query_all_messages(db_filename)
