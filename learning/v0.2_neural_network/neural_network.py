import numpy as np
import math

rng = np.random.default_rng()


class NeuralNetwork:
    def __init__(self):
        self.input_hidden_weights = rng.uniform(low=-0.5, high=0.5, size=(7, 21))
        self.hidden_biases = rng.uniform(low=-0.5, high=0.5, size=21)
        self.output_weights = rng.uniform(low=-0.5, high=0.5, size=21)
        self.output_bias = 0.5
        self.learning_rate = 0.1
        self.epochs = 1000

    def sigmoid(self, weighted_sum):
        return 1 / (1 + np.exp(-weighted_sum))

    def forward_pass(self, inputs):
        # Layer 1 - Hidden layer
        weighted_sum1 = np.dot(inputs, self.input_hidden_weights) + self.hidden_biases
        # Activation function
        activation1 = self.sigmoid(weighted_sum1)

        # Layer 2 - Output layer
        weighted_sum2 = np.dot(activation1, self.output_weights) + self.output_bias
        activation2 = self.sigmoid(weighted_sum2)

        # Stores data for backpropagation
        cache = {
            "weighted_sum1": weighted_sum1,
            "activation1": activation1,
            "weighted_sum2": weighted_sum2,
            "activation2": activation2,
        }

        # Reassigned for easier reading
        prediction = activation2

        return prediction, cache

    def calculate_loss(self, prediction, target):
        """Binary Cross-Entropy (BCE) - to calculate loss"""
        # Decided on BCE as final output is either 'yes' or 'no'
        eps = 1e-15

        # safety buffer to prevent prediction from being exactly 1 or 0
        prediction = np.clip(prediction, eps, 1 - eps)

        loss = -np.mean(target * np.log(prediction) + (1 - target) * np.log(1 - prediction))

        return loss

    def backpropagation(self, inputs, cache, target):
        """Backpropagation to calculate gradients"""

        prediction = cache["activation2"]

        # Layer 2 gradients (output layer)
        gradient2 = prediction - target
        w2_gradient = np.dot(cache["activation1"].T, gradient2)

        # Kept it basic, as I won't be using batches for training
        b2_gradient = gradient2

        # Layer 1 gradients
        # Propagate the output error backwards through the output weights
        # to determine how much each hidden neuron contributed to the error.
        a1_gradient = np.dot(gradient2, self.output_weights.T)

        # Apply the derivative of the sigmoid activation function.
        gradient1 = a1_gradient * (cache["activation1"] * (1 - cache["activation1"]))

        # gradients for weights and bias layer 1
        # Calculate gradients for the input → hidden weights.
        # Each of the 7 inputs connects to all 21 hidden neurons,
        # so the result must contain 7 × 21 gradients.
        w1_gradient = np.outer(inputs, gradient1)

        # one gradient for each hidden bias.
        b1_gradient = gradient1

        backpropagation_data = {
            "w2_gradient": w2_gradient,
            "b2_gradient": b2_gradient,
            "w1_gradient": w1_gradient,
            "b1_gradient": b1_gradient

        }

        return backpropagation_data

    def update_parameters(self, backpropagation_data):
        self.input_hidden_weights = self.input_hidden_weights - self.learning_rate * backpropagation_data["w1_gradient"]
        self.hidden_biases = self.hidden_biases - self.learning_rate * backpropagation_data["b1_gradient"]
        self.output_weights = self.output_weights - self.learning_rate * backpropagation_data["w2_gradient"]
        self.output_bias = self.output_bias - self.learning_rate * backpropagation_data["b2_gradient"]

    def training(self, training_data):
        """Runs through training data to update weights and biases"""
        for epoch in range(self.epochs):
            total_loss = 0

            for training_row in training_data:
                # For each row, applies: forward pass, loss calculation, back propagation and updates parameters

                # Separates current row from training data into inputs and target
                training_inputs = training_row[0:7]
                training_target = training_row[7]

                prediction, cache = self.forward_pass(training_inputs)

                loss = self.calculate_loss(prediction, training_target)
                total_loss += loss

                backpropagation_data = self.backpropagation(training_inputs, cache, training_target)

                self.update_parameters(backpropagation_data)

            # Test for during development, to check if loss decreases
            avg_loss = total_loss / len(training_data)
            print(f"Epoch {epoch + 1}: loss = {avg_loss} ")

    def update_model(self, input_hidden_weights, hidden_biases, output_weights, output_bias):
        "Uses data from load_model() to update the model weights and biases"
        self.input_hidden_weights = input_hidden_weights
        self.hidden_biases = hidden_biases
        self.output_weights = output_weights
        self.output_bias = output_bias