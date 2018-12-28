Database Design
===============


    .. figure:: ../media/db_diagram.png
        :scale: 50 %
        :alt: map to buried treasure

   Database E/R Diagmram


**Database Structure**

Question Collector is built on a PostgreSQL database with three main tables; Users,
Questions and Feedbacks.

In this platform, there are three different user role stored in "role" column in users table.
Role choices are admin, reviewer and teacher. Permissions are given related by this field. Users
table also has different columns to identify the user and store necessary data.

Questions table stores necessary data about questions in the platform. "question_image' and "answer_image"
stores link of the images. Unfortunately current version of the Question Collector does not
support the file upload. For this version users have to enter link of the images. "teacher" field
is foreign key to id of the users table with **"ON DELETE SET NULL"** property.

Feedbacks table stores necessary data about feedbacks given by reviewers. Admins make a decision
about the convenience of the question by evaluating the feedbacks. This table has field to
identify a feedback. "quality_rate" and "difficulty_rate" fields store points given
by reviewer. "is_proper" is a boolean field to store final decision of the reviewer. "reviewer"
field is foreign key to id of the user table with **"ON DELETE SET NULL"** property. "question" field
is foreign key to id of the questions table with **"ON DELETE CASCADE"** property


**Database Client**

.. code-block:: python

    //core/clients/db/client.py
    import os

    import psycopg2 as db


    class Client(object):

        def __init__(self):
            self.dsn = os.getenv('DATABASE_URL')
            self.connection = db.connect(self.dsn)
            self.cursor = self.connection.cursor()

        def query(self, statement, params=None):
            try:
                self.cursor.execute(statement, params)
                self.connection.commit()
            except:
                self.connection.rollback()
                raise

        def fetch(self, statement, params=None):
            try:
                self.cursor.execute(statement, params)
                self.connection.commit()
                return self.cursor.fetchall()
            except:
                self.connection.rollback()
                raise

        def __del__(self):
            self.connection.close()
            self.cursor.close()


    db_client = Client()


This database has a client that does database operations. Aim of the client is providing uniformity
if the database or database adapter changes. In the project, *db_client* used as a singleton object.

