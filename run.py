import sys
import time
from time import sleep
import gspread
from google.oauth2.service_account import Credentials
from email_validator import validate_email, EmailNotValidError
from colorama import init
import os
import random

# Initializes Colorama
init(autoreset=True)

# Scope and constant vars defined as in love_sandwiches walk-through project
# by Code Institute
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

# My updated values
SHEET = GSPREAD_CLIENT.open('connect4_database')
PLAYERS_WORKSHEET = SHEET.worksheet("Players")

# Text colors
YELLOW = "\033[1;33;48m"
RED = "\033[1;31;48m"
GREEN = "\033[1;32;48m"
BLUE = "\033[1;34;48m"
LOGO_Y = "\033[0;33;48m"
LOGO_R = "\033[0;31;48m"


def logo():
    """
    Display game name
    """
    print(BLUE + "Welcome to:")
    print(" ")
    print(LOGO_Y + "  ____                                   _       ___ ")
    print(LOGO_Y + " / __ \                                 | |     /   |")
    print(LOGO_Y + "| /  \/  ___   _ __   _ __    ___   ___ | |_   / /| |")
    print(LOGO_R + "| |     / _ \ |  _ \ |  _ \  / _ \ / __|| __| / /_| |")
    print(LOGO_R + "| \__/\| (_) || | | || | | ||  __/| (__ | |_  \___  |")
    print(LOGO_Y + " \____/ \___/ |_| |_||_| |_| \___| \___| \__|     |_|")
    print(" ")
    print(" ")
    print(BLUE + "                                        for 2 players")
    print(" ")
    print(" ")
    time.sleep(1)


def start_to_do() -> str:
    """
    The program will first show two possible options of the game
    User can select to view the game rules or start the game
    """
    time.sleep(1)
    print(GREEN + "What would you like to do?")
    start_options = "1) View the game rules\n2) Play the game\n"
    start_option_selected = input(start_options)
    separate_line()

    # Validate if answer is either 1 or 2
    while start_option_selected not in ("1", "2"):
        print(GREEN + "Please choose between one of the two options:")
        start_option_selected = input(start_options)
        separate_line()

    if start_option_selected == "1":
        cls()
        logo()
        game_rules()

    elif start_option_selected == "2":
        start_game()

    return start_option_selected


def game_rules():
    """
    Display game rules
    which user can exit by entering any key
    """
    print(BLUE + "\u0332".join("Game Rules:"))
    print("The objective of the game is to be the first one to put four " +
          "of your pieces")
    time.sleep(1)
    print("which fall into columns next to each other in a row")
    time.sleep(1)
    print("either horizontally --, vertically | or diagonally / \.")
    time.sleep(1)
    print("Each column is numbered and you need to enter a column number")
    time.sleep(1)
    print("in which you want to drop your piece.")
    print(" ")
    enjoy = "Good luck and enjoy!!!"
    for char in enjoy:
        sleep(0.1)
        sys.stdout.write(char)
        sys.stdout.flush()
    print(" ")
    time.sleep(1)
    separate_line()
    input("Enter any key to exit...\n")
    cls()
    main()


def start_game() -> str:
    """
    The program will check if users have played the game before
    """
    time.sleep(1)
    print(GREEN + "Have you played before?")
    answer = "1) Yes \n2) No\n"
    answered = input(answer)
    separate_line()

    # Validate if answer is either 1 or 2
    while answered not in ("1", "y", "2", "n"):
        print(GREEN + "Please choose between one of the two options:")
        answered = input(answer)

        separate_line()

    if answered == "1" or answered == "y":
        cls()
        logo()
        log_in_players()

    elif answered == "2" or answered == "n":
        cls()
        logo()
        register_new_players()

    return answered


def separate_line():
    """
    Print '-' lines to separate messages
    """
    print(" ")
    print("- "*30)
    print(" ")


