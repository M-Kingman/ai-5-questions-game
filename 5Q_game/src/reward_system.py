from scipy.stats import entropy

"""
3 reward systems

    1. Elimination reward = N^2*E*F

    where:
        N - the total amount initially at the begining of the round
        E - is the eliminated ratio percentage in decimal form
        F - Factor to scale down the final number

    2. Based on the difference in shannon entropy before and after the round

    3. Final reward is based on whether the final guess was right:
        +1 if correct
        -1 if wrong

    Notes:
        1 and 2 are rewarded after each round and accumulate
        3 is rewarded only at the end of the 5th round
        All points are then added up and passed to the questions selector nn for training
"""


class RewardSystem:
    """Calculates question rewards and final game rewards for the QuestionSelector.
    Uses a simple reinforcement learning approach based on game feedback."""

    def __init__(self, game_state, question_selector):
        self.elimination_points = 0
        self.entropy_points = 0
        self.final_guess_points = 0
        self.game_state = game_state
        self.question_selector = question_selector
        self.probabilities_before = {}
        self.probabilities_after = {}
        self.round_data = {
            1: {
                "inputs": None,                         # From get_question_scores()
                "outputs": None,                        # From get_question_scores()
                "elimination_reward": None,             # From elimination_reward()
                "entropy_reward": None,                 # From entropy_reward()
                "final_round_assigned_points": None     # From assign_round_rewards()
            },
            2: {
                "inputs": None,
                "outputs": None,
                "elimination_reward": None,
                "entropy_reward": None,
                "final_round_assigned_points": None
            },
            3: {
                "inputs": None,
                "outputs": None,
                "elimination_reward": None,
                "entropy_reward": None,
                "final_round_assigned_points": None
            },
            4: {
                "inputs": None,
                "outputs": None,
                "elimination_reward": None,
                "entropy_reward": None,
                "final_round_assigned_points": None
            },
            5: {
                "inputs": None,
                "outputs": None,
                "elimination_reward": None,
                "entropy_reward": None,
                "final_round_assigned_points": None
            }
        }
        self.round_reward = {}

    def normalised_probability_values(self):
        """Ensures probability value for each detected object is between 0 and 1"""

        probabilities = {}
        amount_of_objects = len(self.game_state.detected_objects)
        probabilities_total = 0

        if self.game_state.questions_asked == 0:
            # Prevents 'ZeroDivisionError: division by zero' by assigning equal probability to all detected objects
            for detected_objects in self.game_state.detected_objects:
                probabilities[detected_objects] = 1 / amount_of_objects
        else:
            for detected_objects in self.game_state.detected_objects:
                # Gets the actual object
                object_state = self.game_state.object_states[detected_objects]
                # Adds the label and probability for the object
                probabilities[detected_objects] = object_state.probability
                probabilities_total += object_state.probability

            # Normalises the probabilities for each object
            for probability in probabilities:
                probabilities[probability] = probabilities[probability] / probabilities_total

        return probabilities

    def elimination_reward(self):

        objects_start = len(self.game_state.possible_objects)
        probabilities = self.normalised_probability_values()

        if objects_start == 0:
            return

        amount_of_eliminated_objects = 0

        items_to_remove = []

        # Considers the object eliminated if probability is < 0.15
        for possible in self.game_state.possible_objects:
            if probabilities[possible] < 0.15: # Uses the normalised probability instead of the raw data
                amount_of_eliminated_objects += 1
                items_to_remove.append(possible)

        for remove_item in items_to_remove:
            self.game_state.possible_objects.remove(remove_item)

        objects_end = len(self.game_state.possible_objects)

        N = objects_start
        E = (objects_start - objects_end) / objects_start
        F = 0.01

        round_points = N ** 2 * E * F
        self.elimination_points += round_points

        self.round_data[self.game_state.questions_asked]["elimination_reward"] = round_points

    def detected_objects_probabilities_before(self):

        self.probabilities_before = self.normalised_probability_values()

    def detected_objects_probabilities_after(self):

        self.probabilities_after = self.normalised_probability_values()

    def entropy_calculation(self, probabilities):
        """Takes normalised probability values and returns entropy value"""

        probability_list = []

        for probability in probabilities:
            probability_list.append(probabilities[probability])

        entropy_output = entropy(probability_list)

        return entropy_output

    def entropy_reward(self):
        """Calculates entropy points using the difference in entropy before and after """

        entropy_before = self.entropy_calculation(self.probabilities_before)
        entropy_after = self.entropy_calculation(self.probabilities_after)

        # Reversed formula to ensure lower entropy means higher reward
        entropy_reward = entropy_before - entropy_after

        self.entropy_points += entropy_reward

        self.round_data[self.game_state.questions_asked]["entropy_reward"] = entropy_reward

        # Test
        print(f"entropy_before: {entropy_before}")
        print(f"entropy_after {entropy_after}")
        print(f"entropy_points: {self.entropy_points}")

    def final_guess_reward(self):

        if self.game_state.final_guess_is_correct:
            self.final_guess_points = 1
        else:
            self.final_guess_points = -1

    def assign_round_rewards(self):
        """Calculates how the combined points for each round will be adjusted.
        Positive rounds contribution % is based on how much each round contributed to the overall positive points.
        Negative rounds get a flat 5 %.
        Decided on this method, so NN will learn faster when correct, but slower when wrong."""

        all_rounds_positive_points = 0

        percentage_left = 100

        round_percentage_contribution = {
            1: {
                "elimination_entropy_combined": None,
                "negative": False,
                "assigned_percentage": None,
            },
            2: {
                "elimination_entropy_combined": None,
                "negative": False,
                "assigned_percentage": None,
            },
            3: {
                "elimination_entropy_combined": None,
                "negative": False,
                "assigned_percentage": None,
            },
            4: {
                "elimination_entropy_combined": None,
                "negative": False,
                "assigned_percentage": None,
            },
            5: {
                "elimination_entropy_combined": None,
                "negative": False,
                "assigned_percentage": None,
            },
        }

        # Broke for loops up for easier readability

        # Calculates combined points and is_negative for each round
        for each_round in round_percentage_contribution:
            elimination_reward = self.round_data[each_round]["elimination_reward"]
            entropy_reward = self.round_data[each_round]["entropy_reward"]
            round_total = elimination_reward + entropy_reward
            is_negative = False

            if round_total <= 0:
                is_negative = True

            round_percentage_contribution[each_round]["elimination_entropy_combined"] = round_total
            round_percentage_contribution[each_round]["negative"] = is_negative

        # Assigns 10% if round was neg; or adds points to total if pos
        for each_round in round_percentage_contribution:
            if round_percentage_contribution[each_round]["negative"]:
                round_percentage_contribution[each_round]["assigned_percentage"] = 5
                percentage_left -= 5
            else:
                all_rounds_positive_points += round_percentage_contribution[each_round]["elimination_entropy_combined"]

        # Calculates the percentage contribution for positive rounds from combined positive points
        for each_round in round_percentage_contribution:
            combined_rewards = round_percentage_contribution[each_round]["elimination_entropy_combined"]

            if not round_percentage_contribution[each_round]["negative"]:
                round_percentage_contribution[each_round]["assigned_percentage"] = \
                    (combined_rewards / all_rounds_positive_points) * percentage_left

        # Assigns the final decided contribution points for each round
        for each_round in round_percentage_contribution:
            combined_points = round_percentage_contribution[each_round]["elimination_entropy_combined"]
            assigned_percentage = round_percentage_contribution[each_round]["assigned_percentage"]
            final_round_assigned_points = combined_points * (1 + assigned_percentage / 100)
            self.round_data[each_round]["final_round_assigned_points"] = final_round_assigned_points

    def train_question_selector(self):
        """Once the game is done, trains the NN on each round separately."""
        "Reason for doing it this way, is that the system needs to know wehther the final answwer was right or wrong " \
        "in order to properly assign the right amount of points"

        for each_round in self.round_data:
            round_training_inputs = []
            inputs = self.round_data[each_round]["inputs"]
            outputs = self.round_data[each_round]["outputs"]
            round_total_reward = self.round_data[each_round]["final_round_assigned_points"]

            round_training_inputs = inputs + outputs + [round_total_reward]

            self.question_selector.training(round_training_inputs)