from core.clients.db.client import db_client
from .base import BaseModel
from .users import Users
from .types import QueryList


class Questions(BaseModel):
    sql_fields = [
        'id SERIAL UNIQUE',
        'question_image TEXT NOT NULL',
        'answer_image TEXT',
        'choice CHAR',
        'course VARCHAR(20)',
        'subject VARCHAR(30)',
        'comment TEXT',
        'teacher INTEGER REFERENCES users(id) ON DELETE SET NULL'
    ]

    sql_field_number = len(sql_fields)

    def __init__(self, id=None, question_image=None, answer_image=None, choice=None, course=None,
                 subject=None, comment=None, teacher=None):

        self.id = id
        self.question_image = question_image
        self.answer_image = answer_image
        self.choice = choice
        self.course = course
        self.subject = subject
        self.comment = comment
        self.teacher = teacher
        if not teacher or type(teacher) != Users:
            self.teacher = Users.get(id=1)

        exp = '''CREATE TABLE IF NOT EXISTS {table_name} ({fields})'''.format(
            table_name=self.__class__.__name__.lower(),
            fields=','.join(self.sql_fields))

        db_client.query(exp)

    def save(self):
        if self.id:
            update_set = ','.join([
                "{key}=%s".format(key='question_image', value=self.question_image),
                "{key}=%s".format(key='answer_image', value=self.answer_image),
                "{key}=%s".format(key='choice', value=self.choice),
                "{key}=%s".format(key='course', value=self.course),
                "{key}=%s".format(key='subject', value=self.subject),
                "{key}=%s".format(key='comment', value=self.comment),
                "{key}=%s".format(key='teacher', value=self.teacher.id),
            ])
            exp = '''UPDATE {table_name} SET {values} WHERE id=%s RETURNING id'''.format(
                table_name=self.__class__.__name__.lower(),
                values=update_set,
            )
            self.id = db_client.fetch(exp, (self.question_image,
                                            self.answer_image,
                                            self.choice,
                                            self.course,
                                            self.subject,
                                            self.comment,
                                            self.teacher.id,
                                            self.id))[0][0]

        else:
            exp = '''INSERT INTO {table_name} ({table_fields}) VALUES ({values}) RETURNING id'''.format(
                table_name=self.__class__.__name__.lower(),
                table_fields=','.join([
                    '{}'.format('question_image'),
                    '{}'.format('answer_image'),
                    '{}'.format('choice'),
                    '{}'.format('course'),
                    '{}'.format('subject'),
                    '{}'.format('comment'),
                    '{}'.format('teacher'),
                ]),
                values=','.join(['%s', '%s', '%s', '%s', '%s', '%s', '%s'])
            )
            self.id = db_client.fetch(exp, (self.question_image,
                                            self.answer_image,
                                            self.choice,
                                            self.course,
                                            self.subject,
                                            self.comment,
                                            self.teacher.id))[0][0]
        return self

    @classmethod
    def filter(cls, **kwargs):
        params = ['TRUE']
        values = []

        for key, value in kwargs.items():
            params.append("{}.{}=%s".format(cls.__name__.lower(), key))
            values.append(value)

        exp = '''SELECT * FROM {table_name} JOIN users ON questions.teacher = users.id 
                 WHERE {filter}'''.format(
            table_name=cls.__name__.lower(),
            filter=' and '.join(params),
        )
        print(exp)
        rows = db_client.fetch(exp, values)
        objects = []
        for row in rows:
            t = Users(*row[cls.sql_field_number:])
            q = Questions(*row[:cls.sql_field_number])
            q.teacher=t
            objects.append(q)
        return QueryList(objects)
