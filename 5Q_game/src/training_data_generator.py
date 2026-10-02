import csv
from objects import OBJECTS
from questions import *
import random
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

    def save_data_csv(self, training_data, file_path):
        """Saves training data in human-readable csv format"""

        # Row Layout= name + 14 properties + 56 answer values + target
        with open(file_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)

            # Header: game, object, 14 properties, 14 answer, target
            header = ["game", "object"]

            for property_name in PROPERTIES:
                header.append(f"prop_{property_name}")

            for property_name in PROPERTIES:
                header.append(f"answer_{property_name}")

            header.append("target")

            writer.writerow(header)

            # Adds each training game to the csv file
            for game_number, game_data in enumerate(training_data, start=1):
                for row in game_data:
                    name = row[0]
                    properties = row[1:15]
                    answer_values = row[15:71]
                    target = row[71]

                    #converts raw outputs back into words
                    answers = []

                    for index in range(len(PROPERTIES)):
                        encoded = answer_values[index * 4:(index + 1) * 4]

                        for answer_name, encoding in ANSWERS.items():
                            if encoded == encoding:
                                answers.append(answer_name)

                    writer.writerow([game_number, name] + properties + answers + [target])

        print(f"saved {len(training_data)} games to {file_path}")

    def evaluate_model(self, nn_object_probability, evaluation_data):
        """Evaluates the model using new data"""

        correct_predictions = 0

        for single_game in evaluation_data:
            target_object = None
            highest_probability = -1 # Used -1 because an object may have a prediction of 0
            predicted_object = None

            for row in single_game:
                object_name = row[0]
                inputs = row [1:71]
                target = row[71]

                # Get the target object
                if target == 1:
                    target_object = object_name

                # Get the model's prediction
                prediction, _ = nn_object_probability.forward_pass(inputs)

                if prediction > highest_probability:
                    highest_probability = prediction
                    predicted_object = object_name

            if predicted_object == target_object:
                correct_predictions += 1

        accuracy = (correct_predictions / len(evaluation_data)) * 100
        print("DEBUG accuracy:", accuracy)
        return accuracy


# if __name__ == "__main__":
#     # Testing
#     generator = TrainingDataGenerator(100)
#     training_data = generator.generate_training_data()
#
#     object_probability = ObjectProbability()
#     object_probability.epochs = 100
#
#     object_probability.training(training_data)
#
#     # Test a training example
#     training_row = training_data[0][0]
#
#     training_inputs = training_row[0:70]
#     training_target = training_row[70]
#
#     prediction, _ = object_probability.forward_pass(training_inputs)
#
#     print(f"Target: {training_target}")
#     print(f"Prediction: {prediction}")