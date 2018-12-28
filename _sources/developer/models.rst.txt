Models
======

**Base Model**

The project has simple Object Relational Mapper to make implementation easier. *BaseModel* is
underlying structure of the simple ORM's.

 .. code-block:: python


    #models/base.py

    class BaseModel(object):

        sql_field_number = 0

        def save(self):
            pass

        def update(self, **kwargs):
            set_params = []
            set_values = []

            if 'password' in kwargs:
                kwargs['password'] = generate_password_hash(kwargs['password'])

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

This model has some methods for CRUD operations. Some of them are overrided while using other models.
These methods fetches or creates necessary data and do necessary database operations using *db_client*.



**Users Model**

This model represents user structure of Question Collector. Model is inherited from *BaseModel* and
overrided some methods to do special operations.

.. code-block:: python


    #models/users.py
    class Users(BaseModel):
        sql_fields = [
            'id SERIAL UNIQUE',
            'name VARCHAR(20)',
            'surname VARCHAR(20)',
            'email VARCHAR(40) UNIQUE',
            'phone_number VARCHAR(12) UNIQUE',
            'password text',
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


Save method is not defined in *BaseModel* because of the difference of the table field so it is
defined in user model. This model also has two special methods called *set_password()*
and *check_password()*.


**Questions Model**

This model represents question structure of Question Collector. Model is inherited from *BaseModel* and
overrided some methods to do special operations.

.. code-block:: python


    #models/questions.py
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
        if not teacher:
            teacher_id=1
        if type(teacher) != Users:
            teacher_id=teacher

        self.teacher = Users.get(id=teacher_id)

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

    def get_feedbacks(self):
        exp = '''SELECT comment, quality_rate, difficulty_rate, is_proper, created_at, users.name, users.surname
                FROM feedbacks JOIN users ON feedbacks.reviewer = users.id WHERE question=%s'''

        rows = db_client.fetch(exp, (self.id,))
        r = []
        for row in rows:
            d = {}
            d['comment'] = row[0]
            d['quality_rate'] = int(row[1])
            d['difficulty_rate'] = int(row[2])
            d['is_proper'] = row[3]
            d['created_at'] = row[4].isoformat()
            d['reviewer'] = '{} {}'.format(row[5], row[6])
            r.append(d)

        return r

    @classmethod
    def filter(cls, **kwargs):
        params = ['TRUE']
        values = []

        for key, value in kwargs.items():
            params.append("{}.{}=%s".format(cls.__name__.lower(), key))
            values.append(value)

        exp = '''SELECT * FROM {table_name} JOIN users ON questions.teacher = users.id
                 WHERE {filter} ORDER BY questions.id DESC '''.format(
            table_name=cls.__name__.lower(),
            filter=' and '.join(params),
        )

        rows = db_client.fetch(exp, values)
        objects = []
        for row in rows:
            t = Users(*row[cls.sql_field_number:])
            q = Questions(*row[:cls.sql_field_number])
            q.teacher=t
            objects.append(q)
        return QueryList(objects)



Save method is not defined in *BaseModel* because of the difference of the table field so it is
defined in question model. Filter method is also overrided in question model. This model also has
a special methodscalled *get_feedbacks()

***Feedbacks Model**

This model represents question structure of Question Collector. Model is inherited from *BaseModel* and
overrided some methods to do special operations.

.. code-block:: python


    #models/feedbacks.py
    class FeedBacks(BaseModel):
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

    sql_field_number = len(sql_fields)

    def __init__(self, id=None, question=Questions(), comment=None, quality_rate=None, difficulty_rate=None,
                 is_proper=None,
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

        exp = '''CREATE TABLE IF NOT EXISTS {table_name} ({fields})'''.format(
            table_name=self.__class__.__name__.lower(),
            fields=','.join(self.sql_fields))

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
            query = db_client.fetch(exp, (self.comment,
                                          self.quality_rate,
                                          self.difficulty_rate,
                                          self.is_proper,
                                          self.reviewer.id,
                                          self.id))
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

            self.id, self.created_at = db_client.fetch(exp, (self.comment,
                                                             self.question.id,
                                                             self.quality_rate,
                                                             self.difficulty_rate,
                                                             self.is_proper,
                                                             self.reviewer.id))[0]
        return self

    @classmethod
    def filter(cls, **kwargs):
        params = ['TRUE']
        values = []

        for key, value in kwargs.items():
            params.append("{}.{}=%s".format(cls.__name__.lower(), key))
            values.append(value)

        exp = '''SELECT * FROM {table_name} FULL JOIN users ON feedbacks.reviewer = users.id
                    JOIN questions ON feedbacks.question=questions.id
                    WHERE {filter} ORDER BY feedbacks.id DESC'''.format(
            table_name=cls.__name__.lower(),
            filter=' and '.join(params),
        )
        rows = db_client.fetch(exp, values)
        objects = []
        for row in rows:
            t = Users(*row[cls.sql_field_number:cls.sql_field_number + Users.sql_field_number])
            q = Questions(*row[cls.sql_field_number + Users.sql_field_number:])
            q.teacher = Users.get(id=q.teacher.id)
            fb = FeedBacks(*row[:cls.sql_field_number])
            fb.quality_rate = int(fb.quality_rate)
            fb.difficulty_rate = int(fb.quality_rate)
            fb.reviewer = t
            fb.question = q
            objects.append(fb)
        return QueryList(objects)




Save method is not defined in *BaseModel* because of the difference of the table field so it is
defined in feedback model. Filter method is also overrided in feedback model.