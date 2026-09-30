from game_state import GameState
from question_selector import QuestionSelector
from object_probability import ObjectProbability


class QuestionSystem:
    """Manages questioning process by providing inputs to question_selector, selecting questions,
    processing answers and updating game state."""

    def __init__(self, game_state, question_selector, object_probability):

        self.max_questions = 5
        self.game_state = game_state
        self.question_selector = question_selector
        self.object_probability = object_probability


    def prepare_input(self):
        """Prepares all the needed inputs for the QuestionSelector NN."""

        object_states = self.game_state.object_states


    def update_probabilities(self):
        """Updates the probability for detected objects using ObjectProbability"""

        for object_state in self.game_state.object_states.values():

            # only get probability if object was detected
            if object_state.indicator == 1:

                input_data = (object_state.property_input_values + self.game_state.answer_input_list)

                prediction, cache = self.object_probability.forward_pass(input_data)

                object_state.probability = prediction
