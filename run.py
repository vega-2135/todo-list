import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from tabulate import tabulate
from art import tprint
from termcolor import colored, cprint
from time import sleep
from os import system, name


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
WORKSHEET_TITLE = 'todo'
SHEET_TITLE = 'todo-list'


# Access a specific worksheet within the Google Sheet
SPREADSHEET = GSPREAD_CLIENT.open(SHEET_TITLE)

WORKSHEET_LIST = SPREADSHEET.worksheets()

WORKSHEET = SPREADSHEET.worksheet(WORKSHEET_TITLE)


messages = {
    "welcome message": "\nWelcome to My TO-DO List!\n",
    "choose message": f"Choose one of the following:\n",
    "menu options": f"(1) Create a new to-do list\n(2) Open to-do lists\n(3) "
    "Help\n(4) Exit\n",
    "choose option": "Plase choose an option:\n",
    "open options": f"(1) See lists\n(2) Open list by name\n(3) Open list by "
    "date",
    "next": "What do you want to do next: ",
    "exiting program": "\nYou are exiting the program and redirected to the "
    "main menu......",
    "choose_name": "\nChoose a name by entering the corresponding number.",
    "enter_choice": "\nEnter choice here: \n"
}


def get_user_input():
    """
    Gets option from user and validates that the input is an integer between 1
    and 3, if the input does not follows these constraints, then a ValueError
    is raised

    Return = user_input, type str, this is the option of the main manu that the
    user chooses. This return value will be use as argument in the
    choose_option function
    """
    while True:

        try:
            user_input = input("\nPlease write your option here and press "
                               "Enter to confirm your selection:\n").strip()
            # I'm using int of anwer so the user can exit program entering a
            # string (q) in the choose_option function
            if user_input.lower() == "q" or (int(user_input) >= 1 or
                                             int(user_input) <= 4):
                break

            else:
                raise ValueError()

        except ValueError:
            print("Invalid Answer")

    return user_input


def choose_option(answer):
    """
    Calls the right function depending on the answer provided by the user
    """
    # Here I'm using strings of anwer so the user can exit program entering a
    # string (q)

    if answer == "1":
        create_list()

    elif answer == "2":
        open_list()

    elif answer == "3":
        show_help()
    elif answer == "4":
        exit()

    else:
        main()


def show_menu(messagea, messageb, messagec):
    """
    Displays the main menu to the user
    """
    print(f"\n{messagea}\n")
    print(f"{messageb}")
    print(f"{messagec}")
    user_answer = get_user_input()
    choose_option(user_answer)


def create_list():
    """
    Appends name, date and task/taks provided by the user to
    the todo work sheet
    """
    name = get_list_name()

    date = get_list_date()

    tasks = get_task()

    list_item = []

    list_item.append(name)
    list_item.append(date)
    list_item.append(str(tasks))

    print("")
    print("Loading new item to list....\n")

    WORKSHEET.append_row(list_item)

    print("This is your recently added item :\n")

    print("------------------------------")
    print(f"Date: {date}\n")
    print(f"Name of list: {name}\n")
    print("Tasks: \n")
    for task in tasks:
        print(f"- {task}")
    print("------------------------------")

    show_menu(messages['next'], messages['choose option'],
              messages['menu options'])


def get_list_name():
    """
    Prompts the user for a name for a new list and checks if the
    provided name already exists in the name column of the worksheet
    and if its length is between 1 and 10 characters
    """

    column_name = WORKSHEET.col_values(1)
    while True:
        list_name = input("\nPlease enter a name for your new list(the name "
                          "should be between 1 and 10 characters long):"
                          "\n").strip()

        if len(list_name) < 1 or len(list_name) > 10:
            print("The name should be between 1 and 10 characters long")
            continue
        elif list_name not in column_name and list_name.lower() != "q":
            break
        elif list_name.lower() == "q":
            print(messages["exiting program"])
            sleep(2)
            clear()
            main()
        else:
            print("There is already a list with that name, please choose "
                  "another name\n")

    return list_name


def get_list_date():
    """
    Adds the date in which the new list was created in day-month-year format
    in the date column of the work sheet corresponding to that list
    """
    today_date = datetime.now().date()

    formatted_date = today_date.strftime("%d-%m-%Y")

    return formatted_date


def get_task():
    """
    Prompt the user to add a task and asks if the user
    wants to add an additional task
    """
    tasks = []

    while True:

        task = input("\nAdd task: ").strip()

        if task.lower() == "q":
            print(messages["exiting program"])
            sleep(2)
            clear()
            main()
        elif len(task) < 2:
            print("Tasks should be at least two characters long. Try again.")
            continue
        elif task.lower() != "q":
            tasks.append(task)
        else:
            print(messages["exiting program"])
            main()

        additional_task = input("\nDo you want to add another task "
                                "to this list? y/n\n").lower().strip()

        if additional_task == "y":
            continue
        elif additional_task == "n":
            break
        elif additional_task.lower() == "q":
            print(messages["exiting program"])
            sleep(2)
            clear()
            main()
        else:
            print("Try again")
            continue

    return tasks


