import math

question_1 = "Do you struggle to see texts in books/newspapers?"
question_2 = "Do you struggle to see objects far away?"
question_3 = "Do you struggle to see an object clearly that is 6 meters away?"

questions = [question_1, question_2, question_3]
inputs = [0, 0, 0]
weights = [0.7, 0.4, 0.7]
bias = 0


def neural_equation(inputs, weights, bias):
    """Weighted-sum equation (1 neuron)"""
    answer = ""
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


def main():
    counter = 0

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
