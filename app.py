import sys
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QMovie
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel

class StartUpAnimationWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window setup for the startup animation (no borders)
        self.setWindowTitle("PostureWatcher - Start Up Animation")
        self.setWindowFlags(Qt.FramelessWindowHint)  # No window borders
        self.setGeometry(0, 0, 800, 600)  # Fullscreen or set preferred size

        # Setup QLabel to display GIF animation
        self.gif_label = QLabel(self)
        self.gif_label.setGeometry(0, 0, 800, 600)  # Set the size of the label for your GIF
        self.movie = QMovie("assets/animation_for_web.gif")  # Replace with the path to your GIF
        self.gif_label.setMovie(self.movie)
        
        # Start playing the GIF
        self.movie.start()

        # Set up a timer to transition to the main window after the GIF finishes
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.show_main_window)

        # Start timer (adjust time to match GIF duration, in ms)
        self.timer.start(3000)  # 5000 ms for 5 seconds, adjust as needed

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
        self.setCentralWidget(self.label)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StartUpAnimationWindow()
    window.show()
    sys.exit(app.exec())
