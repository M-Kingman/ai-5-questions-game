class ObjectState:
    """Keeps track of each objects state"""
    # Creates an object for each object in OBJECTS

    def __init__(self, name, properties, property_input_values, indicator, probability, possible):

        self.name = name

        # Stores original property values
        self.properties = properties

        # Set once at the beginning of the game
        # values depend on objects presence
        self.property_input_values = property_input_values
        self.indicator = indicator

        # Changes throughout game
        self.probability = probability

        # Used by elimination_rewards method to keep track of possible existing choices
        self.possible = possible

    def get_object_state_inputs(self):
        """Returns the objects numerical state inputs"""

        return self.property_input_values + [self.indicator] + [self.probability]


