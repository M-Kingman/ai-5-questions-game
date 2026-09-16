from questions import *
import random
from objects import OBJECTS
from questions import *
from main import answer_converter, create_objects_data, objects_complete_inputs

class TrainingDataGenerator:
    """creates training data for the ObjectProbability NN"""

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


    def create_NN_inputs(self, target_object_key, target_object_properties, random_properties):
        """"Converts all OBJECTS + random questions + target into NN inputs """

        # Get all the objects without the properties
        object_list = list(OBJECTS)

        numerical_object_prop = create_objects_data(object_list)

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

        sim_answers_numerical = answer_converter(simulated_answers)

        combined_numerical_data = objects_complete_inputs(numerical_object_prop, sim_answers_numerical)

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


test_train = TrainingDataGenerator(500)
target_object_key, target_object_properties, random_properties = test_train.random_selection()
combined_numerical_data = test_train.create_NN_inputs(target_object_key, target_object_properties, random_properties)
completed_data = test_train.add_training_targets(target_object_key, combined_numerical_data)
print(completed_data)