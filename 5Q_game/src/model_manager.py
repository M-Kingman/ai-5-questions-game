import numpy as np
from question_selector import QuestionSelector


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

    def load_model(self, file_path, model):
        """Loads the specified NN"""

        with np.load(file_path) as data:
            model.input_hidden_weights = data['input_hidden_weights']
            model.hidden_biases = data['hidden_biases']
            model.output_weights = data['output_weights']
            model.output_bias = data['output_bias']


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

    model_manager.load_model("../models/test_model_saving.npz", question_selector)

    print("******\nLoad model Test\n******")
    print(f"input_hidden_weights:\n{question_selector.input_hidden_weights} "
          f"hidden_biases:\n{question_selector.hidden_biases} "
          f"output_weights:\n{question_selector.output_weights} "
          f"output_bias:\n{question_selector.output_bias}")