import os

import psycopg2 as db


class Client(object):

    def __init__(self):
        self.dsn = os.getenv('DATABASE_URL')
        self.connection = db.connect(self.dsn)
        self.cursor = self.connection.cursor()

    def query(self, statement):
        self.cursor.execute(statement)
        self.connection.commit()

    def __del__(self):
        self.connection.close()
        self.cursor.close()


db_client = Client()
