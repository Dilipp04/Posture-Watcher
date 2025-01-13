from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QHBoxLayout, QApplication
)
import sys
from PySide6.QtCore import Qt, QSize, QPoint, QTimer
from PySide6.QtGui import QFont, QIcon, QPixmap

class MiniWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.is_dragging = False  # Flag to check if dragging is in progress
        self.drag_position = QPoint(0, 0)  # To store the mouse position during dragging
        self.is_paused = False  # Flag to track if the button is in paused state
        self.timer_running = False  # Flag to track the state of the timer
        self.timer_seconds = 0  # Track time in seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        # Set the start_pause_button to checked state by default
        self.start_pause_button.setChecked(True)  # The button starts as checked
        self.toggle_icon(True)  # Update the icon immediately to reflect the checked state
        self.start_timer()  # Start the timer immediately when the app starts

    def init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(200, 40)
        self.setStyleSheet("background-color:#013e54 ; border-radius: 10px ")

        # Timer label
        self.timer_label = QLabel("00:00", self)
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setFont(QFont("Arial", 16))
        self.timer_label.setStyleSheet("color: white; border: none")
        
        # Icon for the timer
        self.logo = QLabel(self)
        self.logo.setPixmap(QPixmap("assets/logo-transparent1.png").scaled(60, 45, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Update with the correct image path

        # Buttons
        self.maximize_button = QPushButton(self)
        self.maximize_button.setFixedSize(28, 28)
        self.maximize_button.setIcon(QIcon("assets/maximize_button.svg"))  # Replace with the path to your maximize icon
        self.maximize_button.setIconSize(QSize(25, 25))  # Adjust icon size to fit
        self.maximize_button.setStyleSheet("border: none;")

        self.start_pause_button = QPushButton(self)
        self.start_pause_button.setIcon(QIcon("assets/pause_icon.svg"))  # Default icon is pause
        self.start_pause_button.setIconSize(QSize(25, 25))  # Adjust icon size to fit
        self.start_pause_button.setFixedSize(28, 28)
        self.start_pause_button.setStyleSheet("border: none;")
        self.start_pause_button.setCheckable(True)  # Make the button toggleable
        self.start_pause_button.toggled.connect(self.toggle_icon)  # Connect toggle event

        # Layout
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.addWidget(self.maximize_button)
        layout.addWidget(self.logo)  # Add the icon before the timer
        layout.addWidget(self.timer_label)
        layout.addWidget(self.start_pause_button)
        self.setLayout(layout)

    def toggle_icon(self, checked):
        # Change the icon based on whether the button is checked or not
        if checked:
            self.start_pause_button.setIcon(QIcon("assets/pause_icon.svg"))  # Show pause icon when checked
            self.start_timer()  # Start the timer when the button is checked
        else:
            self.start_pause_button.setIcon(QIcon("assets/play_icon.svg"))  # Show play icon when unchecked
            self.pause_timer()  # Pause the timer when the button is unchecked

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.timer.start(1000)  # Update every second

    def pause_timer(self):
        if self.timer_running:
            self.timer.stop()
            self.timer_running = False

    def update_timer(self):
        self.timer_seconds += 1
        minutes = self.timer_seconds // 60
        seconds = self.timer_seconds % 60
        self.timer_label.setText(f"{minutes:02}:{seconds:02}")

    def mousePressEvent(self, event):
        # Record the position where the mouse was clicked
        if event.button() == Qt.LeftButton:
            self.is_dragging = True
            self.drag_position = event.globalPosition().toPoint()  # Global position for dragging

    def mouseMoveEvent(self, event):
        # Move the window if dragging is in progress
        if self.is_dragging:
            delta = event.globalPosition().toPoint() - self.drag_position
            self.move(self.pos() + delta)
            self.drag_position = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        # Stop dragging when the mouse button is released
        if event.button() == Qt.LeftButton:
            self.is_dragging = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mini_window = MiniWindow()
    mini_window.show()
    sys.exit(app.exec())

