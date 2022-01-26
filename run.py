import sys
import time
import gspread
from google.oauth2.service_account import Credentials
from email_validator import validate_email, EmailNotValidError
from colorama import init
import os

# Initializes Colorama
init(autoreset=True)

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

YELLOW_TEXT = "\033[1;33;40m"
RED_TEXT = "\033[1;31;40m"
GREEN_TEXT = "\033[1;32;48m"
BLUE_TEXT = "\033[1;34;48m"


def welcome():
    """
    Add welcome page
    Display game name and author
    """

    print(" ")
    print(" ")
    print(" ")
    print(YELLOW_TEXT + " _____                                   _        ___ ")
    print(YELLOW_TEXT + "/  __ \                                 | |      /   |")
    print(YELLOW_TEXT + "| /  \/  ___   _ __   _ __    ___   ___ | |_    / /| |")
    print(RED_TEXT + "| |     / _ \ |  _ \ |  _ \  / _ \ / __|| __|  / /_| |")
    print(RED_TEXT + "| \__/\| (_) || | | || | | ||  __/| (__ | |_   \___  |")
    print(YELLOW_TEXT + " \____/ \___/ |_| |_||_| |_| \___| \___| \__|      |_/")
    print(" ")
    print(BLUE_TEXT + "           Created by Aleksandra H.")
    print(" ")
    print(" ")
    time.sleep(1)
    print("\u0332".join("Game Rules:"))
    # print("Game Rules:")
    print("The objective of the game is to be the first one to put four of your pieces which fall into columns next to each other in a row\neither horizontally, vertically or diagonally.")
    print("Each column is numbered and you need to enter a column number in which you want to drop your piece.")
    print("Good luck and enjoy!!!")
    print(" ")
    print(" ")


def select_game():
    """
    The program will first show two possible options of the game
    User can select a game for either 2 or 1 player
    """
    time.sleep(1)
    print(GREEN_TEXT + "Select game option:")
    game_options = "1) 2 Players \n2) Player vs. Computer\n"
    game_selected = input(game_options)
    separate_line()

    # Validate if answer is either 1 or 2    
    while game_selected not in ("1", "2"):
        print(GREEN_TEXT + "Please choose between one of the two options:")
        game_selected = input(game_options)

        separate_line()

    if game_selected == "1":
        print(BLUE_TEXT + "2 players game selected\n")
        get_players_names()

    elif game_selected == "2":
        print(BLUE_TEXT + "Player vs computer game selected\n")
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
        global player1name
        player1name = input("Please enter Player1 name:\n")

        if validate_username(player1name):
            time.sleep(1)
            print(BLUE_TEXT + f"Hello {player1name}!\n")
            break
    
    while True:
        global player2name 
        player2name = input("Please enter Player2 name:\n")

        if validate_username(player2name):
            time.sleep(1)
            print(BLUE_TEXT + f"Hello {player2name}!")
            break
    
    time.sleep(1)
    separate_line()
    print(GREEN_TEXT + "Are you ready?" + RED_TEXT + f"\n{player1name}" + GREEN_TEXT + " & " + YELLOW_TEXT + f"{player2name}"  + GREEN_TEXT + ", let's play the game!")
    separate_line()
    
    time.sleep(2)
    cls()
    run_game() #game for 2 players


def cls():
    """
    Clear the console
    """
    os.system('cls' if os.name=='nt' else 'clear')


def validate_username(playername):
    """
    Validation if the user name input meets the criteria
    It should be between 2 - 12 long using only A-Z
    """
    if len(playername) < 2 or len(playername) > 12:
        print(RED_TEXT + "\nPlayer name must be between 2 - 12 characters long. Please try again.\n")

    elif not playername.isalpha():
        print(RED_TEXT + "\nPlayer name must only contain A-Z. Please try again.\n")
    
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
        print(RED_TEXT + str(e))
        print(RED_TEXT + "Please try again.")


# Option for 1 player game
def login_or_register():
    """
    Player has an option to either log in to an exisiting account
    or register a new user
    """
    time.sleep(1)
    print(GREEN_TEXT + "Would you like to:")
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
    print(BLUE_TEXT + "Welcome back! Please help me verify your login details.")

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
    print(BLUE_TEXT + "Creating a new player...")

    players_worksheet = SHEET.worksheet("Players")
    email_column = players_worksheet.col_values(2)

    while True:
        global player_name
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
            print(RED_TEXT + f"Sorry {player_name}, this email is already registered.")
            print("Please try another email.\n")
    
    return [player_name, email]


def update_players_worksheet(data):
    """
    Update players worksheet, add a new row with the player's data provided
    """
    players_worksheet = SHEET.worksheet("Players")
    players_worksheet.append_row(data)
    print(BLUE_TEXT + f"Thanks {player_name}, your details have been registered!\n")


BOARD_WIDTH = 7
BOARD_HEIGHT = 6

