import time
import gspread
from google.oauth2.service_account import Credentials
from email_validator import validate_email, EmailNotValidError
from colors import Color as Col
from run import run_game, cls, separate_line


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


players = ["Player1", "Player2"]


def log_in_players(players):
    """
    User can log in to existing account
    with their email address which is saved in the 2 row of the spreadsheet
    Their names are retrieved from the first row
    Number of games won so far are saved in the 3rd column
    """
    print(Col.GREEN + "Welcome back! " +
          "Please help me verify your login details.")

    global player1name
    global player2name
    global player1score
    global player2score
    # Rows corresponding to input email addresses
    global player1email_row
    global player2email_row

    try:
        for i, player in enumerate(players):
            while True:
                email = get_email(player)
                existing_player = is_player_registered(email)

                if existing_player:
                    if i == 0:
                        player1email_row = PLAYERS_WORKSHEET.find(email).row
                        player1name = \
                            PLAYERS_WORKSHEET.row_values(player1email_row)[0]
                        player1score = \
                            int(PLAYERS_WORKSHEET.row_values(player1email_row)[2])

                        print(Col.BLUE + f"\nHello {player1name}!\n")
                    elif i == 1:
                        player2email_row = PLAYERS_WORKSHEET.find(email).row
                        player2name = \
                            PLAYERS_WORKSHEET.row_values(player2email_row)[0]
                        player2score = \
                            int(PLAYERS_WORKSHEET.row_values(player2email_row)[2])
                        print(Col.BLUE + f"\nHello {player2name}!\n")
                    break

                else:
                    input_correct_email(player)

            time.sleep(2)
            start_game_message(player1name, player2name)
    
    except TypeError:
        return None


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


def validate_user_email(email: str):
    """
    Validate the email address.
    It must be of the form name@example.com
    @param email(string): Player's email address
    """
    try:
        validate_email(email)
        return True

    except EmailNotValidError as e:
        print(Col.RED + "\n" + str(e))
        print(Col.RED + "Please try again.\n")


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
    print(Col.RED + "\nSorry, this email is not registered.\n")
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
    print(Col.GREEN + "Would you like to:")
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
    print(Col.BLUE + "Creating a new user for you...")
    print(" ")
    new_player = player_number
    player_info = create_new_players(new_player)
    update_players_worksheet(player_info)  # Log data of one player on database


def register_new_players(players):
    """
    Register new players
    Ask players for an input and save first value (name) in a variable
    It will be displayed in the game to indicate which player's move it is
    """
    global player1name
    global player2name
    global player1score
    global player2score
    global player1email_row
    global player2email_row

    time.sleep(1)
    print(Col.BLUE + "Starting the registration...")
    print(" ")

    while True:
        for i, player in enumerate(players):
            if i == 0:
                player_1_info = create_new_players(player)
                update_players_worksheet(player_1_info)
                player1name = player_1_info[0]
                player1score = player_1_info[2]
                player1email_row = PLAYERS_WORKSHEET.find(player_1_info[1]).row

            elif i == 1:
                player_2_info = create_new_players(player)
                update_players_worksheet(player_2_info)
                player2name = player_2_info[0]
                player2score = player_2_info[2]
                player2email_row = PLAYERS_WORKSHEET.find(player_2_info[1]).row
        break

    separate_line()
    print(f"Thanks {player1name} & {player2name}, " +
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
            print(Col.BLUE + "\nThank you!\n")
            break

        else:
            print(Col.RED + f"\nSorry {player}, this email is already used.")
            print(Col.RED + "Please try another email.\n")

    return [player, player_email, 0]


def validate_username(player_name: str) -> bool:
    """
    Validation if the user name input meets the criteria
    It should be between 2 - 12 long using only A-Z
    @param player_name(string): Player name as entered by user input
    """
    try:
        if len(player_name) < 2 or len(player_name) > 12:
            print(Col.RED + "Player name must be between" +
                  "2 - 12 characters long.")
            print(Col.RED + "Please try again.\n")

        elif not player_name.isalpha():
            print(Col.RED + "Player name must only contain A-Z. " +
                  "Please try again.\n")

        else:
            return True

    except TypeError:
        return False


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
    print(Col.GREEN + "Are you ready?")
    print(Col.RED + f"{player1name}" + Col.GREEN +
          " & " + Col.YELLOW + f"{player2name}")
    print(Col.GREEN + "Let's play the game!")
    separate_line()
    time.sleep(2)
    cls()
    run_game()
