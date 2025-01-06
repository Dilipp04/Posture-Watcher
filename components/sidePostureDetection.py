import cv2
import math as m
import mediapipe as mp
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QApplication


class PostureAnalyzer:
    def __init__(self):
        self.good_frames = 0
        self.bad_frames = 0
        self.fps = 30  # Default FPS
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.cap = None

    def start_camera(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise Exception("Error: Cannot access the webcam.")
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))

    def release_camera(self):
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


class PostureApp(QWidget):
    def __init__(self):
        super().__init__()
        # self.setWindowFlag(Qt.FramelessWindowHint)  # No border

        self.posture_analyzer = PostureAnalyzer()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Posture Monitoring")

        self.video_label = QLabel(self)
        self.video_label.setFixedSize(720, 480)

        self.status_label = QLabel("Status: Unknown", self)
        self.status_label.setAlignment(Qt.AlignCenter)

        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_monitoring)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_monitoring)

        layout = QVBoxLayout(self)
        layout.addWidget(self.video_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

    def start_monitoring(self):
        try:
            self.posture_analyzer.start_camera()
            self.timer.start(30)  # 30ms for ~33 FPS
        except Exception as e:
            self.status_label.setText(str(e))

    def stop_monitoring(self):
        self.timer.stop()
        self.posture_analyzer.release_camera()
        self.status_label.setText("Monitoring stopped.")

    def update_frame(self):
        frame, posture_data = self.posture_analyzer.process_frame()
        if frame is not None:
            height, width, channel = frame.shape
            bytes_per_line = channel * width
            qimg = QImage(frame.data, width, height, bytes_per_line, QImage.Format_BGR888)
            self.video_label.setPixmap(QPixmap.fromImage(qimg))

            if posture_data["status"]:
                self.status_label.setText(f"Posture Status: {posture_data['status']}")
        else:
            self.status_label.setText("No frame available.")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = PostureApp()
    window.show()
    sys.exit(app.exec())
