import os
import re
import sys

from datetime import datetime

from models import *


class WorkLog:
    def main_menu(self):
        choice = None
        while choice != 'q':
            self.clear_screen()
            print('What would you like to do?')
            print('A: add entry (Default)')
            print('s: search')
            print('q: quit')
            choice = input('Add, search, or quit: ').lower().strip()
            if choice == 'q':
                sys.exit()
            elif choice == 's':
                self.search_menu()
            else:
                self.add_entry()

    def search_menu(self):
        self.clear_screen()
        print('How would you like to search?')
        print('D: date (Default)')
        print('t: time spent')
        print('s: exact string')
        print('n: name')
        choice = input('Date, time, string, or name: ')
        if choice == 't':
            self.search_by_time_spent()
        elif choice == 's':
            self.search_by_string()
        elif choice == 'n':
            self.search_by_name()
        elif choice == 'q':
            self.main_menu()
        else:
            self.search_by_date()

    def add_entry(self):
        print('Please enter the task details')
        employee_name = input('Your name: ')
        task_name = input('Task name: ')
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
            notes = 'A'
            while notes != '':
                notes = input('Notes: ')
                notes_list.append(notes.replace('\\n', '\n'))
            notes = '\n'.join(notes_list)
        Entry.create(employee_name=employee_name,
                     task_name=task_name,
                     time_spent=time_spent,
                     notes=notes)

    def search_by_time_spent(self):
        search = input('How many minutes? ')
        entries = None
        try:
            entries = Entry.select().where(Entry.time_spent == int(search))
        except ValueError:
            print('Please enter numbers only!!')
            return self.search_by_time_spent()
        self.display_entries(entries)

    def search_by_string(self):
        search = input('What would you like to search for? ')
        entries = Entry.select().where(Entry.task_name.contains(search) or
                                       Entry.notes.contains(search))
        self.display_entries(entries)

    def search_by_name(self):
        search = input('Who would you like to search for? ')
        entries = Entry.select().where(Entry.employee_name.contains(search))
        names = []
        for entry in entries:
            if entry.employee_name not in names:
                names.append(entry.employee_name)
        if len(names) > 1:
            print('There are multiple people with that name. Please be more specific!!')
            for name in names:
                print(name)
            return self.search_by_name()
        self.display_entries(entries)

    def search_by_date(self, error=None):
        self.clear_screen()
        fmt_month_day_year = '%m/%d/%y'
        if error:
            print(error)
        print("Please enter a date to search for (MM/DD/YY).")
        print("You may also search a date range using MM/DD/YY - MM/DD/YY")
        user_input = input("Date: ")
        date_range = re.compile(r'\d\d/\d\d/\d\d - \d\d/\d\d/\d\d')
        date = re.compile(r'\d\d/\d\d/\d\d')
        if date_range.search(user_input):
            date_list = user_input.split('-')
            start_date = datetime.datetime.strptime(
                date_list[0].strip(), fmt_month_day_year).date()
            end_date = datetime.datetime.strptime(
                date_list[1].strip(), fmt_month_day_year).date()
            entries = Entry.select().where(Entry.date >= start_date and Entry.date <= end_date)
            self.display_entries(entries)
        elif date.search(user_input):
            search_date = datetime.datetime.strptime(
                user_input.strip(), fmt_month_day_year).date()
            entries = Entry.select().where(Entry.date == search_date)
            self.display_entries(entries)
        else:
            error = "I don't recognize that format. Please try again.\n"
            return self.search_by_date(error)
        input("\nPress enter to return to the main menu...")

    def delete_entry(self, entry_id):
        entry = Entry.get(Entry.id == entry_id)
        entry.delete_instance()

    def edit_entry(self, entry):
        print("\nUpdate each value or press enter to leave it unchanged.\n")
        prev_employee_name = entry.employee_name
        prev_task_name = entry.task_name
        prev_date = entry.date
        prev_time_spent = entry.time_spent
        prev_notes = entry.notes
        new_employee_name = input('Employee Name: ')
        entry.employee_name = new_employee_name or prev_employee_name
        new_task_name = input('Task Name: ')
        entry.task_name = new_task_name or prev_task_name
        new_date = input('Date: ')
        entry.date = new_date or prev_date
        new_time_spent = input('Time: ')
        entry.time_spent = new_time_spent or prev_time_spent
        notes_list = []
        print("Enter notes here. Press enter on a blank line to save.")
        notes = "A"
        while notes != '':
            notes = input('Notes: ')
            notes_list.append(notes.replace('\\n', '\n'))
        new_notes = '\n'.join(notes_list)
        entry.notes = new_notes or prev_notes
        entry.save()

    def display_entry(self, entry):
        """Print a single entry to the screen"""
        border = '-' * 50
        print(border)
        print('Employee: {}'.format(entry.employee_name))
        print('Task Name: {}'.format(entry.task_name))
        print("Date: {}".format(entry.date))
        print("Time Spent: {}".format(entry.time_spent))
        if entry.notes != '':
            print("Notes:\n{}\n{}".format('----------', entry.notes))
        print(border)

    def display_entries(self, entries):
        """Prints a list of log entries and allows paging through each entry
        individually. Also allows picking an entry for editing or deletion."""
        entries = list(entries)
        if len(entries) == 0:
            print("\nNo results were found.\n")
            input("Press enter to return to the main menu...")
            self.main_menu()
        counter = 0
        error = None
        while True:
            self.clear_screen()
            if len(entries) == 0:
                print("There are no more entries!")
                input("Press enter to return to the main menu...")
                self.main_menu()
            if error:
                print(error)
                input("Press enter to continue...")
                self.clear_screen()
                error = None
            self.display_entry(entries[counter])
            print("\nWhat would you like to do?")
            print("  N: Next entry (Default)")
            print("  p: Previous entry")
            print("  e: Edit entry")
            print("  d: Delete entry")
            print("  q: Quit to main menu")
            user_input = input("Next, previous, edit, delete, quit: ").lower()
            if user_input == 'q':
                self.main_menu()
            elif user_input == 'p':
                if counter <= 0:
                    error = "End of list. Can't go back."
                    continue
                counter -= 1
            elif user_input == 'd':
                self.delete_entry(entries[counter].id)
                del entries[counter]
                if counter > len(entries) - 1:
                    counter -= 1
                print('Entry deleted!')
                input("Press enter to continue...")
            elif user_input == 'e':
                self.edit_entry(entries[counter])
            else:
                counter += 1
                if counter > len(entries) - 1:
                    counter -= 1
                    error = "End of list. Can't move forward."

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    initialize()
    log = WorkLog()
    log.main_menu()
