import cv2
import math as m
import mediapipe as mp

class SidePostureAnalyzer:
    def __init__(self):
        self.good_frames = 0
        self.bad_frames = 0
        self.fps = 30  # Default FPS
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.cap = None

    def run(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise Exception("Error: Cannot access the webcam.")
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        print(f"FPS: {self.fps}")

    def stop(self):
        if self.cap:
            self.cap.release()

    def process_frame(self):
        if not self.cap:
            raise Exception("Camera not started.")
        success, image = self.cap.read()
        if not success:
            return None, None

        h, w = image.shape[:2]
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        keypoints = self.pose.process(image_rgb)
        image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

        posture_data = {"status": "Unknown", "neck_inclination": None, "torso_inclination": None}
        if keypoints.pose_landmarks:
            lm = keypoints.pose_landmarks
            lmPose = self.mp_pose.PoseLandmark

            # Landmarks for calculations
            l_shldr = (int(lm.landmark[lmPose.LEFT_SHOULDER].x * w), int(lm.landmark[lmPose.LEFT_SHOULDER].y * h))
            r_shldr = (int(lm.landmark[lmPose.RIGHT_SHOULDER].x * w), int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h))
            l_ear = (int(lm.landmark[lmPose.LEFT_EAR].x * w), int(lm.landmark[lmPose.LEFT_EAR].y * h))
            l_hip = (int(lm.landmark[lmPose.LEFT_HIP].x * w), int(lm.landmark[lmPose.LEFT_HIP].y * h))

            # Draw landmarks
            cv2.circle(image_bgr, l_shldr, 7, (0, 255, 255), -1)
            cv2.circle(image_bgr, r_shldr, 7, (255, 0, 255), -1)
            cv2.circle(image_bgr, l_ear, 7, (0, 255, 255), -1)
            cv2.circle(image_bgr, l_hip, 7, (0, 255, 255), -1)

            # Draw lines
            cv2.line(image_bgr, l_shldr, l_ear, (0, 255, 0), 4)
            cv2.line(image_bgr, l_shldr, r_shldr, (255, 0, 255), 4)
            cv2.line(image_bgr, l_shldr, l_hip, (0, 255, 0), 4)

            # Calculate angles
            neck_inclination = self.calculate_angle(*l_shldr, *l_ear)
            torso_inclination = self.calculate_angle(*l_hip, *l_shldr)

            posture_data["neck_inclination"] = neck_inclination
            posture_data["torso_inclination"] = torso_inclination

            # Determine posture
            if neck_inclination < 40 and torso_inclination < 10:
                self.bad_frames = 0
                self.good_frames += 1
                posture_data["status"] = "Good"
            else:
                self.good_frames = 0
                self.bad_frames += 1
                posture_data["status"] = "Bad"
        return image_bgr, posture_data


    @staticmethod
    def calculate_angle(x1, y1, x2, y2):
        try:
            theta = m.acos((y2 - y1) * (-y1) / (m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * y1))
            return theta * (180 / m.pi)
        except ValueError:
            return 0
