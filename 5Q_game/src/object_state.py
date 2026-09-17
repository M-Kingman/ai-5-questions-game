class ObjectState:
    """Keeps track of each objects state"""
    # Creates an object for each object in OBJECTS

    def __init__(self, name, properties, property_input_values, indicator, probability):

        self.name = name

        # Stores original property values
        self.properties = properties

        # Set once at the beginning of the game
        # values depend on objects presence
        self.property_input_values = property_input_values
        self.indicator = indicator

        # Changes throughout game
        self.probability = probability




