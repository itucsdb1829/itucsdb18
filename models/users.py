from core.clients.db.client import db_client


class Users(object):

    def __init__(self, name, surname, email, password, role):
        self.name = name;
        self.surname = surname
        self.email = email
        self.password = password  # TODO: hash it
        self.role = role

        sql_fields = [
            'id SERIAL',
            'name CHAR(20)',
            'surname CHAR(20)',
            'email CHAR(40)',
            'password CHAR(16)',
            'role CHAR(20)'
        ]

        exp = '''CREATE TABLE IF NOT EXISTS {table_name} ({fields})'''.format(
            table_name=self.__class__.__name__.lower(),
            fields=','.join(sql_fields))

        db_client.query(exp)

    def create(self):
        exp = '''INSERT INTO {table_name} ({table_fields}) VALUES ({values})'''.format(
            table_name=self.__class__.__name__.lower(),
            table_fields=','.join([
                '{}'.format('name'),
                '{}'.format('surname'),
                '{}'.format('email'),
                '{}'.format('password'),
                '{}'.format('role')
            ]),
            values=','.join([
                "'{}'".format(self.name),
                "'{}'".format(self.surname),
                "'{}'".format(self.email),
                "'{}'".format(self.password),
                "'{}'".format(self.role)
            ])
        )
        db_client.query(exp)

    # def get(self, id=None, name=None, surname=None, email=None, password=None, role=None, limit=1):
    #
    # def get(self, **kwargs):
    #     query_params = dict()
    #     for key, value in kwargs.items():

    def update(self):
        pass

    def delete(self):
        pass
