from datetime import datetime

from elasticsearch_dsl import Date, DocType, Integer, Keyword, Text
from elasticsearch_dsl.connections import connections

# Define a default Elasticsearch client
connections.create_connection(hosts=['localhost'])


class Message(DocType):
    from_user_name = Text()
    to_user_name = Text()
    content = Text()
    timestamp = Date()

    class Meta:
        index = 'bigice'

    def save(self, ** kwargs):
        return super(Message, self).save(** kwargs)

    def is_published(self):
        return datetime.now() > self.timestamp

    def __str__(self):
        return 'from_user_name:{}\n to_user_name:{}\n content:{}\n\
        timestamp:{}\n'.format(self.from_user_name, self.to_user_name, self.content, self.timestamp)


print(connections.get_connection().cluster.health())
