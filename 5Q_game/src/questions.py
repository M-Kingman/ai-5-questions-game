
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

QUESTIONS = {                                           # Index
    "animal": "Is it an animal?",                       # 0
    "food": "Is it food?",                              # 1
    "furniture": "Is it a piece of furniture?",         # 2
    "appliance": "Is it an appliance?",                 # 3
    "vehicle": "Is it a vehicle?",                      # 4
    "tool": "Is it a tool?",                            # 5
    "electronic": "Is it electronic?",                  # 6
    "holdable": "Can you hold it in your hand?",        # 7
    "indoor": "Would you normally find it indoors?",    # 8
    "engine": "Does it have an engine?",                # 9
    "used_for_work": "Is it used for work?",            # 10
    "four_wheels": "Does it have 4 wheels?",            # 11
    "pet": "Is it a pet?",                              # 12
    "healthy": "Is it healthy?"                         # 13
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