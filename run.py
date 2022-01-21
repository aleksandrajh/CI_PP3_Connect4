import time
import gspread
from google.oauth2.service_account import Credentials
from email_validator import validate_email, EmailNotValidError

# Scope and constant variables defined as in love_sandwiches walk-through project
# by Code Institute
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('connect4_database')


def welcome():
    """
    Add welcome page
    Display game name and author
    """
print(" ")
print(" ")
print(" _____                                   _        ___ ")
print("/  __ \                                 | |      /   |")
print("| /  \/  ___   _ __   _ __    ___   ___ | |_    / /| |")
print("| |     / _ \ |  _ \ |  _ \  / _ \ / __|| __|  / /_| |")
print("| \__/\| (_) || | | || | | ||  __/| (__ | |_   \___  |")
print(" \____/ \___/ |_| |_||_| |_| \___| \___| \__|      |_/")
print(" ")
print("           Created by Aleksandra H.")
print(" ")
print(" ")
print("Game Rules:")
print("The objective of the game is to be the first one to put four of your pieces which fall into columns next to each other in a row either horizontally, vertically or diagonally.")
print("Each column is numbered and you need to enter a column number in which you want to drop your piece.")
print("Good luck and enjoy!!!")
print(" ")


def select_game():
    """
    The program will first show two possible options of the game
    User can select a game for either 2 or 1 player
    """
    print("Select game option:")
    game_options = "1) 2 Players \n2) Player vs. Computer\n"
    game_selected = input(game_options)
    separate_line()

    # Validate if answer is either 1 or 2    
    while game_selected not in ("1", "2"):
        print("Please choose between one of the two options:")
        game_selected = input(game_options)

        separate_line()

    if game_selected == "1":
        print("2 players game selected\n")
        get_players_names()

    elif game_selected == "2":
        print("Player vs computer game selected\n")
        login_or_register()

    return game_selected


def separate_line():
    """
    Print '-' lines to separate messages
    """
    print(" ")
    print("- "*30)
    print(" ")


# Option for 2 players game
def get_players_names():
    """
    Players can enter their names
    """
    while True:
        player1name = input("Please enter Player1 name:\n")

        if validate_username(player1name):
            time.sleep(1)
            print(f"Hello {player1name}!\n")
            break
    
    while True:
        player2name = input("Please enter Player2 name:\n")

        if validate_username(player2name):
            time.sleep(1)
            print(f"Hello {player2name}!")
            break
    
    time.sleep(1)
    separate_line()
    print(f"Are you ready?\n{player1name} & {player2name}, let's play the game!")
    separate_line()


def validate_username(playername):
    """
    Validation if the user name input meets the criteria
    It should be between 2 - 12 long using only A-Z
    """
    if len(playername) < 2 or len(playername) > 12:
        print("\nPlayer name must be between 2 - 12 characters long. Please try again.\n")
    
    elif not playername.isalpha():
        print("\nPlayer name must only contain A-Z. Please try again.\n")
    
    else:
        return True


def get_email():
    """
    Ask user to input their email address
    """
    while True:
        email = input("What is your email address?\n").strip()

        separate_line()

        if validate_user_email(email):
            break

    return email


def validate_user_email(email):
    """
    Validate the email address.
    It must be of the form name@example.com
    """
    try:
        validate_email(email)

        return True

    except EmailNotValidError as e:
        print(str(e))
        print("Please try again.")


# Option for 1 player game
def login_or_register():
    """
    Player has an option to either log in to an exisiting account
    or register a new user
    """
    time.sleep(1)
    print("Would you like to:")
    options = "1) Log in\n2) Create a new player\n"
    selected_option = input(options)
    separate_line()

    # Validate if answers is either 1 or 2    
    while selected_option not in ("1", "2"):
        print("Please choose between one of the two options:")
        selected_option = input(options)

        separate_line()

    if selected_option == "1":
        time.sleep(1)
        log_in_player()
        
    elif selected_option == "2":
        time.sleep(1)
        register_new_player()


def log_in_player():
    """
    User can log in to existing account
    """
    print("Welcome back! Please help me verify your login details.")

    while True:
        email = get_email()
        existing_player = is_player_registered(email)

        if existing_player:
            print("Just a confirmation that the user exists on the worksheet")
            # Add function to start the game for this user 
            break
            
        else:
            print("Sorry, this email is not registered.")
            selected_option = email_not_registered()
                
            if selected_option == "1":
                print("Please write your email again:")

            elif selected_option == "2":
                register_new_player()
                break

                
def email_not_registered():
    """
    Called when the email is not registered on the worksheet/database
    Give user an option to enter another email or create a new user
    """
    time.sleep(1)
    print("Would you like to:")
    options = "1) Try another email\n2) Create a new player\n"
    selected_option = input(options)
    separate_line()

    while selected_option not in ("1", "2"):
        print("Please choose between one of the options:")
        selected_option = input(options)

        separate_line()

    return selected_option


def is_player_registered(email):
    """
    Verify if the player is registered by checking if email exists in the database
    """
    players_worksheet = SHEET.worksheet("Players")
    email_column = players_worksheet.col_values(2)

    if email in email_column:
        return True
    else:
        return False


def register_new_player():
    """
    Register a new player
    """
    player_info = create_new_player()
    update_players_worksheet(player_info)


def create_new_player():
    """
    Create a new player
    Get player's name and email
    Check if email is already in the database
    """
    time.sleep(1)
    print("Creating a new player...")

    players_worksheet = SHEET.worksheet("Players")
    email_column = players_worksheet.col_values(2)

    while True:
        player_name = input("What's your name?\n")
        print(" ")

        if validate_username(player_name):
            break

    while True:
        email = get_email()

        # Verify if email is already in use
        if email not in email_column:
            break
            
        else:
            print(f"Sorry {player_name}, this email is already registered.")
            print("Please try another email.\n")
    
    return [player_name, email]


def update_players_worksheet(data):
    """
    Update players worksheet, add a new row with the player's data provided
    """
    players_worksheet = SHEET.worksheet("Players")
    players_worksheet.append_row(data)
    print("Thanks, your details have been registered!.\n")



def main():
    """
    Run all program functions
    """
    welcome()
    select_game()

if __name__ == "__main__":
    main()