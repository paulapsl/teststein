import random
# https://docs.python.org/3/library/enum.html
from enum import IntEnum
import requests
from matplotlib import pyplot as plt

player_wins = 0
comp_wins = 0
name = (input(f"Enter your name: "))
# paula was here
# paula was here again

host = 'http://localhost:5000/score'

dict_stat = {"Rock": 0, "Paper": 0, "Scissors": 0, "Spock": 0, "Lizard": 0}

menu_options = {
    1: 'Eigene Statistik ansehen',
    2: 'RPSSL spielen'
}


# create enum containing all possible actions
class Action(IntEnum):
    Rock = 0
    Paper = 1
    Scissors = 2
    Spock = 3
    Lizard = 4


# define victories - dict
victories = {
    Action.Scissors: [Action.Lizard, Action.Paper],
    Action.Paper: [Action.Spock, Action.Rock],
    Action.Rock: [Action.Lizard, Action.Scissors],
    Action.Lizard: [Action.Spock, Action.Paper],
    Action.Spock: [Action.Scissors, Action.Rock]
}

# define loses - dict
loses = {
    Action.Scissors: [Action.Rock, Action.Spock],
    Action.Paper: [Action.Scissors, Action.Lizard],
    Action.Rock: [Action.Paper, Action.Lizard],
    Action.Lizard: [Action.Rock, Action.Scissors],
    Action.Spock: [Action.Paper, Action.Lizard]
}


# for formatted console-output
def print_menu():
    for key in menu_options.keys():
        print(key, '--', menu_options[key])


# let computer select a random Action
def get_computer_selection():
    # chooses random value (0-4) defined in enum Action
    selection = random.randint(0, len(Action) - 1)
    action = Action(selection)
    # print(f"Computer chose: ", action)
    return action


# make comp selection based on user input
def smart_comp_selection():
    max_value = max(dict_stat.values())
    # print("max value:", max_value)

    # looks for biggest key in dict --> shows us which symbol is chosen most frequently
    max_key = max(dict_stat, key=dict_stat.get)
    # print("max key:",max_key)

    index = list(dict_stat).index(max_key)
    # print("index:", index)
    # get most frequent action
    most_frequent = Action(index)
    # print("most frequent: ", most_frequent)

    defeats = loses[most_frequent]
    # comp doesn't select random values, picks the first value in order to win
    comp_sel = defeats[0]
    # print(f"Computer chose: ", comp_sel)
    return comp_sel


# get input from user
def get_user_selection():
    # display possible choices
    # value returns value assigned to the action in enum, name returns name of element in enum
    choices = [f"{action.name}[{action.value}]" for action in Action]
    choices_str = ", ".join(choices)
    # get user input
    #  F-strings provide a concise and convenient way to embed python expressions inside string literals for formatting.
    selection = int(input(f"Enter a choice ({choices_str}): "))
    # print("selection", selection)
    action = Action(selection)
    # dict_stat["Action.Lizard"] = dict_stat["Action.Lizard"] + 1
    # print(dict_stat)
    return action


def determine_winner(user_action, computer_action):
    global comp_wins, player_wins
    # define defeats - consists of defined victories from specified user input
    defeats = victories[user_action]
    # print("defeats:", defeats)
    if user_action == computer_action:
        print(f"Both players selected {user_action.name}. It's a tie!")
    elif computer_action in defeats:
        # if computer chose something in the user's selected action victories dict, user wins
        print(f"{user_action.name} beats {computer_action.name}! You win!")
        player_wins = player_wins + 1
    else:
        print(f"{computer_action.name} beats {user_action.name}! You lose.")
        comp_wins = comp_wins + 1


# saves count of wins, statistics and player name to .txt-file
def save_data_to_file():
    data = "Spieler " + str(name) + " gewinnt: " + str(player_wins) + "\nComputer gewinnt: " + str(
        comp_wins) + "\n" + str(dict_stat)
    with open("statistics/stat.txt", 'w') as stat:
        stat.write(data)
        stat.close()


def save_to_server():
    print('Speichere einen Eintrag am Server:')
    stat = str(dict_stat)
    response = requests.put('%s/%s' % (host, name), data={'score': stat})
    print(response)
    print(response.json())


def get_from_server():
    print('---------------------------')
    print('Hole diesen Eintrag wieder:')
    response = requests.get('%s/%s' % (host, name)).json()
    print(response)


def get_plot():
    labels = []
    sizes = []

    for x, y in dict_stat.items():
        labels.append(x)
        sizes.append(y)

    # Plot
    plt.pie(sizes, labels=labels)

    plt.axis('equal')
    plt.show()


def main():
    while (True):
        print_menu()
        option = int(input('Enter your choice: '))
        if option == 1:
            get_from_server()
        else:
            while True:
                try:
                    user_action = get_user_selection()
                    print("User chose:", user_action)
                    # count amount of chosen symbols in dictionary
                    if user_action == Action.Rock:
                        dict_stat["Rock"] = dict_stat["Rock"] + 1
                    elif user_action == Action.Paper:
                        dict_stat["Paper"] = dict_stat["Paper"] + 1
                    elif user_action == Action.Scissors:
                        dict_stat["Scissors"] = dict_stat["Scissors"] + 1
                    elif user_action == Action.Spock:
                        dict_stat["Spock"] = dict_stat["Spock"] + 1
                    elif user_action == Action.Lizard:
                        dict_stat["Lizard"] = dict_stat["Lizard"] + 1


                except ValueError as e:
                    # if an impossible actions gets chosen, let the user know
                    range_str = f"[0, {len(Action) - 1}]"
                    print(f"Invalid selection. Enter a value in range {range_str}")
                    # continue statement in Python returns the control to the beginning of the while loop.
                    continue

                computer_action = smart_comp_selection()
                determine_winner(user_action, computer_action)

                play_again = input("Play again? (y/n): ")
                # .lower because we also accept Y as well as y
                if play_again.lower() != "y":
                    break  # ends while True

                save_data_to_file()

            # stat = str(dict_stat)

            # after the game ended, name and statistics of the player are saved to the flask-server
            save_to_server()
            get_from_server()
            get_plot()


if __name__ == "__main__":
    main()
