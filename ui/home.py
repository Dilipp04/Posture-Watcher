import cv2
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,QFrame
from posture_detector import PostureWatcher  # Assuming PostureWatcher from previous code

class Home(QFrame):
    def __init__(self):
        super().__init__()

        # Initialize the PostureWatcher
        self.posture_watcher = PostureWatcher()

        # Timer for updating frames and counting elapsed time
        self.frame_timer = QTimer()
        self.frame_timer.timeout.connect(self.update_frame)

        self.elapsed_time_timer = QTimer()
        self.elapsed_time_timer.timeout.connect(self.update_elapsed_time)
        self.elapsed_time = 0  # Initialize elapsed time

        # Initialize CSV file for posture history
        self.history_file = "posture_history.csv"
        self.history = []
        self.last_save_time = 0  # Initialize the last save time

        # Setup UI components
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: white;")  # Set background color
        # Camera view tab layout
        layout = QVBoxLayout(self)

        # Video display label
        self.video_label = QLabel(self)
        self.video_label.setFixedSize(720, 480)

        # Timer label to display elapsed time
        self.timer_label = QLabel("Elapsed Time: 00:00", self)
        self.timer_label.setAlignment(Qt.AlignCenter)

        # Start and stop buttons
        self.start_button = QPushButton("Start", self)
        # Example button style code
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #013E54;  /* Gold color */
                border: none;                /* No border */
                border-radius: 8px;         /* Rounded corners */
                padding: 10px 20px;         /* Padding for better size */
                font-size: 16px;            /* Larger font */
                font-weight: bold;          /* Bold text */
                color: white;               /* White text color */
            }
        """)

        self.start_button.clicked.connect(self.start_posture_monitor)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #013E54;  /* Gold color */
                border: none;                /* No border */
                border-radius: 8px;         /* Rounded corners */
                padding: 10px 20px;         /* Padding for better size */
                font-size: 16px;            /* Larger font */
                font-weight: bold;          /* Bold text */
                color: white;               /* White text color */
            }
        """)
        self.stop_button.clicked.connect(self.stop_posture_monitor)

        # Set base posture button
        self.set_base_button = QPushButton("Set Base Posture", self)
        self.set_base_button.setStyleSheet("""
            QPushButton {
                background-color: #013E54;  /* Gold color */
                border: none;                /* No border */
                border-radius: 8px;         /* Rounded corners */
                padding: 10px 20px;         /* Padding for better size */
                font-size: 16px;            /* Larger font */
                font-weight: bold;          /* Bold text */
                color: white;               /* White text color */
            }
        """)
        self.set_base_button.clicked.connect(self.set_base_posture)

        # Status label to show posture deviation
        self.status_label = QLabel("Deviation: None", self)
        self.status_label.setAlignment(Qt.AlignCenter)

        # Good/Bad posture label
        self.posture_status_label = QLabel("Posture Status: Unknown", self)
        self.posture_status_label.setAlignment(Qt.AlignCenter)

        # Layout for camera view tab
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.set_base_button)

        layout.addWidget(self.video_label)
        layout.addWidget(self.timer_label)
        layout.addLayout(button_layout)
        layout.addWidget(self.status_label)
        layout.addWidget(self.posture_status_label)

        self.setLayout(layout)

    def start_posture_monitor(self):
        # Start the posture watcher and the timer to update frames
        self.frame_timer.start(30)  # Update frame every 30ms (around 33 FPS)
        self.elapsed_time_timer.start(1000)  # Update elapsed time every second
        self.status_label.setText("Monitoring started...")

    def stop_posture_monitor(self):
        # Stop the posture watcher and release the resources
        self.frame_timer.stop()
        self.elapsed_time_timer.stop()  # Stop the elapsed time timer
        self.status_label.setText("Monitoring stopped.")

    def set_base_posture(self):
        # Capture base posture for comparison
        self.posture_watcher.set_base_posture()
        self.status_label.setText("Base posture set")

    def update_elapsed_time(self):
        # Update the elapsed time and display it in the timer label
        self.elapsed_time += 1
        minutes, seconds = divmod(self.elapsed_time, 60)
        self.timer_label.setText(f"Elapsed Time: {minutes:02}:{seconds:02}")

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
        if deviation < 35:
            self.posture_status_label.setText("Posture Status: Good ✅")
            posture_status = "Good"
        else:
            self.posture_status_label.setText("Posture Status: Bad ❌")
            posture_status = "Bad"
