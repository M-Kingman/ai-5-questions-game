import math
import numpy
import csv
import json


def position_conversion(position):
    """Converts chessboard position to inputs between 0 and 1"""
    conversion_table = {
        'a': 1,
        'b': 2,
        'c': 3,
        'd': 4,
        'e': 5,
        'f': 6,
        'g': 7,
        'h': 8,
    }

    # 8 board positions span 7 intervals, so normalize from 0 to 1 using /7
    x_pos = int(conversion_table[position[0]] - 1) / 7
    y_pos = (int(position[1]) - 1) / 7
    pos_converted = (x_pos, y_pos)

    return pos_converted


def move_validation(position):
    """"Checks start/end user selected positions are valid"""
    if len(position) == 2 and position[0].isalpha and position[1].isdigit():
        if 1 <= int(position[1]) <= 8:
            if 'a' <= position[0].lower() <= 'h':
                return True
    else:
        return False


def get_player_move():
    """Gets user inputs for questions and applies move_validation(), position_conversion"""
    question1 = "What piece do you choose:\n1: Knight\n2: Bishop\n3: King"
    question2 = "What is the starting position?"
    question3 = "What is the ending position?"

    questions = [question1, question2, question3]

    player_input = ''

    piece_input = [0, 0, 0]
    start_input = [0, 0]
    end_input = [0, 0]

    combined_inputs = piece_input + start_input + end_input

    for i in range(len(questions)):
        validation_check = False
        if i == 0:
            while player_input != '1' and player_input != '2' and player_input != '3':
                print(questions[i])
                player_input = input()
                if player_input == '1':
                    piece_input[0] = 1
                elif player_input == '2':
                    piece_input[1] = 1
                elif player_input == '3':
                    piece_input[2] = 1
                else:
                    print("Please select 1, 2 or 3")
        else:
            while not validation_check:
                print(questions[i])
                player_input = input().lower()
                validation_check = move_validation(player_input)
                if validation_check:
                    pos_input = position_conversion(player_input)
                    if i == 1:
                        start_input = pos_input
                        validation_check = True
                    elif i == 2:
                        end_input = pos_input
                        validation_check = True
                else:
                    print("Please choose a valid position")

    return combined_inputs


def main():
    piece_input = [0, 0, 0]
    start_input = [0, 0]
    end_input = [0, 0]

    piece_input, start_input, end_input = get_player_move()

    print(f"{piece_input}")
    print(f"{start_input}")
    print(f"{end_input}")


if __name__ == "__main__":
    main()
