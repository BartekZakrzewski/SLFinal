"""
Main entry point for the game.

This module initializes the game, handles user login via the menu,
runs the game loop, and saves the score to a file.
"""
from src import Game
from src.menu.menu import menu


def main():
    """
    Run the main game loop.

    Handles the user login, game initialization, execution, and score saving.
    """
    username = ""
    score = 0
    while username == "":
        username = menu()
    if username is not None and username != '':
        game = Game(username)
        score = game.run()

    if score > 0 and username is not None and username != '':
        with open('./scores/scores.txt', 'a') as file:
            username = username.split(' ')
            username = '_'.join(username)
            file.write(f"{username} {score}\n")


if __name__ == "__main__":
    main()
