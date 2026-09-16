from objects import OBJECTS
from vision import Vision
from questions import *
from object_probability import ObjectProbability


def all_objects_data(list_of_objects):
    """Assigns values to all objects. Values depend on whether object is present"""
    # Used by QuestionSelector

    present_objects = create_objects_data(list_of_objects)
    complete_objects_data = []

    for item in OBJECTS:
        object_found = False
        complete_data_row = []
        not_selected_item_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]

        for present_item in present_objects:
            if present_item[0] == item:
                object_found = True
                complete_data_row = present_item

        if not object_found:
            complete_data_row.append(item)
            complete_data_row.extend(not_selected_item_values)

        complete_objects_data.append(complete_data_row)

    return complete_objects_data

def create_objects_data(list_of_objects):
    """Gets the properties for the list of identified objects"""
    properties = PROPERTIES.copy()

    available_objects_data = []

    for item in list_of_objects:
        complete_data_row = []
        properties_values = []
        item_data = OBJECTS[item]

        for object_property in properties:
            properties_values.append(item_data[object_property])

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


def main():

    vision = Vision()
    network_probability = ObjectProbability()
    detected_objects = vision.detect_objects("../scenes/beach.jpg")
    available_objects_data = create_objects_data(detected_objects)

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
    converted_answers = answer_converter(test_question)
    completed_objects_data = objects_complete_inputs(available_objects_data, converted_answers)
    probability_list = probability_checker(completed_objects_data, network_probability)
    #print(probability_list)

    # test for all_objects_data
    test_data = all_objects_data(detected_objects)
    print(detected_objects)
    print(test_data)

if __name__ == "__main__":
    main()