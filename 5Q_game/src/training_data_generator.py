from questions import *
import random
from objects import OBJECTS
from questions import *
from object_probability import ObjectProbability

class TrainingDataGenerator:
    """Creates training data for the ObjectProbability NN.
    Doesn't use GameState methods because the training data format is different from the actual gameplay format.+"""

    def __init__(self, number_of_games):
        self.number_of_games = number_of_games

    def random_selection(self):
        """Randomly selects 5 questions and a target object"""

        # Randomly selects 1 target object
        target_object_key = random.choice(list(OBJECTS.keys()))
        target_object_properties = OBJECTS[target_object_key]

        # Selects 5 random properties
        random_properties = []
        for i in range(5):
            random_properties_key = random.choice(PROPERTIES)
            while random_properties_key in random_properties:
                random_properties_key = random.choice(PROPERTIES)
            random_properties.append(random_properties_key)

        return target_object_key, target_object_properties, random_properties

    def create_NN_inputs(self, target_object_properties, random_properties):
        """"Converts all OBJECS + random questions + target into NN inputs """

        # Converts object properties into numerical inputs
        numerical_object_prop = []

        for object_name in OBJECTS:
            object_properties = []

            for property_name in PROPERTIES:
                object_properties.append(OBJECTS[object_name][property_name])

            numerical_object_prop.append([object_name] + object_properties)

        # Matches the sim answers to the target properties answers
        simulated_answers = QUESTION_LIST.copy()
        for question in random_properties:
            target_prop_answer = target_object_properties[question]
            if target_prop_answer == 1:
                simulated_answers[question] = "yes"
            elif target_prop_answer == 0:
                simulated_answers[question] = "no"
            else:
                simulated_answers[question] = random.choice(["sometimes", "unsure"])

        # Converts simulated answers into numerical inputs
        sim_answers_numerical =[]

        for question in simulated_answers:
            answer = simulated_answers[question]
            sim_answers_numerical.extend(ANSWERS[answer])

        # Combines object properties and answers into complete NN inputs
        combined_numerical_data = []

        for object_properties in numerical_object_prop:
            combined_numerical_data.append(object_properties + sim_answers_numerical)

        return combined_numerical_data

    def add_training_targets(self, target_object_key, combined_numerical_data):
        """Appends either 1 or 0 to each object"""

        for data_row in combined_numerical_data:
            if data_row[0] == target_object_key:
                data_row.append(1)
            else:
                data_row.append(0)

        # For easier naming
        completed_data = combined_numerical_data

        return completed_data

    def generate_training_data(self):
        """Generates training data based off of number of simulated games"""

        complete_data_sim_pack = []

        for game in range(self.number_of_games):
            target_object_key, target_object_properties, random_properties = self.random_selection()
            combined_numerical_data = self.create_NN_inputs(target_object_properties, random_properties)
            completed_data = self.add_training_targets(target_object_key, combined_numerical_data)

            complete_data_sim_pack.append(completed_data)

        return complete_data_sim_pack

if __name__ == "__main__":
    # Testing
    generator = TrainingDataGenerator(100)
    training_data = generator.generate_training_data()

    object_probability = ObjectProbability()
    object_probability.epochs = 100

    object_probability.training(training_data)

    # Test a training example
    training_row = training_data[0][0]

    training_inputs = training_row[0:70]
    training_target = training_row[70]

    prediction, _ = object_probability.forward_pass(training_inputs)

    print(f"Target: {training_target}")
    print(f"Prediction: {prediction}")