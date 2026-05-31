import cv2
import mediapipe as mp
import numpy as np
from datetime import datetime

class PoseTracker:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.3, min_tracking_confidence=0.3)
        self.last_detected = None
        self.last_time = datetime.now()

    def detect_exercise(self, landmarks):
        if not landmarks:
            return None

        left_hip = np.array([landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].x,
                             landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y])
        left_knee = np.array([landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                              landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].y])
        left_ankle = np.array([landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                               landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value].y])
        left_shoulder = np.array([landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                  landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y])
        right_shoulder = np.array([landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                   landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y])
        hip_height = left_hip[1]
        shoulder_height = (left_shoulder[1] + right_shoulder[1]) / 2
        knee_height = left_knee[1]
        ankle_height = left_ankle[1]

        if hip_height - knee_height < 0.08 and hip_height - ankle_height > 0.2:
            return 'squat'
        if abs(left_ankle[1] - right_shoulder[1]) < 0.15 and abs(right_shoulder[1] - left_shoulder[1]) < 0.15:
            return 'jumping_jacks'
        if left_ankle[1] < left_knee[1] - 0.1:
            return 'leg_raise'
        if abs(hip_height - shoulder_height) < 0.05 and abs(left_knee[1] - left_ankle[1]) < 0.05:
            return 'plank'
        return None

    def process_image(self, image_bytes):
        if not image_bytes:
            return None

        image_array = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        if frame is None:
            return None

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image)
        if not results.pose_landmarks:
            return None

        label = self.detect_exercise(results.pose_landmarks.landmark)
        if not label:
            return None

        now = datetime.now()
        if label != self.last_detected or (now - self.last_time).total_seconds() > 0.5:
            self.last_detected = label
            self.last_time = now
            return label

        return None
