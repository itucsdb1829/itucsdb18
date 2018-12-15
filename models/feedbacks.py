from core.clients.db.client import db_client
from .base import BaseModel
from .users import Users
from .questions import Questions


class FeedBacks(BaseModel):

    def __init__(self, id=None, question=Questions(), comment=None, quality_rate=None, difficulty_rate=None, is_proper=None,
                 created_at=None, reviewer=Users()):
        self.id = id
        self.question = question
        self.comment = comment
        self.quality_rate = quality_rate
        self.difficulty_rate = difficulty_rate
        self.is_proper = is_proper
        self.created_at = created_at
        self.reviewer = reviewer

        if not type(question) == Questions:
            self.question = Questions.get(id=question)

        if not type(reviewer) == Users:
            self.reviewer = Users.get(id=reviewer)

        sql_fields = [
            'id SERIAL UNIQUE',
            'question INTEGER REFERENCES questions(id) ON DELETE CASCADE',
            'comment TEXT',
            'quality_rate NUMERIC',
            'difficulty_rate NUMERIC',
            'is_proper BOOLEAN DEFAULT FALSE',
            'created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP',
            'reviewer INTEGER REFERENCES users(id) ON DELETE SET NULL',
        ]

        self.foreign_keys=[
            'question',
            'reviewer'
        ]

        self.sql_field_number = len(sql_fields)

        exp = '''CREATE TABLE IF NOT EXISTS {table_name} ({fields})'''.format(
            table_name=self.__class__.__name__.lower(),
            fields=','.join(sql_fields))

        db_client.query(exp)

    def save(self):
        if self.id:
            update_set = ','.join([
                "{key}=%s".format(key='comment'),
                "{key}=%s".format(key='quality_rate'),
                "{key}=%s".format(key='difficulty_rate'),
                "{key}=%s".format(key='is_proper'),
                "{key}=%s".format(key='reviewer'),
            ])
            exp = '''UPDATE {table_name} SET {values} WHERE id=%s RETURNING id, created_at'''.format(
                table_name=self.__class__.__name__.lower(),
                values=update_set,
            )
            query = db_client.fetch(exp, (self.id,))
            self.id = query[0][0]
            self.created_at = query[0][1]
        else:
            exp = '''INSERT INTO {table_name} ({table_fields}) VALUES ({values}) RETURNING id, created_at'''.format(
                table_name=self.__class__.__name__.lower(),
                table_fields=','.join([
                    '{}'.format('comment'),
                    '{}'.format('question'),
                    '{}'.format('quality_rate'),
                    '{}'.format('difficulty_rate'),
                    '{}'.format('is_proper'),
                    '{}'.format('reviewer'),
                ]),
                values=','.join(['%s', '%s', '%s', '%s', '%s', '%s'])
            )
            print(exp)
            self.id, self.created_at = db_client.fetch(exp, (self.comment,
                                                             self.question.id,
                                                             self.quality_rate,
                                                             self.difficulty_rate,
                                                             self.is_proper,
                                                             self.reviewer.id))[0]
        return self
