import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('credentials.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('todo-list')

todo = SHEET.worksheet("todo")
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



def main():

    print("Welcome to My TO-DO List!\n")
    print(f"{message1}\n{message2}")
    user_answer = get_user_input()
    print(user_answer)

main()