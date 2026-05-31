import cv2
import numpy as np
from datetime import datetime


class PoseTracker:

    def __init__(self):
        self.last_detected = None
        self.last_time = datetime.now()

    def detect_exercise(self, frame):

        h, w = frame.shape[:2]

        brightness = np.mean(frame)

        if brightness < 60:
            return "plank"

        elif brightness < 100:
            return "squat"

        elif brightness < 150:
            return "jumping_jacks"

        else:
            return "leg_raise"

    def process_image(self, image_bytes):

        if image_bytes is None:
            return None

        image_array = np.frombuffer(
            image_bytes,
            np.uint8
        )

        frame = cv2.imdecode(
            image_array,
            cv2.IMREAD_COLOR
        )

        if frame is None:
            return None

        label = self.detect_exercise(frame)

        now = datetime.now()

        if (
            label != self.last_detected
            or
            (now - self.last_time).total_seconds() > 1
        ):
            self.last_detected = label
            self.last_time = now
            return label

        return None
