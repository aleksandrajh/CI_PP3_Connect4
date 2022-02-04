import sys
import time
from time import sleep
import os
import random
from colors import Color as Col
import validation as val


def logo():
    """
    Display game name
    """
    print(Col.BLUE + "Welcome to:")
    print(" ")
    print(Col.LOGO_Y + "  ____                                   _       ___ ")
    print(Col.LOGO_Y + " / __ \                                 | |     /   |")
    print(Col.LOGO_Y + "| /  \/  ___   _ __   _ __    ___   ___ | |_   / /| |")
    print(Col.LOGO_R + "| |     / _ \ |  _ \ |  _ \  / _ \ / __|| __| / /_| |")
    print(Col.LOGO_R + "| \__/\| (_) || | | || | | ||  __/| (__ | |_  \___  |")
    print(Col.LOGO_Y + " \____/ \___/ |_| |_||_| |_| \___| \___| \__|     |_|")
    print(" ")
    print(" ")
    print(Col.BLUE + "                                        for 2 players")
    print(" ")
    print(" ")
    time.sleep(1)


def cls():
    """
    Clear the console
    """
    os.system("cls" if os.name == "nt" else "clear")


def separate_line():
    """
    Print '-' lines to separate messages
    """
    print(" ")
    print("- "*30)
    print(" ")


def main_menu() -> str:
    """
    The program will first show two possible options of the game
    User can select to view game rules or start game
    """
    time.sleep(1)
    print(Col.GREEN + "What would you like to do?")
    start_options = "1) View game rules\n2) Play game\n"
    start_option_selected = input(start_options)
    separate_line()

    # Validate if answer is either 1 or 2
    while start_option_selected not in ("1", "2"):
        print(Col.GREEN + "Please choose between one of the two options:")
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
    print(Col.BLUE + "\u0332".join("Game Rules:"))
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
    print(Col.GREEN + "Have you played before?")
    answer = "1) Yes \n2) No\n"
    answered = input(answer)
    separate_line()

    # Validate if answer is either 1 or 2
    while answered not in ("1", "y", "2", "n"):
        print(Col.GREEN + "Please choose between one of the two options:")
        answered = input(answer)

        separate_line()

    if answered == "1" or answered == "y":
        cls()
        logo()
        val.log_in_players(val.players)

    elif answered == "2" or answered == "n":
        cls()
        logo()
        val.register_new_players(val.players)

    return answered


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
            print(Col.BLUE + '|', end="")
            for col in range(0, BOARD_WIDTH):
                print(f"  {self.board[row][col]}" + Col.BLUE + "  |", end="")
            print("\n")

        print(Col.BLUE + " -"*21)

        # Display number of columns on the board
        for row in range(BOARD_WIDTH):
            print(Col.BLUE + f"   {row+1}  ", end="")
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
                    self.board[row][column] = Col.RED + self.whos_move()
                else:
                    self.board[row][column] = Col.YELLOW + self.whos_move()

                self.last_move = [row, column]
                self.moves += 1
                return True

        # If there is no available space in the column
        print(Col.RED + "You cannot put a piece in the full column.")
        print(Col.RED + "Please choose another column.\n")
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
            if last_move == Col.RED + 'X':
                print(Col.GREEN + "\n----> " +
                      f"{val.player1name.upper()}" + " is the winner <----\n")
            else:
                print(Col.GREEN + "\n----> " +
                      f"{val.player2name.upper()}" + " is the winner <----\n")

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
                print(f"{val.player1name}'s move. " +
                       "You play with " + Col.RED + "X")
                player_move = input(f"Choose a column 1 - {BOARD_WIDTH}:\n")
            else:
                print(f"{val.player2name}'s move. " +
                      "You play with " + Col.YELLOW + "O")
                player_move = input(f"Choose a column 1 - {BOARD_WIDTH}:\n")

            # if player types invalid input
            try:
                is_move_valid = game.move(int(player_move)-1)
            except:
                print(Col.RED + f"Please choose a column 1 - {BOARD_WIDTH}.\n")

        # The game is over when the last move connects 4 pieces
        game_won = game.winning_move()

        # The game is over if there is a tie
        if game.moves == BOARD_HEIGHT * BOARD_WIDTH:
            cls()
            game.display_board()
            print(Col.GREEN + "\n----> The game is over - it's a tie! <----\n")

            time.sleep(2)
            separate_line()
            play_again()


def play_again():
    """
    Give players an option to carry on playing with same players names
    go back to the main menu or exit the game
    """
    print(Col.GREEN + "What would you like to do:")
    options = "1) Play again\n2) Go to main menu\n3) Quit game\n"
    selected = input(options)
    separate_line()

    # Validate if answer is either 1 or 2 or 3
    while selected not in ("1", "2", "3"):
        print(Col.GREEN + "Please choose between one of below options:")
        selected = input(options)

        separate_line()

    if selected == "1":
        print(Col.BLUE + "Starting a new game for " +
              f"{val.player1name} & {val.player2name}!\n")
        time.sleep(2)
        run_game()

    elif selected == "2":
        time.sleep(1)
        cls()
        main()

    elif selected == "3":
        print(Col.BLUE + "Thanks for playing! See you soon!\n")
        sys.exit()


def main():
    """
    Run all program functions
    """
    logo()
    main_menu()

if __name__ == "__main__":
    main()
