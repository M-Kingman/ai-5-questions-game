from questions import QUESTIONS, ANSWERS
import numpy as np

def softmax(values):
    exp_values = np.exp(values - np.max(values))
    return exp_values / np.sum(exp_values)


class QuestionSystem:
    """Manages questioning process by providing inputs to question_selector, selecting questions,
    processing answers and updating game state."""

    def __init__(self, game_state, reward_system, object_probability, question_selector):

        self.max_questions = 5
        self.game_state = game_state
        self.object_probability = object_probability
        self.question_selector = question_selector
        self.reward_system = reward_system

    def prepare_input(self):
        """Prepares all the needed inputs for the QuestionSelector NN."""

        object_states = self.game_state.get_all_objects_inputs()
        answer_input_list = self.game_state.answer_input_list
        questions_remaining = [self.game_state.questions_remaining]

        question_selector_input_data = (object_states + answer_input_list + questions_remaining)

        return question_selector_input_data

    def get_question_logits(self):
        """Passes prepare_input data into QuestionSelector NN and returns raw logits"""

        inputs = self.prepare_input()
        question_logits, cache = self.question_selector.forward_pass(inputs)

        # Provides inputs/outputs to RewardSystem, round_data dictionary
        self.reward_system.round_data[self.game_state.questions_asked + 1]["inputs"] = inputs

        return question_logits

    def select_question(self):
        """Filters out already asked questions before applying softmax
        so the remaining probabilities are only valid selections"""

        # Get raw logits from NN1
        question_logits = self.get_question_logits()

        masked_logits = question_logits.copy()

        # Mask questions that have already been asked
        # -np.inf (neg infinity) ensures masked questions have a probability of 0 after softmax
        for question_index, question in enumerate(self.game_state.question_tracker):
            if self.game_state.question_tracker[question] != "not_asked":
                masked_logits[question_index] = -np.inf

        # Only questions that haven't been asked get a probability (not == 0)
        question_probabilities = softmax(masked_logits)

        # Test
        print("Question probabilities:", question_probabilities)
        print("Sum:", np.sum(question_probabilities))

        # Match each question with its probability
        ranked_questions = {}

        for question_index, question in enumerate(self.game_state.question_tracker):
            ranked_questions[question] = question_probabilities[question_index]

        question_to_ask = max(ranked_questions, key=ranked_questions.get)

        self.reward_system.round_data[self.game_state.questions_asked + 1]["outputs"] = question_probabilities

        # Test:
        print("Selected question:", question_to_ask)

        return question_to_ask

    def ask_question(self):
        """Gets player input for chosen question and updates question_tracker and answer_input_list"""

        question_to_ask = self.select_question()

        print(QUESTIONS[question_to_ask])
        print("Select the number which corresponds to the correct answer:\n")
        print(" 1. 'Yes'\n 2. 'No' \n 3. 'Sometimes' \n 4. 'Unsure'")

        player_answer = input().lower()

        # Updates question_tracker
        if player_answer == '1':
            self.game_state.question_tracker[question_to_ask] = "yes"
        elif player_answer == '2':
            self.game_state.question_tracker[question_to_ask] = "no"
        elif player_answer == '3':
            self.game_state.question_tracker[question_to_ask] = "sometimes"
        else:
            self.game_state.question_tracker[question_to_ask] = "unsure"

        # Updates answer_input_list
        self.game_state.answer_converter()

    def update_progress(self):
        """Updates question count and checks if game is over"""

        self.game_state.questions_asked += 1
        self.game_state.questions_remaining = (5 - self.game_state.questions_asked) / 5

        if self.game_state.questions_asked >= self.max_questions:
            self.game_state.game_over = True

    def update_probabilities(self):
        """Updates the probability for detected objects using ObjectProbability"""

        for object_state in self.game_state.object_states.values():

            # only get probability if object was detected
            if object_state.indicator == 1:

                input_data = (object_state.property_input_values + self.game_state.answer_input_list)

                prediction, cache = self.object_probability.forward_pass(input_data)

                object_state.probability = prediction

    def get_best_answer(self):
        """Gets the highest probability object for the final answer"""

        highest_probability_object = None

        # loops through all objects to get the highest probability
        for object_state in self.game_state.object_states.values():
            if highest_probability_object is None:
                highest_probability_object = object_state
            elif object_state.probability > highest_probability_object.probability:
                highest_probability_object = object_state

        return highest_probability_object.name
