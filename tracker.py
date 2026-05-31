import cv2
import mediapipe as mp
import numpy as np
from datetime import datetime


class PoseTracker:

    def __init__(self):

        self.pose = mp.tasks.vision.PoseLandmarker

        self.last_detected = None
        self.last_time = datetime.now()

    def detect_exercise(self, landmarks):

        return None

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

        return None
