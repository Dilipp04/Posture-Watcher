import sys
import cv2
import mediapipe as mp
import numpy as np
import pickle
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QTimer

class PoseDetectionApp(QWidget):
    def __init__(self):
        super().__init__()

        # Load the trained pose classifier
        self.model = pickle.load(open("pose_classifier.pkl", "rb"))
        self.pose_labels = ["Mountain Pose", "Pranamasan"]  # Adjust as per your dataset

        # Initialize MediaPipe Pose
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.mp_drawing = mp.solutions.drawing_utils

        # Set up UI
        self.setWindowTitle("Pose Detection App")
        self.setGeometry(100, 100, 800, 600)

        self.video_label = QLabel(self)
        self.video_label.setFixedSize(800, 500)

        self.pose_label = QLabel("Pose: Waiting...", self)
        self.pose_label.setStyleSheet("font-size: 18px; font-weight: bold; color: green;")

        self.start_button = QPushButton("Start Camera", self)
        self.start_button.clicked.connect(self.start_camera)

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.pose_label)
        layout.addWidget(self.start_button)
        self.setLayout(layout)

        # Initialize camera and timer
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    def start_camera(self):
        self.timer.start(30)  # Update every 30ms

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return
        
        frame = cv2.flip(frame, 1)  # Flip for a mirror effect
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)

        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS
            )

            # Extract landmarks for classification
            landmarks = np.array([[lm.x, lm.y, lm.z] for lm in results.pose_landmarks.landmark]).flatten()
            prediction = self.model.predict([landmarks])
            predicted_pose = self.pose_labels[int(prediction[0])]

            self.pose_label.setText(f"Pose: {predicted_pose}")

        # Convert OpenCV frame to QImage
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_BGR888)
        self.video_label.setPixmap(QPixmap.fromImage(q_img))

    def closeEvent(self, event):
        self.cap.release()
        self.timer.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PoseDetectionApp()
    window.show()
    sys.exit(app.exec())
