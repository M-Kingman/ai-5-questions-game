from objects import OBJECTS
from vision import Vision
from questions import *


def create_objects_data(list_of_objects):
    """Gets the properties for the list of identified objects"""
    properties = PROPERTIES.copy()

    available_objects_data = []

    for item in list_of_objects:
        complete_data_row = []
        properties_values = []
        item_data = OBJECTS[item]

        for property in properties:
            properties_values.append(item_data[property])

        complete_data_row.append(item)
        complete_data_row.extend(properties_values)
        available_objects_data.append(complete_data_row)

    return available_objects_data


def answer_converter(questions_asked):
    """converts all 14 questions into a 4 digit numerical value"""
    question_list = QUESTION_LIST.copy()
    converted_answers = []

    for key in questions_asked:
        question_list[key] = questions_asked[key]

    for key in question_list:
        question_answer = question_list[key]
        converted_answers.extend(ANSWERS[question_answer])

    return converted_answers

def objects_complete_inputs(available_objects_data, converted_answers):
    """Extends each list from available_objects_data and with answer_converter"""
    for object_data in available_objects_data:
        object_data.extend(converted_answers)

def main():

    vision = Vision()
    print(create_objects_data(vision.detect_objects("../scenes/beach.jpg")))

    #Test answer_converter
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
    print(answer_converter(test_question))


if __name__ == "__main__":
    main()