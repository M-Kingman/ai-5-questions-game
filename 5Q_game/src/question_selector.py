import numpy as np
rng = np.random.default_rng()

# NN Structure
# Inputs: 297
# Hidden Layer: 20
# Output: 14


class QuestionSelector:
    """Predicts the next best question to ask"""

    def __init__(self):
        self.input_hidden_weights = rng.uniform(low=-0.5, high=0.5, size=(297, 20))
        self.hidden_biases = rng.uniform(low=-0.5, high=0.5, size=20)
        self.output_weights = rng.uniform(low=-0.5, high=0.5, size=(20, 14))
        self.output_bias = rng.uniform(low=-0.5, high=0.5, size=14)
        self.learning_rate = 0.1
        self.epochs = 5000