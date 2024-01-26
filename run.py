import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import pandas as pd
from tabulate import tabulate

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('credentials.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
WORKSHEET = 'todo'
sheet_title = 'todo-list'

# Sync data from googlesheets to csv file
# Access a specific worksheet within the Google Sheet
spreadsheet = GSPREAD_CLIENT.open(sheet_title)

worksheet_list = spreadsheet.worksheets()

worksheet = spreadsheet.worksheet(WORKSHEET)


# Read data from CSV file into a DataFrame
csv_file = 'to-do.csv'
df = pd.read_csv(csv_file)

# Next step takes place after the create list function, to sync the data 
# that the user added to googlesheets to the csv file saved in this directory


message1 = f"Choose one of the following:\n"
message2 = f"(1) Create a new to-do list\n(2) Open to-do lists\n(3) Help\n(4) Exit\n"
message3 = "Plase choose and option: "
message4 = f"(1) See lists\n(2) Open list by name\n(3) Open list by date"


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

    worksheet.append_row(list_item)

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

    #Sync googlesheet data with csv file
    # Check if the data in CSV and Google Sheet are different
    if not df.equals(pd.DataFrame(worksheet.get_all_values(), columns=df.columns)):
        # Update the CSV file with data from Google Sheet
        df_updated = pd.DataFrame(worksheet.get_all_values(), columns=df.columns)
        df_updated.to_csv(csv_file, index=False)

        print("CSV file has been updated with data from Google Sheet.")
    else:
        print("CSV file is already up-to-date.")

  
def get_list_name():
    """ 
    Gets name for a new list and checks if the provided answwer already exists 
    in the name column of the to-do worksheet  
    """

    column_name = worksheet.col_values(1)
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


def open_list():
    name = 0
    date = 1

    text1 = "Please write a list's name: "
    text2 = "Please write a date in this format: dd-m-y: "

    feedback1 = "There is no match with the provided name, try again with another name"
    feedback2 = "There is no match with the provided date, try again with another date"

    print(f"\n{message3}\n")
    print(f"{message4}\n")
    user_choice = int(input("Enter your choice: "))

    if user_choice == 1:
        show_lists()
    elif user_choice == 2:
        show_list_by(text1, name, feedback1)
    elif user_choice == 3:
        show_list_by(text2, date, feedback2)
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")

    return user_choice

def show_lists():
    """ 
    Shows the all the lists created by the user
    """

    if df.empty:
        print("There is no list. There is nothing to display.")
    else:
        # Display the first row of worksheet centered 
        print(tabulate(df.head(), headers='keys', tablefmt='fancy_grid', numalign="center"))
        

def show_list_by(text, column, feedbak):
    """
    Shows lists content corresponding to the date the user inputs
    """
    list_item = worksheet.get_all_values()
    items = []
    list_name = []

    while True:
        user_answer = input(f"{text} \n")
        
        for row in list_item:
            if row[column] == user_answer:
                list_name.append(row[column])
                items.append(row)
        
        if user_answer not in list_name:
            print("\nThere is no match with the provided date, try with another date\n")
            continue
        else:
            break
            
    
    for element in items:
        name = element[0]
        date = element[1]
        tasks = element[2]
        print("------------------------------------------------")
        print(f"Date: {date}\nName: {name}\nTasks: {tasks}")
        print("------------------------------------------------\n")




def main():

    print("Welcome to My TO-DO List!\n")
    print(f"{message1}\n{message2}")
    user_answer = get_user_input()
    choose_option(user_answer)

main()
    
