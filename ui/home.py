from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout,QFrame,QApplication
)
import sys
from os import system
from PySide6.QtCore import QTimer, Qt, QTime
from PySide6.QtGui import QPixmap, QImage, QFont
from posture_detector.sidePostureAnalyzer import SidePostureAnalyzer
from posture_detector.frontPostureAnalyzer import FrontPostureAnalyzer

class Home(QFrame):
    def __init__(self):
        super().__init__()
        self.posture_analyzer = FrontPostureAnalyzer()
        # self.posture_analyzer = SidePostureAnalyzer()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)

        self.init_ui()

    def init_ui(self):

        # Title
        title = QLabel("Posture Analyzer")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setStyleSheet("margin:15px 10px; padding: 10px;")
        title.setAlignment(Qt.AlignLeft)

        # Video display
        self.video_label = QLabel(self)
        self.video_label.setFixedSize(720, 480)
        self.video_label.setStyleSheet("background-color: #f0f0f0; border: 1px solid #d6d6d6;")
        self.video_label.setAlignment(Qt.AlignCenter)

        # Clock display
        self.clock_label = QLabel(self)
        self.clock_label.setAlignment(Qt.AlignCenter)
        self.clock_label.setFont(QFont("Arial", 16))
        self.setStyleSheet("color:black")

        # Buttons
        self.start_button = QPushButton("Start", self)
        self.start_button.setFixedSize(120, 40)
        self.start_button.setStyleSheet("background-color: #003d4d; color: white;")
        self.start_button.clicked.connect(self.start_monitoring)

        self.set_base_button = QPushButton("Set base posture", self)
        self.set_base_button.setFixedSize(120, 40)
        self.set_base_button.setStyleSheet("background-color: #003d4d; color: white;")
        self.set_base_button.clicked.connect(self.set_base_posture)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setFixedSize(120, 40)
        self.stop_button.setStyleSheet("background-color: #003d4d; color: white;")
        self.stop_button.clicked.connect(self.stop_monitoring)

        # Layout setup
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(title)
        # Add video frame
        main_layout.addWidget(self.video_label, alignment=Qt.AlignCenter)

        # Add clock
        main_layout.addWidget(self.clock_label, alignment=Qt.AlignCenter)

        # Add buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.set_base_button)
        button_layout.addWidget(self.stop_button)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # Start clock timer
        self.clock_timer.start(1000)  # Update clock every second
        self.update_clock()

    def start_monitoring(self):
        try:
            self.posture_analyzer.run()
            self.timer.start(30)  # 30ms for ~33 FPS
        except Exception as e:
            self.video_label.setText(str(e))

    def stop_monitoring(self):
        self.timer.stop()
        self.posture_analyzer.stop()
        self.video_label.setText("Monitoring stopped.")

    def set_base_posture(self):
        # Logic to set the base posture
        self.posture_analyzer.set_base_posture()
        self.video_label.setText("Base posture set.")

    def update_frame(self):
        frame, posture_data = self.posture_analyzer.process_frame()
        
        if frame is not None:
            height, width, channel = frame.shape
            bytes_per_line = channel * width
            qimg = QImage(frame.data, width, height, bytes_per_line, QImage.Format_BGR888)
            self.video_label.setPixmap(QPixmap.fromImage(qimg))
        else:
            self.video_label.setText("No frame available.")

    def update_clock(self):
        current_time = QTime.currentTime().toString("hh:mm:ss")
        self.clock_label.setText(current_time)

def main():
    app = QApplication(sys.argv)
    mainWin = Home()
    mainWin.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