def open_list():
    """
    Prompt the user for a number corresponding to an option to:
    show all the lists, open a list by its name or open all lists with
    the same date
    """
    while True:
        print(f"\n{messages['choose option']}\n")
        print(f"{messages['open options']}\n")
        user_choice = input(messages['enter_choice']).strip()

        if user_choice == "1":
            show_lists()
            break
        elif user_choice == "2":
            show_list_by_name()
            break
        elif user_choice == "3":
            show_list_by_date()
            break
        elif user_choice.lower() == "q":
            print(messages["exiting program"])
            sleep(2)
            clear()
            main()
        else:
            print("\nInvalid choice. Please enter 1, 2, or 3.")


def show_lists():
    """
    Displays all the lists created by the user in a table
    """
    list_items = WORKSHEET.get_all_values()
    if len(list_items) == 1:
        print("There is nothing to display.")
    else:
        print("")
        print(tabulate(list_items, headers="firstrow",
                       tablefmt="fancy_grid", numalign="center"))

    show_menu(messages['next'], messages['choose option'],
              messages['menu options'])


def show_list_by_name():
    """
    Displays all the lists name so that the user can then choose one name,
    the user will be prompted to enter a number which corresponds to a name,
    once a number is entered, the whole list's content related with that name
    will be displayed
    """
    list_items = WORKSHEET.get_all_values()
    list_content = []
    column_name = WORKSHEET.col_values(1)
    lists_names = column_name[1:]

    while True:
        try:
            print("   Name")
            print("-----------")
            column_name = WORKSHEET.col_values(1)
            lists_names = column_name[1:]
            id = 1
            for item in lists_names:
                print(f"{id}: {item}")
                id += 1
            print(f"{messages['choose_name']}")

            choice = input(messages["enter_choice"]).strip()
            if choice.lower() == "q":
                print(messages["exiting program"])
                sleep(2)
                clear()
                main()
            elif 0 < (choice_int := int(choice)) <= len(lists_names):
                for element in list_items[int(choice)]:
                    list_content.append(element)
                break
            else:
                raise ValueError

        except ValueError:
            print("\nInput out of range! Please try again.\n")

    print("------------------------------------------------")
    print(f"Date: {list_content[1]}\nName: {list_content[0]}\nTasks:")

    tasks = list_content[-1]
    # eval is use to convert tasks(a str element) to a list element
    tasks_list = eval(tasks)
    for task in tasks_list:
        print(f"  - {task}")
    print("------------------------------------------------\n")

    show_menu(messages['next'], messages['choose option'],
              messages['menu options'])


def show_list_by_date():
    """
    Displays worksheet content of the rows containing the date provided by the
    user
    """
    message = "\nPlease write a date in this format: dd-mm-yy: "
    date_column = 1  # the element with index 1 of the row in the working
    # sheets containing all the elements of a list is the
    # date element
    list_items = WORKSHEET.get_all_values()
    items_by_date = []
    list_date = []

    while True:
        user_answer = input(f"{message} \n").strip()

        for row in list_items:
            if row[date_column] == user_answer:
                list_date.append(row[date_column])
                items_by_date.append(row)

        if user_answer not in list_date and user_answer.lower() != "q":
            print("\nThere is no match with the provided date, try with "
                  "another date\n")
            continue
        elif user_answer.lower() == "q":
            print(messages["exiting program"])
            sleep(2)
            clear()
            main()
        else:
            break

    for item in items_by_date:
        print("------------------------------------------------")
        print(f"Date: {item[1]}\nName: {item[0]}\nTasks:")

        # eval is use to convert tasks(a str element) to a list element
        tasks_list = eval(item[2])
        for task in tasks_list:
            print(f"  - {task}")
        print("------------------------------------------------\n")

    show_menu(messages['next'], messages['choose option'],
              messages['menu options'])


def show_help():
    """
    Explains the user what can they do with this program and how to do it
    """
    help_message = """
    How to Use My To-Do List:\n
    (1) Create a new list:

    To create a new list, enter '1' and follow the prompts to input the
    necessary information. Once your list is created, it will be loaded into
    Google Sheets and displayed for you.

    (2) Open to-do lists:

    Use this option to access:

    - All your lists: Enter '1' in the menu to view all lists in a table
      format.
    - A specific list by name: Enter '2' to access an item by specifying the
      list's name.
    - A specific list by date: Enter '3' to access an item by specifying the
      list's date.

    Note: You can re-start the program at any time by entering q or Q into the
    console.
    """
    print(help_message)
    show_menu(messages['next'], messages['choose option'],
              messages['menu options'])


def clear():
    """
    Clear the program screen depending on the os the user has
    """
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux
    else:
        _ = system('clear')


def main():
    tprint(" MY\nTO-DO\n LIST")
    cprint("My To-Do List © Maria Romero", "magenta")
    sleep(2)
    clear()
    cprint(f"{messages['welcome message']} \n", "magenta")
    print(f"{messages['choose message']}\n{messages['menu options']}")
    user_answer = get_user_input().strip()
    choose_option(user_answer)


main()
