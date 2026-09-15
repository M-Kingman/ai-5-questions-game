from objects import OBJECTS
from vision import Vision
from questions import QUESTIONS

def create_objects_data(list_of_objects):
    """Gets the properties for the list of identified objects"""
    properties = [
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

def main():

    vision = Vision()
    print(create_objects_data(vision.detect_objects("../scenes/beach.jpg")))

if __name__ == "__main__":
    main()