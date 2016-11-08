import datetime

from peewee import *

DATABASE = 'work_log.db'
db = SqliteDatabase(DATABASE)


class Entry(Model):
    employee_name = CharField(max_length=255)
    task_name = CharField(max_length=255)
    date = DateField(default=datetime.date.today)
    time_spent = IntegerField(default=0)
    notes = TextField()

    class Meta:
        database = db


def initialize():
    db.connect()
    db.create_tables([Entry], safe=True)
