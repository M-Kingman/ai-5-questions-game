import numpy as np
import math

rng = np.random.default_rng()
class NeuralNetwork:
    def __init__(self):
        self.input_hidden_weights = rng.uniform(low=-0.5, high=0.5, size=(7, 21))
        self.hidden_biases = rng.uniform(low=-0.5, high=0.5, size=21)
        self.output_weights = rng.uniform(low=-0.5, high=0.5, size=21)
        self.output_bias = 0.5

    def sigmoid(self, weighted_sum):
        return 1 / (1 + np.exp(-weighted_sum))

    def forward_pass(self, inputs):
        #Layer 1 - Hidden layer
        weighted_sum1 = np.dot(inputs, self.input_hidden_weights) + self.hidden_biases
        #Activation function
        activation1 = self.sigmoid(weighted_sum1)

        #Layer 2 - Output layer
        weighted_sum2 = np.dot(activation1, self.output_weights) + self.output_bias
        activation2 = self.sigmoid(weighted_sum2)

        #Stores data for backpropagation
        cache = {
            "weighted_sum1": weighted_sum1,
            "activation1": activation1,
            "weighted_sum2": weighted_sum2,
            "activation2": activation2,
         }

        #Reassigned for easier reading
        prediction = activation2

        return prediction, cache

    def calculate_loss(self, prediction, target):
        """Binary Cross-Entropy (BCE) - to calculate loss"""
        #Decided on BCE as final output is either 'yes' or 'no'
        eps = 1e-15

        #safety buffer to prevent prediction from being exactly 1 or 0
        prediction = np.clip(prediction, eps, 1 - eps)

        loss = -np.mean(target * np.log(prediction) + (1 - target) * np.log(1 - prediction))

        return loss