def log_in_players():
    """
    User can log in to existing account
    """
    print(GREEN + "Welcome back! Please help me verify your login details.")
    global player1name
    global player2name

    while True:
        email = get_email("Player1")
        existing_player = is_player_registered(email)

        if existing_player:
            email_row = PLAYERS_WORKSHEET.find(email).row
            player1name = PLAYERS_WORKSHEET.row_values(email_row)[0]
            print(BLUE + f"\nHello {player1name}!\n")
            break

        else:
            input_correct_email("Player1")

    while True:
        email = get_email("Player2")
        existing_player = is_player_registered(email)

        if existing_player:
            email_row = PLAYERS_WORKSHEET.find(email).row
            player2name = PLAYERS_WORKSHEET.row_values(email_row)[0]

            print(BLUE + f"\nHello {player2name}!\n")
            break

        else:
            input_correct_email("Player2")

    time.sleep(2)
    start_game_message(player1name, player2name)


def get_email(playername: str) -> str:
    """
    Ask user to input their email address
    @param playername(string): Player's number
    """
    while True:
        email = input(f"{playername} - what's your email address?\n").strip()

        if validate_user_email(email):
            break

    return email


def validate_user_email(email: str) -> bool:
    """
    Validate the email address.
    It must be of the form name@example.com
    @param email(string): Player's email address
    """
    try:
        validate_email(email)
        return True

    except EmailNotValidError as e:
        print(RED + "\n" + str(e))
        print(RED + "Please try again.\n")


def is_player_registered(email: str) -> bool:
    """
    Verify if the player is registered
    by checking if email exists in the database
    @param email(string): Player's email address
    """
    email_column = PLAYERS_WORKSHEET.col_values(2)

    if email in email_column:
        return True
    else:
        return False


def input_correct_email(player: str):
    """
    Asks players to input their email again
    if the email was not found in the database
    @param player(sting): number of current player

    """
    print(RED + "\nSorry, this email is not registered.\n")
    selected_option = email_not_registered()

    if selected_option == "1":
        print("Please write your email again:")

    elif selected_option == "2":
        register_single_player(player)


def email_not_registered() -> str:
    """
    Called when the email is not registered on the worksheet/database
    Give user an option to enter another email or create a new user
    """
    time.sleep(1)
    print(GREEN + "Would you like to:")
    options = "1) Try another email\n2) Create a new player\n"
    selected_option = input(options)
    separate_line()

    while selected_option not in ("1", "2"):
        print("Please choose between one of the options:")
        selected_option = input(options)

        separate_line()

    return selected_option


def register_single_player(player_number: str):
    """
    Register one player
    if they forgot their email address during the log-in step
    @param player_number(string): number of player who's turn it is
    """
    time.sleep(1)
    print(BLUE + "Creating a new user for you...")
    print(" ")
    new_player = player_number
    player_info = create_new_players(new_player)
    update_players_worksheet(player_info)  # Log data of one player on database


def register_new_players():
    """
    Register new players
    Ask players for an input and save first value (name) in a variable
    It will be displayed in the game to indicate which player's move it is
    """
    global player1name
    player1 = "Player1"  # It will first display that Player1 has to input data
    global player2name
    player2 = "Player2"  # It will first display that Player2 has to input data

    time.sleep(1)
    print(BLUE + "Starting the registration...")
    print(" ")
    player_1_info = create_new_players(player1)
    player_2_info = create_new_players(player2)

    # Log data of both players in separate rows
    update_players_worksheet(player_1_info)
    update_players_worksheet(player_2_info)

    player1name = player_1_info[0]  # Update value of Player1 to input name
    player2name = player_2_info[0]  # Update value of Player2 to input name

    separate_line()
    print(f"Thanks {player1name} & {player2name}," +
           "your details have been registered!\n")

    time.sleep(2)
    start_game_message(player1name, player2name)
    separate_line()


def create_new_players(player_number: str) -> list:
    """
    Create a new player
    Get player's name and email
    Check if email is already in the database
    @param player_number(string): number of the player who's turn it is
    """
    email_column = PLAYERS_WORKSHEET.col_values(2)

    while True:
        player = input(f"{player_number} - what's your name?\n")
        print(" ")

        if validate_username(player):
            break

    while True:
        player_email = get_email(player)

        # Verify if email is already in use
        if player_email not in email_column:
            print(BLUE + "\nThank you!\n")
            break

        else:
            print(RED + f"\nSorry {player}, this email is already used.")
            print(RED + "Please try another email.\n")

    return [player, player_email]


