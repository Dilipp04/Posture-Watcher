import sys
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QMovie
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget

class StartUpAnimationWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window setup for the startup animation (no borders)
        self.setWindowTitle("PostureWatcher - Start Up Animation")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # No window borders, stays on top

        # Get screen geometry and center the window
        screen_geometry = QApplication.primaryScreen().geometry()
        window_width, window_height = 800, 500
        x = (screen_geometry.width() - window_width) // 2
        y = (screen_geometry.height() - window_height) // 2
        self.setGeometry(x, y, window_width, window_height)

        # Apply a stylesheet for the background
        self.setStyleSheet("background-color: #013e54;")  # Replace with desired color or image

        # Central widget to hold layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Layout to center the GIF
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)

        # QLabel to display GIF animation
        self.gif_label = QLabel(self)
        self.movie = QMovie("assets/animation_for_web.gif")  # Replace with the path to your GIF
        self.gif_label.setMovie(self.movie)

        # Add the QLabel to the layout
        layout.addWidget(self.gif_label)

        # Start playing the GIF
        self.movie.start()

        # Set up a timer to transition to the main window after the GIF finishes
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.show_main_window)

        # Start timer (adjust time to match GIF duration, in ms)
        self.timer.start(5000)  # 3000 ms for 3 seconds, adjust as needed

    def show_main_window(self):
        # Transition to the main window once the GIF finishes
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()  # Close the startup animation window

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main PostureWatcher Application")
        self.setGeometry(100, 100, 800, 600)

        # Main window content
        self.label = QLabel("Welcome to PostureWatcher!", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.showMaximized()
        self.setCentralWidget(self.label)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StartUpAnimationWindow()
    window.show()
    sys.exit(app.exec())
