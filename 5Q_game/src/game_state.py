from questions import *
from objects import OBJECTS


class GameState:
    """Keeps track of the overall game state"""
    # Only creates one object representing the game

    def __init__(self, detected_objects):

        # Objects detected by vision
        self.detected_objects = detected_objects

        # Keeps track of which questions have been asked
        self.question_tracker = QUESTION_LIST.copy()

        # Uses question tracker to convert question states into numerical inputs
        self.answer_input_list = [[0, 0, 0, 0] for _ in range(14)]

        # Tracks how many questions have been asked
        self.questions_asked = 0

        # Assigns a value between 0 and 1 (for input)
        self.questions_remaining = (5 - self.questions_asked) / 5

        self.game_over = False

        # Stores all 16 objects from ObjectState
        self.object_states = []





