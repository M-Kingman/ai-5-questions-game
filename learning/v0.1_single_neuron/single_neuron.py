import math
import csv
import json

question_1 = "Do you struggle to see texts in books/newspapers?"
question_2 = "Do you struggle to see objects far away?"
question_3 = "Do you struggle to see an object clearly that is 6 meters away?"

questions = [question_1, question_2, question_3]
inputs = [0, 0, 0]
LEARNING_RATE = 0.1
EPOCHS = 100


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
    """Takes a row from the training data and seperates it"""
    training_inputs = [row[0], row[1], row[2]]
    target = row[3]
    return training_inputs, target

def adjust_weights(inputs, weights, bias, error, LEARNING_RATE):
    """Adjusts weights and bias during training"""
    new_weights = []
    for i in range(3):
        adjustment_needed = inputs[i] * error * LEARNING_RATE
        new_weights.append(weights[i] + adjustment_needed)

    new_bias = bias + (error * LEARNING_RATE)
    return new_weights, new_bias


def train(training_data_set, weights, bias, LEARNING_RATE):
    """Runs through training data set to adjust weights and bias """
    for row in range(len(training_data_set)):
        training_inputs, target = (seperate_training_row(training_data_set[row]))
        prediction = neural_equation(training_inputs, weights, bias)
        error = calculate_error(prediction, target)
        new_weights, new_bias = adjust_weights(training_inputs, weights, bias, error, LEARNING_RATE)
        weights = new_weights
        bias = new_bias

    return weights, bias


def epochs_training(training_data_set, weights, bias, LEARNING_RATE, EPOCHS):
    """Loops over training a fixed amount of times"""
    new_weights = weights
    new_bias = bias
    for epoch in range(EPOCHS):
        new_weights, new_bias = train(training_data_set, new_weights, new_bias, LEARNING_RATE)
    return new_weights, new_bias


def save_model(weights, bias):
    """Saves new weights and bias after training"""
    data = {
        "weights": weights,
        "bias": bias
    }

    with open("model.json", "w") as file:
        json.dump(data, file)

def main():
    weights = [0.7, 0.4, 0.7]
    bias = 0
    counter = 0

    training_data_set = read_training_data()

    # Test read_training_data.csv
    print(read_training_data())

    print("before training")
    print(f"weights: {weights} | bias: {bias}")
    weights, bias = epochs_training(training_data_set, weights, bias, LEARNING_RATE, EPOCHS)
    print("after training")
    print(f"weights: {weights} | bias: {bias}")

    save_model(weights, bias)

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