def validate_username(player_name: str) -> bool:
    """
    Validation if the user name input meets the criteria
    It should be between 2 - 12 long using only A-Z
    @param player_name(string): Player name as entered by user input
    """
    if len(player_name) < 2 or len(player_name) > 12:
        print(RED + "Player name must be between 2 - 12 characters long.")
        print(RED + "Please try again.\n")

    elif not player_name.isalpha():
        print(RED + "Player name must only contain A-Z. Please try again.\n")

    else:
        return True


def update_players_worksheet(data: list):
    """
    Update players worksheet
    Add a new row with data provided by both players
    @param data(list): Player's name and email values
    """
    PLAYERS_WORKSHEET.append_row(data)


def start_game_message(player1name: str, player2name: str):
    """
    Displays welcome to the game message
    Once players have logged in
    @param player1(string): Player1's name
    @param player2(string): Player2's name

    """
    separate_line()
    print(GREEN + "Are you ready?")
    print(RED + f"{player1name}" + GREEN + " & " + YELLOW + f"{player2name}")
    print(GREEN + "Let's play the game!")
    separate_line()
    time.sleep(2)
    cls()
    run_game()


def cls():
    """
    Clear the console
    """
    os.system("cls" if os.name == "nt" else "clear")


BOARD_WIDTH = 7
BOARD_HEIGHT = 6


class Board():
    def __init__(self):
        self.board = [[' ' for x in range(BOARD_WIDTH)]
                      for y in range(BOARD_HEIGHT)]
        self.moves = random.randint(0, 1)  # Random player starts the game
        self.last_move = [-1, -1]  # Coordinates outside of the board

    def display_board(self):
        """
        Display a game board of 7 columns and 6 rows
        Dimensions specified in the constant variable
        """
        print(" ")
        for row in range(0, BOARD_HEIGHT):
            print(BLUE + '|', end="")
            for col in range(0, BOARD_WIDTH):
                print(f"  {self.board[row][col]}" + BLUE + "  |", end="")
            print("\n")

        print(BLUE + " -"*21)

        # Display number of columns on the board
        for row in range(BOARD_WIDTH):
            print(BLUE + f"   {row+1}  ", end="")
        print("\n")

    def whos_move(self) -> str:
        """
        Alternate moves between player 1 and 2
        """
        pieces = ['X', 'O']
        return pieces[self.moves % 2]

    def move(self, column) -> bool:
        """
        Look for the first available slot in the column
        and place current player's piece in that space
        """
        for row in range(BOARD_HEIGHT-1, -1, -1):
            # If the space has not been filled in yet
            if self.board[row][column] == ' ':
                # Display pieces in different colors on the board
                if self.whos_move() == 'X':
                    self.board[row][column] = RED + self.whos_move()
                else:
                    self.board[row][column] = YELLOW + self.whos_move()

                self.last_move = [row, column]
                self.moves += 1
                return True

        # If there is no available space in the column
        print(RED + "You cannot put a piece in the full column.")
        print("Please choose another column.\n")
        return False

    def winning_move(self) -> bool:
        """
        Check for 4 pieces in a row
        either horizontally, vertically or diagonally
        """
        last_row = self.last_move[0]
        last_col = self.last_move[1]
        last_move = self.board[last_row][last_col]  # Either 'X' or 'O'

        # Check horizontal lines for win
        def horizontal_win() -> bool:
            for row in range(0, BOARD_HEIGHT):
                # Subtracting 3 as impossible to connect 4 from [row, col > 3]
                for col in range(0, (BOARD_WIDTH - 3)):
                    if(last_move == self.board[row][col] and
                       last_move == self.board[row][col+1]):
                        if(last_move == self.board[row][col+2] and
                           last_move == self.board[row][col+3]):
                            return True
            return False

        # Check vertical lines for win
        def vertical_win() -> bool:
            # Subtracting 3 as impossible to connect 4 from [row < 3 , col]
            for row in range(0, (BOARD_HEIGHT-3)):
                for col in range(0, BOARD_WIDTH):
                    if(last_move == self.board[row][col] and
                       last_move == self.board[row+1][col]):
                        if(last_move == self.board[row+2][col] and
                           last_move == self.board[row+3][col]):
                            return True
            return False

        # Check diagonal lines for win going up and to the right
        def diagonal_win() -> bool:
            for row in range(3, BOARD_HEIGHT):
                # Possible to connect 4 starting at [row >= 3 & col =< 3]
                for col in range(0, (BOARD_WIDTH-3)):
                    if(last_move == self.board[row][col] and
                       last_move == self.board[row-1][col+1]):
                        if(last_move == self.board[row-2][col+2] and
                           last_move == self.board[row-3][col+3]):
                            return True

            # Check diagonal lines for win going down and to the right
            # Possible to connect 4 starting at [row < 3 & col =< 3]
            for row in range(0, (BOARD_HEIGHT-3)):
                for col in range(0, (BOARD_WIDTH-3)):
                    if(last_move == self.board[row][col] and
                       last_move == self.board[row+1][col+1]):
                        if(last_move == self.board[row+2][col+2] and
                           last_move == self.board[row+3][col+3]):
                            return True

            return False  # If there is no winner

        if horizontal_win() or vertical_win() or diagonal_win():
            cls()
            self.display_board()
            if last_move == RED + 'X':
                print(GREEN + "\n----> " +
                      f"{player1name.upper()}" + " is the winner <----\n")
            else:
                print(GREEN + "\n----> " +
                      f"{player2name.upper()}" + " is the winner <----\n")

            time.sleep(2)
            separate_line()
            play_again()

        return False  # If there are no winners


