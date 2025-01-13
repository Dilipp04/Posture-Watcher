from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout,QFrame,QApplication,QGraphicsDropShadowEffect
)
import sys
from os import system
from PySide6.QtCore import QTimer, Qt, QTime,Signal
from PySide6.QtGui import QPixmap, QImage, QFont
from posture_detector.sidePostureAnalyzer import SidePostureAnalyzer
from posture_detector.frontPostureAnalyzer import FrontPostureAnalyzer
from states.state import State

class Home(QFrame):
    def __init__(self,state: State):
        super().__init__()

        self.state = state
        self.state.camera_angle_changed.connect(self.handle_state_change)
        self.init_posture_analyzer()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.elapsed_time_timer = QTimer()
        self.elapsed_time_timer.timeout.connect(self.update_elapsed_time)
        self.elapsed_time = 0  # Initialize elapsed time
        

        self.init_ui()


    def init_posture_analyzer(self):
        camera_angle = self.state.get_setting("camera_angle")
        if camera_angle == "Front":
            self.posture_analyzer = FrontPostureAnalyzer()
        elif camera_angle == "Side":
            self.posture_analyzer = SidePostureAnalyzer()

    def init_ui(self):

        # Title
        title = QLabel("Posture Analyzer")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setStyleSheet("margin:15px 10px; padding: 10px;")
        title.setAlignment(Qt.AlignLeft)

        # Video display
        self.video_label = QLabel(self)
        self.video_label.setFixedSize(720, 480)
        self.video_label.setStyleSheet(f"background-color: #f0f0f0; border: 5px solid black;")
        self.video_label.setAlignment(Qt.AlignCenter)

        # Timer label to display elapsed time
        self.timer_label = QLabel("00:00", self)
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setFont(QFont("Arial", 16))
        self.timer_label.setStyleSheet("color:black")

        self.status_label = QLabel(self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Arial", 16))
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
        main_layout.addWidget(self.timer_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.status_label, alignment=Qt.AlignCenter)

        # Add buttons
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.set_base_button)
        button_layout.addWidget(self.stop_button)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        
    def handle_state_change(self):
        """Handle changes in the state dynamically."""
        try:
            # Reinitialize the posture analyzer if the state has changed
            self.init_posture_analyzer()
            self.update_ui()
            self.video_label.setText("Restart monitoring.")
        except Exception as e:
            self.video_label.setText(f"Error: {e}")

    def update_ui(self):
        if self.state.get_setting("camera_angle")=="Side":
            self.set_base_button.setHidden(True)
        else:
            self.set_base_button.setHidden(False)

    def start_monitoring(self):
        try:
            self.video_label.setText("Loading")
            self.elapsed_time_timer.start(1000)
            self.posture_analyzer.run(self.state.get_setting("camera"))
            self.timer.start(30)  # 30ms for ~33 FPS
        except Exception as e:
            self.video_label.setText(str(e))

    def stop_monitoring(self):
        self.timer.stop()
        self.elapsed_time_timer.stop() 
        self.posture_analyzer.stop()
        self.video_label.setText("Monitoring stopped.")

    def set_base_posture(self):
        # Logic to set the base posture
        self.posture_analyzer.set_base_posture()
        self.video_label.setText("Base posture set.")

    def update_frame(self):
        frame, posture_data = self.posture_analyzer.process_frame()

        if posture_data["status"] =="Good":
            self.status_label.setText("Posture Status: Good ✅")
            self.video_label.setStyleSheet("border: 5px solid Green;")
        else:
            self.status_label.setText("Posture Status: Bad ❌")
            self.video_label.setStyleSheet("border: 5px solid red;")

        if frame is not None:
            height, width, channel = frame.shape
            bytes_per_line = channel * width
            qimg = QImage(frame.data, width, height, bytes_per_line, QImage.Format_BGR888)
            self.video_label.setPixmap(QPixmap.fromImage(qimg))
        else:
            self.video_label.setText("No frame available.")

    def update_elapsed_time(self):
        # Update the elapsed time and display it in the timer label
        self.elapsed_time += 1
        minutes, seconds = divmod(self.elapsed_time, 60)
        self.timer_label.setText(f"{minutes:02}:{seconds:02}")

def main():
    app = QApplication(sys.argv)
    mainWin = Home()
    mainWin.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
