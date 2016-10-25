import unittest

from peewee import *
from work_log_db import Entry


DATABASE = 'work_log_test.db'
db = SqliteDatabase(DATABASE)


class WorkLogDBTests(unittest.TestCase):
    def setUp(self):
        db.connect()
        db.create_tables([Entry], safe=True)

    def test_can_create_entry(self):
        test_entry = Entry.create(
            employee_name='John Smith',
            task_name='Test Task',
            time_spent=20,
            notes='Test Notes'
        )
        self.assertEqual(test_entry.employee_name, 'John Smith')
        self.assertEqual(test_entry.task_name, 'Test Task')
        self.assertEqual(test_entry.time_spent, 20)
        self.assertEqual(test_entry.notes, 'Test Notes')


if __name__ == '__main__':
    unittest.main()
