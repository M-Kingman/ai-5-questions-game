from objects import OBJECTS
from vision import Vision
from questions import *
from object_probability import ObjectProbability
import sys
import random
from pathlib import Path
from PIL import Image


def all_objects_data(detected_objects):
    """Assigns values to all objects. Values depend on whether object is present"""
    # Also assigns a 1 or 0 to indicate if object was detected
    # Used by QuestionSelector

    present_objects = create_objects_data(detected_objects)
    complete_objects_data = []
    object_present_indicator = []

    for item in OBJECTS:
        object_found = False
        complete_data_row = []
        not_selected_item_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]

        for present_item in present_objects:
            if present_item[0] == item:
                object_found = True
                complete_data_row = present_item
                object_present_indicator.append(1)

        if not object_found:
            complete_data_row.append(item)
            complete_data_row.extend(not_selected_item_values)
            object_present_indicator.append(0)

        complete_objects_data.append(complete_data_row)

    # 16 objects * 14 properties = 224 values
    # 16 object indicators
    # total: 240 values
    return complete_objects_data, object_present_indicator


def create_objects_data(detected_objects):
    """Gets the properties for the list of identified objects"""
    properties = PROPERTIES.copy()

    available_objects_data = []

    for item in detected_objects:
        complete_data_row = []
        properties_values = []
        item_data = OBJECTS[item]

        for object_property in properties:
            properties_values.append(item_data[object_property])

        complete_data_row.append(item)
        complete_data_row.extend(properties_values)
        available_objects_data.append(complete_data_row)

    # Total objects detected * 14 properties
    return available_objects_data


def answer_converter(questions_asked):
    """converts all 14 questions into a 4 digit numerical value"""
    # Gets updated after each question
    #  following format [0, 0, 0, 0]
    question_list = QUESTION_LIST.copy()
    converted_answers = []

    for key in questions_asked:
        question_list[key] = questions_asked[key]

    for key in question_list:
        question_answer = question_list[key]
        converted_answers.extend(ANSWERS[question_answer])

    # Total values: 56 (14 * 4)
    return converted_answers


def objects_complete_inputs(available_objects_data, converted_answers):
    """Extends each list from available_objects_data with answer_converter"""

    for object_data in available_objects_data:
        object_data.extend(converted_answers)

    return available_objects_data


def probability_checker(completed_objects_data, network_probability):
    """Assigns a probability value to each object using ObjectProbability"""
    probability_list = {}

    for data_object in completed_objects_data:
        object_name = data_object[0]
        input_data = data_object[1:]
        prediction, cache = network_probability.forward_pass(input_data)
        probability_list[object_name] = prediction

    return probability_list


def get_random_scene():
    """Picks a random image from the scenes folder"""

    # Get the folder containing main.py
    src_folder = Path(__file__).resolve().parent

    # Go from src -> 5Q_game -> scenes
    scenes_folder = src_folder.parent / "scenes"

    image_extensions = [".jpg"]

    images = [
        image for image in scenes_folder.iterdir()
        if image.suffix.lower() in image_extensions
    ]

    if not images:
        return None

    return random.choice(images)


def play_game(vision, ):
    print("You will be provided a random scene."
          "\nPick an object from the scene and keep it in mind"
          "\nThe game will then ask you 5 questions, answer as best as you can"
          "\nOnce done, the game will guess which object you picked")

    scene_path = get_random_scene()

    # Displays the selected scene to the player
    image = Image.open(scene_path)
    image.show()

    player_ready = False

    while not player_ready:
        print("\n\nType 'yes' once you're ready for the questions")
        player_input = input().lower()
        if player_input == 'yes':
            player_ready = True

    detected_objects = vision.detect_objects(str(scene_path))

    complete_objects_data, object_present_indicator = all_objects_data(detected_objects)


def main():

    vision = Vision()
    network_probability = ObjectProbability()

    print("Welcome to the 5 Questions Game\n___________________________")

    menu_choice = 0
    while menu_choice != '1' and menu_choice != '2' and menu_choice != '3':
        print("1. Play Game\n2. Neural Network Training\n3. Exit")
        menu_choice = input()

        if menu_choice == "1":
            play_game(vision)
            menu_choice = 0
            print("1. Press anything to play again\n2.Exit")

        elif menu_choice == "2":
            menu_choice = 0

            while menu_choice != '1' and menu_choice != '2':
                print("1. Question Selector Neural Network\n2. Object Probability Neural Network")
                menu_choice = input()

                if menu_choice == "1":
                    menu_choice = 0
                    print("Question Selector Neural Network\n1. Train\n2. Generate Data")
                    menu_choice = input()
                elif menu_choice == "2":
                    menu_choice = 0
                    print("Object Probability Neural Network\n1. Train\n2. Generate Data")
                    menu_choice = input()
                else:
                    print("please make a valid selection")

        elif menu_choice == "3":
            sys.exit()

        else:
            print("please make a valid selection")



    # Test answer_converter
    test_question = {
        "animal": "no",
        "food": "no",
        "furniture": "not_asked",
        "appliance": "not_asked",
        "vehicle": "yes",
        "tool": "not_asked",
        "electronic": "not_asked",
        "holdable": "not_asked",
        "indoor": "sometimes",
        "engine": "not_asked",
        "used_for_work": "not_asked",
        "four_wheels": "not_asked",
        "pet": "not_asked",
        "healthy": "not_asked"}


if __name__ == "__main__":
    main()