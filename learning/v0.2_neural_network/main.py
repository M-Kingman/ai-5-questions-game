import math
import numpy
import csv
import json
import sys
from neural_network import NeuralNetwork


def position_conversion(position):
    """Converts chessboard position to inputs between 0 and 1"""
    conversion_table = {
        'a': 1, #0
        'b': 2, #1
        'c': 3, #2
        'd': 4, #3
        'e': 5, #4
        'f': 6, #5
        'g': 7, #6
        'h': 8, #7
    }

    # 8 board positions span 7 intervals, so normalize from 0 to 1 using /7
    x_pos = (conversion_table[position[0]] - 1) / 7
    y_pos = (int(position[1]) - 1) / 7
    pos_converted = [x_pos, y_pos]

    return pos_converted


def move_validation(position):
    """"Checks start/end user selected positions are valid"""
    if len(position) == 2 and position[0].isalpha() and position[1].isdigit():
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

    combined_inputs = piece_input + start_input + end_input
    return combined_inputs


def read_training_data():
    """Imports training data set"""
    training_data_set = []
    with open('training_data.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)

        # Converts each item in a row to a float, and then appends the row to training_data_set
        for row in reader:
            if not row or len(row) != 8:
                continue
            row_item_counter = 0
            temp_data_row = [0, 0, 0, 0, 0, 0, 0, 0]
            while row_item_counter < 8:
                temp_data_row[row_item_counter] = float(row[row_item_counter])
                row_item_counter+=1
            training_data_set.append(temp_data_row)

    return training_data_set


def save_model(network):
    """Saves new weights and bias to model.json"""
    data = {
        "input_hidden_weights": network.input_hidden_weights.tolist(),
        "hidden_biases": network.hidden_biases.tolist(),
        "output_weights": network.output_weights.tolist(),
        "output_bias": network.output_bias
    }

    with open("model.json", "w", encoding='utf-8') as file:
        json.dump(data, file)


def load_model(network):
    """Load weights and bias from json"""
    with open('model.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

        input_hidden_weights = numpy.array(data["input_hidden_weights"])
        hidden_biases = numpy.array(data["hidden_biases"])
        output_weights = numpy.array(data["output_weights"])
        output_bias = data["output_bias"]

    network.update_model(input_hidden_weights, hidden_biases, output_weights, output_bias)


def main_menu():
    print("Chess Checker\n===============")
    menu_choice = 0
    while menu_choice != '1' and menu_choice != '2' and menu_choice != '3':
        print("1. Train AI\n2. Play Game\n3. Exit")
        menu_choice = input()
    return menu_choice


def train_ai(network):
    training_data = read_training_data()
    network.training(training_data)
    save_model(network)


def play_game(network):
    load_model(network)
    combined_inputs = get_player_move()
    prediction, cache = network.forward_pass(combined_inputs)
    if prediction <= 0.5:
        print("No, it's an illegal move")
    else:
        print("Yes, you can make that play!")


def main():

    network = NeuralNetwork()

    while True:
        menu_choice = main_menu()
        if menu_choice == "1":
            train_ai(network)
        elif menu_choice == "2":
            play_game(network)
        else:
            sys.exit()


if __name__ == "__main__":
    main()
