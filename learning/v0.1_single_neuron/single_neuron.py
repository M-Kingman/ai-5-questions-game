import math
import csv

question_1 = "Do you struggle to see texts in books/newspapers?"
question_2 = "Do you struggle to see objects far away?"
question_3 = "Do you struggle to see an object clearly that is 6 meters away?"

questions = [question_1, question_2, question_3]
inputs = [0, 0, 0]
weights = [0.7, 0.4, 0.7]
bias = 0


def neural_equation(inputs, weights, bias):
    """Weighted-sum equation (1 neuron)"""
    equation = (inputs[0] * weights[0]) + (inputs[1] * weights[1]) + (inputs[2] * weights[2]) + bias
    # Sigmoid Function
    output = 1 / (1 + math.e ** -equation)
    return output


def final_answer(output):
    """Takes output from neural_equation() and provides final answer"""
    if output <= 0.5:
        answer = "No,you probably dont need an eye test."
    else:
        answer = "Yes, you should probably go for an eye test."
    return answer


def read_training_data():
    """Imports training data set"""
    training_data_set = []
    with open('training_data.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)

        #Converts each item in a row to an Int, and then appends the row to training_data_set
        for row in reader:
            if not row or len(row) != 4:
                continue
            row_item_counter = 0
            temp_data_row = [0, 0, 0, 0]
            while row_item_counter < 4:
                temp_data_row[row_item_counter] = int(row[row_item_counter])
                row_item_counter+=1
            training_data_set.append(temp_data_row)

    return training_data_set


def calculate_error(prediction, target):
    return target - prediction


def seperate_training_row(row):
    training_inputs = [row[0], row[1], row[2]]
    target = row[3]
    return training_inputs, target


def main():
    counter = 0

    # Test read_training_data.csv
    print(read_training_data())

    # Asks questions and takes users inputs
    while counter < 3:
        print(questions[counter])
        print("y for yes or n for no")
        player_input = input().lower()

        while player_input != 'y' and player_input != 'n':
            print("only input 'y' or 'n'")
            player_input = input().lower()

        if player_input == "y":
            inputs[counter] = 1

        counter += 1

    print(final_answer(neural_equation(inputs, weights, bias)))


if __name__ == "__main__":
    main()
