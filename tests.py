import os
import unittest
from unittest.mock import patch
from test import support

from work_log_db import WorkLog
from models import *


DATABASE = 'work_log_test.db'
db = SqliteDatabase(DATABASE)


class WorkLogDBTests(unittest.TestCase):
    def setUp(self):
        self.test_log = WorkLog()
        db.connect()
        db.create_tables([Entry], safe=True)
        self.search = {
            'main_menu': (generate for generate in ['s', 'q']),
            'minutes': (generate for generate in ['a', '20'])
        }
        self.add = {
            'main_menu': (generate for generate in ['a', 'q']),
            'time_spent': (generate for generate in ['a', '20'])
        }
        self.delete = (generate for generate in ['d', 'q'])
        self.search_by_date = (generate for generate in ['123', '11/04/16'])
        self.edit = (generate for generate in ['e', 'q'])

    def tearDown(self):
        db.close()
        if os.path.isfile(DATABASE):
            os.remove(DATABASE)

    def mock_input(self, prompt):
        if 'Date, time, string, or name' in prompt:
            return 't'
        elif 'Add, search, or quit' in prompt:
            return 'q'
        elif 'Your name' in prompt:
            return 'Ben'
        elif 'Task name' in prompt:
            return 'Test Task'
        elif 'Minutes spent' in prompt:
            return '20'
        elif 'Add notes?' in prompt:
            return 'n'
        elif '> ' in prompt:
            return 'Notes\n\n'
        elif 'How many minutes?' in prompt:
            return '20'
        elif 'What would you like to search for?' in prompt:
            return 'Test'
        elif 'Who would you like to search for?' in prompt:
            return 'Ben'
        elif 'Press enter to' in prompt:
            return '\n'
        elif 'Next, previous, edit, delete, quit' in prompt:
            return 'q'

    @patch('builtins.input', return_value='q')
    def test_can_return_to_main_menu_from_search_menu(self, input):
        with support.captured_stdout() as stdout:
            with self.assertRaises(SystemExit):
                self.test_log.search_menu()
        search_string = stdout.getvalue()
        self.assertIn('What would you like to do', search_string)

    def mock_add_entry(self, prompt):
        if 'Add, search, or quit' in prompt:
            return next(self.add['main_menu'])
        elif 'Your name' in prompt:
            return 'Ben'
        elif 'Task name' in prompt:
            return 'Test Task'
        elif 'Minutes spent' in prompt:
            return next(self.add['time_spent'])
        elif 'Add notes?' in prompt:
            return 'y'
        elif 'Notes:' in prompt:
            return ''

    def test_can_add_entry(self):
        with patch('builtins.input', self.mock_add_entry):
            with support.captured_stdout() as stdout:
                with self.assertRaises(SystemExit):
                    self.test_log.main_menu()
        search_string = stdout.getvalue()
        entry = Entry.get(id=1)
        self.assertIn('Time must be entered in numbers', search_string)
        self.assertEqual(entry.task_name, 'Test Task')
        self.assertEqual(entry.employee_name, 'Ben')
        self.assertEqual(entry.time_spent, 20)

    def mock_search_string(self, prompt):
        if 'Add, search, or quit' in prompt:
            return 'q'
        elif 'Date, time, string, or name' in prompt:
            return 's'
        elif 'What would you like to search for?' in prompt:
            return 'Test'
        elif 'Next, previous, edit, delete, quit' in prompt:
            return 'q'

    def test_can_search_by_string(self):
        test_entry = Entry.create(
            employee_name='John Smith',
            task_name='Test Task',
            time_spent=20,
            notes='Test Notes'
        )
        with patch('builtins.input', self.mock_search_string):
            with support.captured_stdout() as stdout:
                with self.assertRaises(SystemExit):
                    self.test_log.search_menu()
        search_string = stdout.getvalue()
        self.assertIn('Test Task', search_string)

    def mock_search_not_found_name(self, prompt):
        if 'Add, search, or quit' in prompt:
            return 'q'
        elif 'Date, time, string, or name' in prompt:
            return 'n'
        elif 'Who would you like to search for?' in prompt:
            return 'John Doe'
        elif 'Next, previous, edit, delete, quit' in prompt:
            return 'q'

    def test_no_results_displays_error(self):
        with patch('builtins.input', self.mock_search_not_found_name):
            with support.captured_stdout() as stdout:
                with self.assertRaises(SystemExit):
                    self.test_log.search_menu()
        search_string = stdout.getvalue()
        self.assertIn('No results were found', search_string)

    def mock_search_name(self, prompt):
        if 'Add, search, or quit' in prompt:
            return 'q'
        elif 'Date, time, string, or name' in prompt:
            return 'n'
        elif 'Who would you like to search for?' in prompt:
            return 'John Smith'
        elif 'Next, previous, edit, delete, quit' in prompt:
            return 'q'

    def test_can_search_by_name(self):
        test_entry = Entry.create(
            employee_name='John Smith',
            task_name='Test Task',
            time_spent=20,
            notes='Test Notes'
        )
        with patch('builtins.input', self.mock_search_name):
            with support.captured_stdout() as stdout:
                with self.assertRaises(SystemExit):
                    self.test_log.search_menu()
        search_string = stdout.getvalue()
        self.assertIn('John Smith', search_string)

    def mock_display(self, prompt):
        if 'Date, time, string, or name' in prompt:
            return 't'
        elif 'Add, search, or quit' in prompt:
            return next(self.search['main_menu'])
        elif 'How many minutes?' in prompt:
            return next(self.search['minutes'])
        elif 'Next, previous, edit, delete, quit' in prompt:
            return 'q'

    def test_can_display_entry(self):
        test_entry = Entry.create(
            employee_name='John Smith',
            task_name='Test Task',
            time_spent=20,
            notes='Test Notes'
        )
        with patch('builtins.input', self.mock_display):
            with support.captured_stdout() as stdout:
                with self.assertRaises(SystemExit):
                    self.test_log.main_menu()
        search_string = stdout.getvalue()
        self.assertIn('Test Task', search_string)
        self.assertIn('Please enter numbers only', search_string)

    def mock_delete(self, prompt):
        if 'Date, time, string, or name' in prompt:
            return 't'
        elif 'Add, search, or quit' in prompt:
            return 'q'
        elif 'How many minutes?' in prompt:
            return '44'
        elif 'Next, previous, edit, delete, quit' in prompt:
            return next(self.delete)
        elif 'Press enter to continue' in prompt:
            return '\n'

    def test_can_delete_entry(self):
        test_entry = Entry.create(
            employee_name='John Smith',
            task_name='Test Task',
            time_spent=44,
            notes='Test Notes'
        )
        with patch('builtins.input', self.mock_delete):
            with support.captured_stdout() as stdout:
                with self.assertRaises(SystemExit):
                    self.test_log.search_menu()
        search_string = stdout.getvalue()
        self.assertIn('Entry deleted', search_string)

    def mock_search_by_date(self, prompt):
        if 'Date, time, string, or name' in prompt:
            return 'd'
        elif 'Add, search, or quit' in prompt:
            return next(self.search['main_menu'])
        elif 'Next, previous, edit, delete, quit' in prompt:
            return 'q'
        elif 'Date: ' in prompt:
            return next(self.search_by_date)

    def test_can_search_by_date(self):
        test_entry = Entry.create(
            employee_name='John Smith',
            task_name='Test Task Search Date',
            time_spent=20,
            notes='Test Notes',
            date='2016-11-04'
        )
        with patch('builtins.input', self.mock_search_by_date):
            with support.captured_stdout() as stdout:
                with self.assertRaises(SystemExit):
                    self.test_log.main_menu()
        search_string = stdout.getvalue()
        self.assertIn('Test Task Search Date', search_string)
        self.assertIn("I don't recognize that format", search_string)

    def mock_search_by_date_range(self, prompt):
        if 'Date, time, string, or name' in prompt:
            return 'd'
        elif 'Add, search, or quit' in prompt:
            return 'q'
        elif 'Next, previous, edit, delete, quit' in prompt:
            return 'q'
        elif 'Date: ' in prompt:
            return '11/01/16 - 11/03/16'

    def test_can_search_by_date_range(self):
        test_entry = Entry.create(
            employee_name='John Smith',
            task_name='Test Task Search Date Range',
            time_spent=20,
            notes='Test Notes',
            date='2016-11-02'
        )
        with patch('builtins.input', self.mock_search_by_date_range):
            with support.captured_stdout() as stdout:
                with self.assertRaises(SystemExit):
                    self.test_log.search_by_date()
        search_string = stdout.getvalue()
        self.assertIn('Test Task Search Date Range', search_string)

    def mock_edit_entry(self, prompt):
        if 'Date, time, string, or name' in prompt:
            return 't'
        elif 'Add, search, or quit' in prompt:
            return 'q'
        elif 'How many minutes?' in prompt:
            return '3'
        elif 'Next, previous, edit, delete, quit' in prompt:
            return next(self.edit)
        elif 'Employee Name' in prompt:
            return ''
        elif 'Task Name' in prompt:
            return 'Test Edit (Updated)'
        elif 'Date' in prompt:
            return ''
        elif 'Time' in prompt:
            return ''
        elif 'Notes' in prompt:
            return ''

    def test_can_edit_entry(self):
        test_entry = Entry.create(
            employee_name='John Smith',
            task_name='Test Edit',
            time_spent=3,
            notes='Test Notes',
            date='2016-11-11'
        )
        with patch('builtins.input', self.mock_edit_entry):
            with support.captured_stdout() as stdout:
                with self.assertRaises(SystemExit):
                    self.test_log.search_by_time_spent()
        search_string = stdout.getvalue()
        self.assertIn('Test Edit (Updated)', search_string)

    def test_can_show_search_menu(self):
        with patch('builtins.input', self.mock_input):
            with support.captured_stdout() as stdout:
                with self.assertRaises(SystemExit):
                    self.test_log.search_menu()
        search_string = stdout.getvalue()
        self.assertIn('How would you like to search?', search_string)
        self.assertIn('D: date (Default)', search_string)
        self.assertIn('t: time spent', search_string)
        self.assertIn('s: exact string', search_string)
        self.assertIn('n: name', search_string)

    def test_main_menu(self):
        with patch('builtins.input', self.mock_input):
            with support.captured_stdout() as stdout:
                with self.assertRaises(SystemExit):
                    self.test_log.main_menu()
        search_string = stdout.getvalue()
        self.assertIn('What would you like to do?', search_string)
        self.assertIn('A: add entry (Default)', search_string)
        self.assertIn('s: search', search_string)
        self.assertIn('q: quit', search_string)

if __name__ == '__main__':
    unittest.main()
