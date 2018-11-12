# import os
#
# import psycopg2 as db
#
# from core.clients.db.client import db_client
#
# import psycopg2 as dbapi2
#
#
# class BaseModel:
#
#     def __init__(self, **kwargs):
#         for key in kwargs:
#             self.__setattr__(key, kwargs.get(key))
#
#
#         exp = '''CREATE TABLE IF NOT EXISTS {table_name} (NUM INTEGER)'''.format(
#             table_name=self.__class__.__name__.lower())
#
#         db_client.query(exp)
#
#     def create(self, **kwargs):
#
#
#
#     def get(self):
#         pass
#
#     def update(self):
#         pass
#
#     def delete(self):
#         pass
