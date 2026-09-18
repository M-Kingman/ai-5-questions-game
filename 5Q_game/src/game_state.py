from questions import *
from objects import OBJECTS
from object_state import ObjectState


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
        self.object_states = self.create_object_states()

    def create_object_states(self):
        """Creates an ObjectState object for each OBJECT and sets its state,
        depending on if it was detected"""

        # Params needed: name, properties, property_input_values, indicator, probability

        all_object_states = {}

        for item in OBJECTS:
            object_found = False

            name = item
            properties = OBJECTS[item]
            property_input_values = []
            indicator = 0
            probability = 0

            for detected_object in self.detected_objects:
                if detected_object == item:
                    indicator = 1
                    object_found = True
                    for object_property in PROPERTIES:
                        property_input_values.append(properties[object_property])

            if not object_found:
                property_input_values = [0 for _ in range(14)]

            object_state = ObjectState(name, properties, property_input_values, indicator, probability)

            all_object_states[item] = object_state

        return all_object_states

