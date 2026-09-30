from questions import QUESTIONS, ANSWERS


class QuestionSystem:
    """Manages questioning process by providing inputs to question_selector, selecting questions,
    processing answers and updating game state."""

    def __init__(self, game_state, object_probability, question_selector):

        self.max_questions = 5
        self.game_state = game_state
        self.object_probability = object_probability
        self.question_selector = question_selector

    def prepare_input(self):
        """Prepares all the needed inputs for the QuestionSelector NN."""

        object_states = self.game_state.get_all_objects_inputs()
        answer_input_list = self.game_state.answer_input_list
        questions_remaining = [self.game_state.questions_remaining]

        question_selector_input_data = (object_states + answer_input_list + questions_remaining)

        return question_selector_input_data

    def get_question_scores(self):
        """Passes prepare_input data into QuestionSelector NN and returns scores"""

        question_scores, cache = self.question_selector.forward_pass(self.prepare_input())
        return question_scores

    def select_question(self):
        """Filters out already asked questions and selects the highest scoring question"""

        question_scores = self.get_question_scores()

        ranked_questions = {}
        question_scores_index = 0

        # Filters out already asked questions
        for question in self.game_state.question_tracker:

            if self.game_state.question_tracker[question] == "not_asked":
                ranked_questions[question] = question_scores[question_scores_index]
            else:
                ranked_questions[question] = 0

            question_scores_index += 1

        # Gets the key for the question with the highest score
        question_to_ask = max(ranked_questions, key=ranked_questions.get)

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
