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
        clear_screen()
        print('What would you like to do?')
        print('A: add entry (Default)')
        print('s: search')
        print('q: quit')
        choice = input('> ').lower().strip()
        if choice == 'q':
            sys.exit()
        elif choice == 's':
            search_menu()
        else:
            add_entry()


def search_menu():
    clear_screen()
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
    search = input('How many minutes? ')
    entries = None
    try:
        entries = Entry.select().where(Entry.time_spent == int(search))
    except ValueError:
        print('Please enter numbers only!!')
        return search_by_time_spent()
    display_entries(entries)


def search_by_string():
    search = input('What would you like to search for? ')
    entries = Entry.select().where(Entry.task_name.contains(search) or
                                   Entry.notes.contains(search))
    display_entries(entries)


def search_by_name():
    search = input('Who would you like to search for? ')
    entries = Entry.select().where(Entry.employee_name.contains(search))
    display_entries(entries)


def search_by_date():
    pass


def display_entry(entry):
    """Print a single entry to the screen"""
    border = '-' * 50
    print(border)
    print(entry.employee_name)
    print("Date: {}".format(entry.date))
    print("Time Spent: {}".format(entry.time_spent))
    if entry.notes != '':
        print("Notes:\n{}\n{}".format('----------', entry.notes))
    print(border)


def display_entries(entries):
    """Prints a list of log entries and allows paging through each entry
    individually. Also allows picking an entry for editing or deletion."""
    if len(entries) == 0:
        print("\nNo results were found.\n")
        input("Press enter to return to the main menu...")
        main_menu()
    counter = 0
    error = None
    while True:
        clear_screen()
        if len(entries) == 0:
            print("There are no more entries!")
            input("Press enter to return to the main menu...")
            main_menu()
        if error:
            print(error)
            input("Press enter to continue...")
            clear_screen()
            error = None
        display_entry(entries[counter])
        print("\nWhat would you like to do?")
        print("  n: Next entry (Default)")
        print("  p: Previous entry")
        print("  e: Edit entry")
        print("  d: Delete entry")
        print("  q: Quit to main menu")
        user_input = input("> ").lower()
        if user_input == 'q':
            main_menu()
        elif user_input == 'p':
            if counter <= 0:
                error = "End of list. Can't go back."
                continue
            counter -= 1
        elif user_input == 'd':
            delete_entry(entries[counter]['id'])
            del entries[counter]
            if counter > len(entries) - 1:
                counter -= 1
        elif user_input == 'e':
            edit_entry(entries[counter])
        else:
            counter += 1
            if counter > len(entries) - 1:
                counter -= 1
                error = "End of list. Can't move forward."


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    initialize()
    main_menu()
