import sys
import time
import cv2
import csv
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from posture_detector.posture import PostureWatcher  # Assuming PostureWatcher from previous code


class PostureWatcherUI(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the PostureWatcher
        self.posture_watcher = PostureWatcher()

        # Setup UI components
        self.init_ui()

        # Timer to fetch frames from the camera
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # Initialize JSON file for posture history
        self.history_file = "posture_history.csv"
        self.history = []
        self.last_save_time = 0  # Initialize the last save time


    def init_ui(self):
        # Video display label
        self.video_label = QLabel(self)
        self.video_label.setFixedSize(720, 480)

        # Start button
        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_posture_monitor)

        # Stop button
        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_posture_monitor)

        # Set base posture button
        self.set_base_button = QPushButton("Set Base Posture", self)
        self.set_base_button.clicked.connect(self.set_base_posture)

        # Status label to show posture deviation
        self.status_label = QLabel("Deviation: None", self)
        self.status_label.setAlignment(Qt.AlignCenter)

        # Good/Bad posture label
        self.posture_status_label = QLabel("Posture Status: Unknown", self)
        self.posture_status_label.setAlignment(Qt.AlignCenter)

        # Layouts
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.set_base_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.video_label)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.posture_status_label)

        self.setLayout(main_layout)
        self.setWindowTitle("Posture Watcher")
        self.resize(800, 600)

    def start_posture_monitor(self):
        # Start the posture watcher and the timer to update frames
        self.timer.start(30)  # Update frame every 30ms (around 33 FPS)
        self.status_label.setText("Monitoring started...")

    def stop_posture_monitor(self):
        # Stop the posture watcher and release the resources
        self.timer.stop()
        self.posture_watcher.stop()
        self.status_label.setText("Monitoring stopped.")

    def set_base_posture(self):
        # Capture base posture for comparison
        self.posture_watcher.set_base_posture()
        self.status_label.setText("Base posture set.")

    def update_frame(self):
        # Fetch the current frame from PostureWatcher and display it in the QLabel
        ret, img = self.posture_watcher.cap.read()
        if not ret:
            return  # Exit if there's an issue grabbing the frame
        
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB format

        # Run the PostureWatcher logic to analyze the posture
        self.posture_watcher.run()

        # Convert image to QImage and display it in QLabel
        height, width, channel = img_rgb.shape
        bytes_per_line = channel * width
        qimg = QImage(img_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qimg))

        # Display deviation in status label
        if self.posture_watcher.deviation.current_deviation is not None:
            deviation = self.posture_watcher.deviation.current_deviation
            self.status_label.setText(f"Deviation: {deviation}%")
            self._update_posture_status(deviation)


    def _update_posture_status(self, deviation):
        # Determine if the posture is good or bad
        if deviation < 25:
            self.posture_status_label.setText("Posture Status: Good ✅")
            posture_status = "Good"
        else:
            self.posture_status_label.setText("Posture Status: Bad ❌")
            posture_status = "Bad"

        # Store the posture data in history
        self._save_posture_history(deviation, posture_status)

    
    def _save_posture_history(self, deviation, status):
        current_time = time.time()  # Get the current time in seconds since the epoch
        if current_time - self.last_save_time >= 1:  # Check if 1 second has passed
            # Save the current deviation and status with a timestamp in the CSV history
            entry = [time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), deviation, status]
            self.history.append(entry)

            # Save to CSV file
            with open(self.history_file, 'a', newline='') as f:
                writer = csv.writer(f)
                if f.tell() == 0:  # Check if file is empty to write headers
                    writer.writerow(['Timestamp', 'Deviation', 'Status'])
                writer.writerow(entry)

            self.last_save_time = current_time  # Update the last save time


def main():
    app = QApplication(sys.argv)
    mainWin = PostureWatcherUI()
    mainWin.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
