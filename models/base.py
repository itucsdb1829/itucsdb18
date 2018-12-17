from core.clients.db.client import db_client
from .types import QueryList


class BaseModel(object):

    sql_field_number = 0

    def save(self):
        pass

    def update(self, **kwargs):
        set_params = []
        set_values = []

        for key, value in kwargs.items():
            set_params.append("{}=%s".format(key))
            set_values.append(value)

        exp = '''UPDATE {table_name} SET {filter} WHERE id=%s'''.format(
            table_name=self.__class__.__name__.lower(),
            filter=','.join(set_params),
        )
        set_values.append(self.id)
        db_client.query(exp, set_values)
        self.__dict__.update(**kwargs)
        return self

    def delete(self):
        if not self.id:
            return None

        exp = '''DELETE FROM {table_name} WHERE id=%s RETURNING id'''.format(
            table_name=self.__class__.__name__.lower(),
        )
        id = self.id
        self.id = None

        return db_client.fetch(exp, [id])[0][0]

    @classmethod
    def filter(cls, **kwargs):
        params = ['TRUE']
        values = []

        for key, value in kwargs.items():
            params.append("{}=%s".format(key))
            values.append(value)

        exp = '''SELECT * FROM {table_name} WHERE {filter} ORDER BY id ASC'''.format(
            table_name=cls.__name__.lower(),
            filter=' and '.join(params),
        )

        rows = db_client.fetch(exp, values)
        objects = [cls(*row) for row in rows]

        return QueryList(objects)

    @classmethod
    def get(cls, **kwargs):
        return cls.filter(**kwargs).first()

    @classmethod
    def create(cls, **kwargs):
        obj = cls(**kwargs)
        obj.save()
        return obj