def run_game():
    """
    Start the game once both players have validated their names
    """
    game = Board()

    game_won = False

    while not game_won:
        # If the game continues and there is no winner
        cls()
        game.display_board()

        is_move_valid = False

        while not is_move_valid:
            if game.whos_move() == 'X':
                print(f"{player1name}'s move. You play with " + RED + "X")
                player_move = input(f"Choose a column 1 - {BOARD_WIDTH}:\n")
            else:
                print(f"{player2name}'s move. You play with " + YELLOW + "O")
                player_move = input(f"Choose a column 1 - {BOARD_WIDTH}:\n")

            # if player types invalid input
            try:
                is_move_valid = game.move(int(player_move)-1)
            except:
                print(RED + f"Please choose a column 1 - {BOARD_WIDTH}.\n")

        # The game is over when the last move connects 4 pieces
        game_won = game.winning_move()

        # The game is over if there is a tie
        if game.moves == BOARD_HEIGHT * BOARD_WIDTH:
            cls()
            game.display_board()
            print(GREEN + "\n----> The game is over - it's a tie! <----\n")

            time.sleep(2)
            separate_line()
            play_again()


def play_again():
    """
    Give players an option to carry on playing with same players names
    go back to the main menu or exit the game
    """
    print(GREEN + "What would you like to do:")
    options = "1) Play again\n2) Go to main menu\n3) Quit game\n"
    selected = input(options)
    separate_line()

    # Validate if answer is either 1 or 2 or 3
    while selected not in ("1", "2", "3"):
        print(GREEN + "Please choose between one of below options:")
        selected = input(options)

        separate_line()

    if selected == "1":
        print(BLUE + "Starting a new game for " +
              f"{player1name} & {player2name}!\n")
        time.sleep(2)
        run_game()

    elif selected == "2":
        time.sleep(1)
        cls()
        main()

    elif selected == "3":
        print(BLUE + "Thanks for playing! See you soon!\n")
        sys.exit()


def main():
    """
    Run all program functions
    """
    logo()
    start_to_do()

if __name__ == "__main__":
    main()
