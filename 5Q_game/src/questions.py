
# Used in create_objects_data()
PROPERTIES = [
    "animal",
    "food",
    "furniture",
    "appliance",
    "vehicle",
    "tool",
    "electronic",
    "holdable",
    "indoor",
    "engine",
    "used_for_work",
    "four_wheels",
    "pet",
    "healthy"]

QUESTIONS = {
    "animal": "Is it an animal?",
    "food": "Is it food?",
    "furniture": "Is it a piece of furniture?",
    "appliance": "Is it an appliance?",
    "vehicle": "Is it a vehicle?",
    "tool": "Is it a tool?",
    "electronic": "Is it electronic?",
    "holdable": "Can you hold it in your hand?",
    "indoor": "Would you normally find it indoors?",
    "engine": "Does it have an engine?",
    "used_for_work": "Is it used for work?",
    "four_wheels": "Does it have 4 wheels?",
    "pet": "Is it a pet?",
    "healthy": "Is it healthy?"
}

ANSWERS = {
    "yes": [1, 0, 0, 0],
    "no": [0, 1, 0, 0],
    "sometimes": [0, 0, 1, 0],
    "unsure": [0, 0, 0, 1],
    "not_asked": [0, 0, 0, 0]
}

# Used in answer_converter()
QUESTION_LIST = {
    "animal": "not_asked",
    "food": "not_asked",
    "furniture": "not_asked",
    "appliance": "not_asked",
    "vehicle": "not_asked",
    "tool": "not_asked",
    "electronic": "not_asked",
    "holdable": "not_asked",
    "indoor": "not_asked",
    "engine": "not_asked",
    "used_for_work": "not_asked",
    "four_wheels": "not_asked",
    "pet": "not_asked",
    "healthy": "not_asked"}