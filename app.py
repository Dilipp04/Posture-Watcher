import cv2
import mediapipe as mp
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import QTimer
from PySide6.QtGui import QImage, QPixmap

# Initialize Mediapipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

class PostureDetectorApp(QWidget):
    def __init__(self):
        super().__init__()

        # UI Elements
        self.video_label = QLabel()
        self.status_label = QLabel("Posture: Unknown")
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.start_button.clicked.connect(self.start_webcam)
        self.stop_button.clicked.connect(self.stop_webcam)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        self.setLayout(layout)

        # Timer for capturing video frames
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        # Webcam feed
        self.cap = None

    def start_webcam(self):
        self.cap = cv2.VideoCapture(0)
        self.timer.start(20)  # Update every 20 ms

    def stop_webcam(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
        self.video_label.clear()

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        # Convert the image to RGB (from BGR)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect posture using Mediapipe
        results = pose.process(rgb_frame)

        # Draw landmarks on the frame
        if results.pose_landmarks:
            self.check_posture(results.pose_landmarks)
            mp.solutions.drawing_utils.draw_landmarks(rgb_frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Convert image to Qt format and display
        qt_img = self.convert_cv_qt(rgb_frame)
        self.video_label.setPixmap(qt_img)

    def check_posture(self, landmarks):
        # Extract key landmarks
        nose = landmarks.landmark[mp_pose.PoseLandmark.NOSE]
        left_ear = landmarks.landmark[mp_pose.PoseLandmark.LEFT_EAR]
        right_ear = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EAR]
        left_shoulder = landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]

        # Analyze vertical and horizontal alignment
        face_alignment = (nose.y - (left_shoulder.y + right_shoulder.y) / 2)  # Face to shoulders alignment
        ear_alignment = abs(left_ear.y - left_shoulder.y) + abs(right_ear.y - right_shoulder.y)  # Ears to shoulders

        # Set posture status based on analysis
        if face_alignment < 0.1 and ear_alignment < 0.1:
            self.status_label.setText("Posture: Good")
        else:
            self.status_label.setText("Posture: Bad")

    def convert_cv_qt(self, cv_img):
        """Convert from an OpenCV image (RGB) to QPixmap (for Qt display)."""
        h, w, ch = cv_img.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(cv_img.data, w, h, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(convert_to_Qt_format)

if __name__ == "__main__":
    app = QApplication([])
    window = PostureDetectorApp()
    window.show()
    app.exec()
