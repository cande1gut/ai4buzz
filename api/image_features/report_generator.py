"""Contains ReportGenerator class.

This class is used to generate report for the image based on the
returned descriptions from the models."""
import base64
from io import BytesIO
from typing import Any, Dict, List, Union
from api.image_features import descriptions

class ReportGenerator:
    """Generates report for each image feature extraction model."""

    def generate_report(self, descriptions_: Union[descriptions.Descriptions, Any]) -> \
        Dict[str, Union[int, List[float]]]:
        if not isinstance(descriptions_, descriptions.Descriptions):
            return descriptions_
        if descriptions_.feature == 'Object Detection':
            return self._generate_report_for_object_detection(descriptions_)
        elif descriptions_.feature == 'Image Classification':
            return self._generate_report_for_image_classification(descriptions_)
        else:
            {}

    def generate_image_string(self, image) -> bytes:
        # convert to base64
        buffer = BytesIO()
        image_rgb = image.convert('RGB')
        image_rgb.save(buffer, format="JPEG")
        image_string = base64.b64encode(buffer.getvalue())
        return image_string

    def  _generate_report_for_object_detection(self, descriptions_: descriptions.Descriptions) -> \
        Dict[str, Dict[str, Union[int, List[float]]]]:
        object_detections = dict()
        for obj_class, obj_confidence in descriptions_.descriptions:
            if obj_class not in object_detections:
                object_detections[obj_class] = {
                    "freq": 1,
                    "confidences": [obj_confidence] 
                }
            else:
                object_detections[obj_class]["freq"] += 1
                object_detections[obj_class]["confidences"].append(obj_confidence)
        object_detections[
            'processes_bounding_boxes_image_as_base64_string'] = descriptions_.processed_image
        return object_detections

    def  _generate_report_for_image_classification(self,
        descriptions_: descriptions.Descriptions) -> Dict[str, float]:
        classes = dict()
        for image_class, class_confidence in descriptions_.descriptions:
            classes[image_class] = class_confidence
        return classes
