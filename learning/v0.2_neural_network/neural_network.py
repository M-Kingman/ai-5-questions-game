import numpy as np
import math

rng = np.random.default_rng()
class NeuralNetwork:
    def __init__(self, inputs):
        self.inputs = inputs
        self.input_hidden_weights = rng.uniform(low=-0.5, high=0.5, size=(7, 21))
        self.hidden_biases = rng.uniform(low=-0.5, high=0.5, size=21)
        self.hidden_output_weights = rng.uniform(low=-0.5, high=0.5, size=21)
        self.output_bias = 0