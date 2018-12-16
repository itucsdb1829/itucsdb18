from core.clients.db.client import db_client
from .base import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash


class Users(BaseModel):
    sql_fields = [
        'id SERIAL UNIQUE',
        'name VARCHAR(20)',
        'surname VARCHAR(20)',
        'email VARCHAR(40) UNIQUE',
        'phone_number VARCHAR(12) UNIQUE',
        'password bytea',
        'role VARCHAR(20)',
        'iban VARCHAR(24)'
    ]

    sql_field_number = len(sql_fields)

    def __init__(self, id=None, name=None, surname=None, email=None, phone_number=None, password=None, role=None,
                 iban=None):
        self.id = id
        self.name = name
        self.surname = surname
        self.email = email
        self.phone_number = phone_number
        self.password = password
        self.role = role
        self.iban = iban

        exp = '''CREATE TABLE IF NOT EXISTS {table_name} ({fields})'''.format(
            table_name=self.__class__.__name__.lower(),
            fields=','.join(self.sql_fields))

        db_client.query(exp)

    def save(self):
        if self.id:
            update_set = ','.join([
                "{key}=%s".format(key='name'),
                "{key}=%s".format(key='surname'),
                "{key}=%s".format(key='email'),
                "{key}=%s".format(key='phone_number'),
                "{key}=%s".format(key='password'),
                "{key}=%s".format(key='role'),
                "{key}=%s".format(key='iban'),
            ])
            exp = '''UPDATE {table_name} SET {values} WHERE id=%s RETURNING id'''.format(
                table_name=self.__class__.__name__.lower(),
                values=update_set,
            )
            self.id = db_client.fetch(exp, (self.name,
                                            self.surname,
                                            self.email,
                                            self.phone_number,
                                            self.password,
                                            self.role,
                                            self.iban,
                                            self.id))[0][0]
        else:
            self.password = generate_password_hash(self.password)
            exp = '''INSERT INTO {table_name} ({table_fields}) VALUES ({values}) RETURNING id'''.format(
                table_name=self.__class__.__name__.lower(),
                table_fields=','.join([
                    '{}'.format('name'),
                    '{}'.format('surname'),
                    '{}'.format('email'),
                    '{}'.format('phone_number'),
                    '{}'.format('password'),
                    '{}'.format('role'),
                    '{}'.format('iban'),
                ]),
                values=','.join(['%s', '%s', '%s', '%s', '%s', '%s', '%s'])
            )
            print(exp)
            self.id = db_client.fetch(exp, (self.name,
                                            self.surname,
                                            self.email,
                                            self.phone_number,
                                            self.password,
                                            self.role,
                                            self.iban))[0][0]
        return self

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)
        self.save()
