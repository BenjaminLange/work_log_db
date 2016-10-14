import datetime
import os
import sys

from peewee import *


DATABASE = 'work_log.db'

db = SqliteDatabase(DATABASE)


class Entry(Model):
    employee_name = CharField(max_length=255)
    task_name = CharField(max_length=255)
    date = DateTimeField(default=datetime.datetime.now)
    time_spent = IntegerField(default=0)
    notes = TextField()

    class Meta:
        database = db


def initialize():
    db.connect()
    db.create_tables([Entry], safe=True)


def main_menu():
    choice = None
    while choice != 'q':
        clear()
        print('What would you like to do?')
        print('A: add entry (Default)')
        print('s: search')
        print('q: quit')
        choice = input('> ').lower().strip()
        if choice != 'q':
            if choice == 's':
                search_menu()
            else:
                add_entry()


def search_menu():
    clear()
    print('How would you like to search?')
    print('D: date (Default)')
    print('t: time spent')
    print('s: exact string')
    print('n: name')
    choice = input('> ').lower().strip()
    if choice == 't':
        search_by_time_spent()
    elif choice == 's':
        search_by_string()
    elif choice == 'n':
        search_by_name()
    else:
        search_by_date()


def add_entry():
    print('Please enter the task details')
    employee_name = input('Your name: ')
    task_name = input('Task Name: ')
    while True:
        time_spent = input('Minutes spent: ')
        try:
            time_spent = int(time_spent)
            break
        except ValueError:
            print('Time must be entered in numbers')
    add_notes = input('Add notes? Y/n ')
    notes = None
    if add_notes != 'n':
        notes_list = []
        print("Enter notes here. Press enter on a blank line to save.")
        while notes != '':
            notes = input('> ')
            notes_list.append(notes)
    Entry.create(employee_name=employee_name,
                 task_name=task_name,
                 time_spent=time_spent,
                 notes=notes)


def search_by_time_spent():
    pass


def search_by_string():
    pass


def search_by_name():
    pass


def search_by_date():
    pass


def display_entry():
    pass


def display_entries():
    pass


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    initialize()
    main_menu()
