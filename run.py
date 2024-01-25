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
                return user_input
                break

            else:
                raise ValueError()
            
        except ValueError:
            print("Invalid Answer")

def choose_option(answer):
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
    name = get_list_name(list_name)

    date = get_list_date()

    entry = get_entry()




def get_list_name():
    """ 
    Gets name for a new list and checks if the provided answwer already exists 
    in the name column of the to-do worksheet  
    """

    column_name = todo.col_values(1)
    while True:
        list_name = input("Please enter a name for your new list: ")
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
    

def get_entry():
    """
    Gets entry containing what the user wants to do
    and asks if the user wants to add an additional entry
    """


    while True:

        entries = []

        entry = input("Enter entry(Add what you want to do): ").strip()

        entries.append(entry)

        additional_entry = input("Do you want to add another entry to this list? y/n\n").lower().strip()
        
        if additional_entry == "y":
            continue
        
        elif additional_entry == "n":
            break
        
        else:
            print("Try again")
            continue

    return entries  



# def main():

#     print("Welcome to My TO-DO List!\n")
#     print(f"{message1}\n{message2}")
#     user_answer = get_user_input()
#     print(user_answer)
#     choose_option(user_answer)

#main()