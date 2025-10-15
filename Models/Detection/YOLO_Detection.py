from ultralytics import YOLO
import cv2
import os
import random
import numpy as np
from collections import Counter

def draw_boxes(image, results, class_names, color_sample):
    image_with_boxes = image.copy()

    for box in results.boxes:
        xmin, ymin, xmax, ymax = map(int, box.xyxy[0])
        cls_id = int(box.cls[0])
        # print(cls_id)
        # print(box)
        label = f"{class_names[cls_id]}"

        color = random.choice(color_sample)

        # Draw the bounding box
        cv2.rectangle(image_with_boxes, (xmin, ymin), (xmax, ymax), color, 2)

        # Put text over the filled background
        cv2.putText(
            image_with_boxes,
            label,
            (xmin, ymin - 5),
            cv2.FONT_HERSHEY_COMPLEX,
            1,
            color,  # Black text
            2,
            cv2.LINE_AA,
        )

    return image_with_boxes



def detection(image, class_names, color_sample, weights):
    
    # Load the model
    weights_path = os.path.join(os.path.dirname(__file__),"..","Weights",f"{weights}")

    model = YOLO(weights_path)
    
    # Inference
    results = model(image)[0]  # Get first result (one image)

    image_numpy = np.array(image)

    image_with_boxes = draw_boxes(image_numpy, results, class_names, color_sample)    

    # Filter labels where score > 0.8
    filtered_labels = [int(box.cls[0]) for box in results.boxes]

    # Count occurrences of each class
    counter = Counter(filtered_labels)

    return image_with_boxes, counter

