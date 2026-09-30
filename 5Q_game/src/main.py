from objects import OBJECTS
from vision import Vision
from questions import *
from object_probability import ObjectProbability
import sys
import random
from pathlib import Path
from PIL import Image


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