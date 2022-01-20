import time

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
    the program will first show to possible options
    user can select a game for 2 or 1 player
    """
    print("Select game option:\n")
    game_options = "1) 2 Players 2) Player vs. Computer\n"
    game_selected = input(game_options)
           
    if game_selected == "1":
        print("2 players game selected")

    elif game_selected == "2":
        print("Player vs computer")

    else:
        print("Not a valid option, please try again")
        print("Select game option:\n")
        game_selected = input(game_options)



def main():
    """
    Run all program functions
    """
    welcome()
    select_game()

if __name__ == "__main__":
    main()