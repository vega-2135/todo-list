import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('credentials.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('todo-list')

to_do = SHEET.worksheet("to-do")
message1 = f"Choose one of the following:\n"
message2 = f"(1) Create a new to-do list\n(2) Open to-do lists\n(3) Help\n(4) Exit\n"


def get_user_input():
    """ 
    Gets option from user and validates that the input is an integer between 1 and 4,
    if the input does not follows these constrains, then a ValueError is raise 
    """
    while True:
        
        try:
            user_input = int(input("Please write your option here and press Enter to confirm your selection:\n"))
            if user_input >= 1 or user_input <= 4:
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
    if answer == 1:
        create_list()

    elif answer == 2:
        open_list()
    
    elif answer == 3:
        show_help()
    
    else:
        exit_program()


def create_list():
    """ 
    Appends name, date and entry to to-do worksheet
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

    to_do.append_row(list_item)

    print("This is your recently added item :\n")

    # last_name = get_last_item("name")
    # last_date = get_last_item("date")
    # last_task = get_last_item("task")

    print("------------------------------")
    print(f"Date: {date}\n")
    print(f"Name of list: {name}\n")
    print("Tasks: \n")
    for task in tasks:
        print (f"- {task}")
    print("------------------------------\n")



    
# def get_last_item(item):
#     """
#     Gets the last item of each column in to-do. Item 1 is the 
#     name column, item 2 is the date column and number 3 is the task column
#     """def tasks():
# #     task = get_task()
# #     for item in task:
# #         print(f"- {item}")
#     if item == "name":
#         item = 1
#     elif item == "date":
#         item = 2
#     else:
#         item = 3

#     column = to_do.col_values(item)
#     last_item = column[-1]
#     return(last_item)

  
def get_list_name():
    """ 
    Gets name for a new list and checks if the provided answwer already exists 
    in the name column of the to-do worksheet  
    """

    column_name = to_do.col_values(1)
    while True:
        list_name = input("\nPlease enter a name for your new list: \n")
        if list_name not in column_name:
            break
        else:
            print("There is already a list with that name, please choose another name\n")    
    
    return list_name 
            

def get_list_date():
    """ 
    Gets the date in which the new list was created in day-month-year format
    """
    today_date = datetime.now().date()

    formatted_date = today_date.strftime("%d-%m-%Y")
    
    return formatted_date
    

def get_task():
    """
    Gets tasks containing what the user wants to do
    and asks if the user wants to add an additional entry
    """
    tasks = []

    while True:

        task = input("\nEnter entry(Add what you want to do): ").strip()

        tasks.append(task)

        additional_task = input("\nDo you want to add another task to this list? y/n\n").lower().strip()
        
        if additional_task == "y":
            continue
        
        elif additional_task == "n":
            break
        
        else:
            print("Try again")
            continue

    return tasks  


def main():

    print("Welcom# to My TO-DO List!\n")
    print(f"{message1}\n{message2}")
    user_answer = get_user_input()
    choose_option(user_answer)

main()