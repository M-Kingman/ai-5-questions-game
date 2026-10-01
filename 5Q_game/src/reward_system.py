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

    def __init__(self, game_state):
        self.elimination_points = 0
        self.entropy_points = 0
        self.final_guess_points = 0
        self.game_state = game_state
        self.probabilities_before = {}
        self.probabilities_after = {}

    def elimination_reward(self, objects_start, objects_end):
        N = objects_start
        E = (objects_start - objects_end) / objects_start
        F = 0.01

        round_points = N ** 2 * E * F
        self.elimination_points += round_points

        # Test
        print(f"elimination_points: {self.elimination_points}")

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

        # Test
        print(f"entropy_before: {entropy_before}")
        print(f"entropy_after {entropy_after}")
        print(f"entropy_points: {self.entropy_points}")

    def final_guess_reward(self):

        if self.game_state.final_guess_is_correct:
            self.final_guess_points = 1
        else:
            self.final_guess_points = -1

        # Test
        print(f"Final points: {self.final_guess_points}")