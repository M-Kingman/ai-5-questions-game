from ultralytics import YOLO


class Vision:
    def __init__(self):
        self.model = YOLO("yolo11n.pt")

    def detect_objects(self, image_path):
        """Returns a unique list of objects that are in the scene"""
        results = self.model(image_path)[0]
        objects = []

        for detected_object in results.boxes:
            class_id = int(detected_object.cls[0])
            object_name = self.model.names[class_id]
            objects.append(object_name)

        # Gets rid of duplicates
        objects = list(set(objects))
        return objects

