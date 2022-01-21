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
    the program will first show two possible options
    user can select a game for either 2 or 1 player
    """
    print("Select game option:")
    game_options = "1) 2 Players \n2) Player vs. Computer\n"
    game_selected = input(game_options)
    separate_line()

    # Validate if answers is either 1 or 2    
    while game_selected not in ("1", "2"):
        print("Please choose between one of the options:")
        game_selected = input(game_options)

        separate_line()

    if game_selected == "1":
        print("2 players game selected")
        print(" ")
        get_players_names()

    elif game_selected == "2":
        print("Player vs computer game selected")
        print(" ")
        login_or_register()

    return game_selected


def separate_line():
    """
    Print a - line to end the sections
    """
    print(" ")
    print("- "*25)
    print(" ")


def get_players_names():
    """
    Players can enter their name
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
            print(f"Hello {player2name}!\n")
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
        print("Player name must be between 2 - 12 characters long. Please try again.\n")
    elif not playername.isalpha():
        print("Player name must only contain A-Z. Please try again.\n")
    else:
        return True


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
        print("Please try again")


def login_or_register():
    """
    Verify if the player wants to register to an existing account
    or create a new user/player
    """
    print("Would you like to:")
    selected_option = input("1) Log in\n2) Create a new player\n")
    
    separate_line()

    while selected_option not in ("1", "2"):
        print("Please choose between one of the options.")
        selected_option = input("1) Log in\n2) Create a new player\n")

        separate_line()

    # Log in option
    if selected_option == "1":
        print("Selected Log in option")
        #add function for user login
        
    # Register to an existing account option
    elif selected_option == "2":
        create_new_player()


def create_new_player():
    """
    Create a new account for the player
    Collect player's name and email
    Check if it's already in the database
    """
    print("Creating a new player....")

    players_worksheet = SHEET.worksheet("Players")
    email_column = players_worksheet.col_values(2)

    while True:
        player_name = input("What's your name?\n")

        if validate_username(player_name):
            break
      
    while True:
        email = input("What is your email address?\n").strip()

        if validate_user_email(email):
            break

    print(email_column)

def main():
    """
    Run all program functions
    """
    welcome()
    select_game()

if __name__ == "__main__":
    main()