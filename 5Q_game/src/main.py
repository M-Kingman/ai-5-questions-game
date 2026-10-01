from vision import Vision
from object_probability import ObjectProbability
import sys
import random
from pathlib import Path
from PIL import Image
from game_state import GameState
from question_selector import QuestionSelector
from question_system import QuestionSystem
from model_manager import ModelManager
from reward_system import RewardSystem

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


def play_game(vision, nn_object_probability, nn_question_selector):
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
    game_state = GameState(detected_objects)
    question_system = QuestionSystem(game_state,  nn_object_probability, nn_question_selector)
    reward_system = RewardSystem(game_state)

    while game_state.game_over is not True:
        question_system.ask_question()
        question_system.update_probabilities()
        question_system.update_progress()

    system_object_guess = question_system.get_best_answer()
    game_state.player_reveal(system_object_guess)
    reward_system.final_guess_reward()





def main():

    vision = Vision()
    nn_object_probability = ObjectProbability()
    nn_question_selector = QuestionSelector()
    model_manager = ModelManager()

    model_manager.load_model(nn_object_probability.file_path, nn_object_probability)
    model_manager.load_model(nn_question_selector.file_path, nn_question_selector)

    print("Welcome to the 5 Questions Game\n___________________________")

    menu_choice = 0
    while menu_choice != '1' and menu_choice != '2' and menu_choice != '3':
        print("1. Play Game\n2. Neural Network Training\n3. Exit")
        menu_choice = input()

        if menu_choice == "1":
            play_game(vision, nn_object_probability, nn_question_selector)
            menu_choice = 0

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


if __name__ == "__main__":
    main()