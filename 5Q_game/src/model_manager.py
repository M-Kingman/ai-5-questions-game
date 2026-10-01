import numpy as np
from question_selector import QuestionSelector
from object_probability import ObjectProbability


class ModelManager:
    """Handles loading/saving of data and models"""

    def save_model(self, file_path, input_hidden_weights, hidden_biases, output_weights, output_bias):
        """Saves the specified NN"""

        np.savez(
            file_path,
            input_hidden_weights=input_hidden_weights,
            hidden_biases=hidden_biases,
            output_weights=output_weights,
            output_bias=output_bias)


# Testing
if __name__ == "__main__":
    model_manager = ModelManager()
    question_selector = QuestionSelector()

    model_manager.save_model(
            "../models/test_model_saving.npz",
            question_selector.input_hidden_weights,
            question_selector.hidden_biases,
            question_selector.output_weights,
            question_selector.output_bias)