class Board():
    def __init__(self):
        self.board = [[' ' for x in range(BOARD_WIDTH)] for y in range(BOARD_HEIGHT)]
        self.moves = 0
        self.last_move = [-1, -1] # Coordinates ([row, column]) outside of the board

    def display_board(self):
        """
        Display a game board of 7 columns and 6 rows
        """
        print(" ")
        for row in range(0, BOARD_HEIGHT):
            print(BLUE_TEXT + '|', end="")
            for col in range(0, BOARD_WIDTH):
                print(f"  {self.board[row][col]}" + BLUE_TEXT +"  |", end="")
            print("\n")

        print(BLUE_TEXT + " -"*21)

        # Display number of columns on the board
        for row in range(BOARD_WIDTH):
            print(BLUE_TEXT + f"   {row+1}  ", end="")
        print("\n")


    def whos_move(self):
        """
        Alternate moves between player 1 and 2
        """
        pieces = ['X', 'O']
        return pieces[self.moves % 2]


    def move(self, column):
        """
        Look for the first available slot in the column
        and place current player's piece in that space
        """
        for row in range(BOARD_HEIGHT-1, -1, -1):
            if self.board[row][column] == ' ': # If the space has not been filled in yet
                # Display pieces in different colors on the board
                if self.whos_move() == 'X':
                    self.board[row][column] = RED_TEXT + self.whos_move()
                else:
                    self.board[row][column] = YELLOW_TEXT + self.whos_move()
                
                self.last_move = [row, column]
                self.moves += 1
                return True

        # if there is no available space in the column     
        print(RED_TEXT + "You cannot put a piece in the full column. Please choose another column.\n")
        return False


    def winning_move(self):
        """
        Check for 4 pieces in a row
        either horizontally, vertically or diagonally
        """
        last_row = self.last_move[0]
        last_col = self.last_move[1]
        last_move = self.board[last_row][last_col] # either 'X' or 'O'

        # Check horizontal lines for win
        def horizontal_win():
            for row in range(0, BOARD_HEIGHT):
                for col in range(0, (BOARD_WIDTH - 3)): # Subtracting 3 as impossible to connect 4 starting at [row, col > 3]
                    if(last_move == self.board[row][col] and last_move == self.board[row][col+1] and last_move == self.board[row][col+2] and  last_move == self.board[row][col+3]):
                        return True
            return False

        # Check vertical lines for win
        def vertical_win():
            for row in range(0, (BOARD_HEIGHT-3)): # Subtracting 3 as impossible to connect 4 starting at [row < 3 , col]
                for col in range(0, BOARD_WIDTH):
                    if(last_move == self.board[row][col] and last_move == self.board[row+1][col] and last_move == self.board[row+2][col] and  last_move == self.board[row+3][col]):
                        return True
            return False

        # Check diagonal lines for win going up and to the right
        def diagonal_win():
            for row in range(3, BOARD_HEIGHT): # Possible to connect 4 starting at [row >= 3 & col =< 3]
                for col in range(0, (BOARD_WIDTH-3)):
                    if(last_move == self.board[row][col] and last_move == self.board[row-1][col+1] and last_move == self.board[row-2][col+2] and  last_move == self.board[row-3][col+3]):
                        return True

            # Check diagonal lines for win going down and to the right
            for row in range(0, (BOARD_HEIGHT-3)): # Possible to connect 4 starting at [row < 3 & col =< 3]
                for col in range(0, (BOARD_WIDTH-3)):
                    if(last_move == self.board[row][col] and last_move == self.board[row+1][col+1] and last_move == self.board[row+2][col+2] and  last_move == self.board[row+3][col+3]):
                        return True

            return False # if there is no winner

        if horizontal_win() or vertical_win() or diagonal_win():
            cls()
            self.display_board()
            if last_move == RED_TEXT + 'X':
                print(GREEN_TEXT + f"\n-----> {player1name.upper()} is the winner! <-----\n")
            else:
                print(GREEN_TEXT + f"\n-----> {player2name.upper()} is the winner! <-----\n")

            time.sleep(2)
            separate_line()
            play_again()

        return False # If there are no winners


def run_game():
    """
    Start the game once both players have validated their names
    """
    game = Board()

    game_won = False
    
    while not game_won:
        # if the game continues and there is no winner
        cls()
        game.display_board()
       
        is_move_valid = False

        while not is_move_valid:
            if game.whos_move() == 'X':
                print(f"{player1name}'s move. You play with "  + RED_TEXT + "X")
                player_move = input(f"Choose a column 1 - {BOARD_WIDTH}:\n")
            else:
                print(f"{player2name}'s move. You play with "  + YELLOW_TEXT + "O")
                player_move = input(f"Choose a column 1 - {BOARD_WIDTH}:\n")
            
            # if player types invalid input
            try:
                is_move_valid = game.move(int(player_move)-1) # 0-indexing of the board, input 1 will fill in column 0
            except:
                print(RED_TEXT + f"Please choose a column between 1 - {BOARD_WIDTH}.\n")

        # The game is over when the last move connects 4 pieces
        game_won = game.winning_move()

        # The game is over if there is a tie
        if game.moves == BOARD_HEIGHT * BOARD_WIDTH:
            cls()
            game.display_board()
            print(GREEN_TEXT + "\n----> The game is over - it's a tie! <----\n")

            time.sleep(2)
            separate_line()
            play_again()
    

def play_again():
    """
    Give players an option to carry on playing with same names
    or go to the main menu
    """
    print(GREEN_TEXT + "What would you like to do:")
    options = "1) Play again\n2) Go to main menu\n3) Quit game\n"
    selected = input(options)
    separate_line()

    # Validate if answer is either 1 or 2 or 3    
    while selected not in ("1", "2", "3"):
        print(GREEN_TEXT + "Please choose between one of below options:")
        selected = input(options)

        separate_line()

    if selected == "1":
        print(BLUE_TEXT + f"Ok... loading a game for {player1name} & {player2name}!\n")
        time.sleep(2)
        run_game()

    elif selected == "2":
        time.sleep(1)
        cls()
        main()

    elif selected == "3":
        print(BLUE_TEXT + "Thanks for playing! See you soon!\n")
        sys.exit()


def main():
    """
    Run all program functions
    """
    welcome()
    select_game()

if __name__ == "__main__":
    main()