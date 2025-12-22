from src import Game
from src.menu.menu import menu


def main():
    username = ""
    score = 0
    while username == "":
        username = menu()
    if username != None and username != '':
        game = Game(username)
        score = game.run()
        print(f"SCORE!!!: {score}")
    else:
        print('Cancelled the game')

    if score > 0 and username != None and username != '':
        with open('./scores/scores.txt', 'a') as file:
            username = username.split(' ')
            username = '_'.join(username)
            file.write(f"{username} {score}\n")


if __name__ == "__main__":
    main()
