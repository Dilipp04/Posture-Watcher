import sys
from ui.mainWindow import PostureWatcherUI
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QMovie
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget

class StartUpAnimationWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PostureWatcher - Start Up Animation")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # No window borders, stays on top
        self.setAttribute(Qt.WA_TranslucentBackground)

        screen_geometry = QApplication.primaryScreen().geometry()
        window_width, window_height = 800, 500
        x = (screen_geometry.width() - window_width) // 2
        y = (screen_geometry.height() - window_height) // 2
        self.setGeometry(x, y, window_width, window_height)

        self.setStyleSheet("background-color: #013e54;border-radius:10px")  # Replace with desired color or image

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)

        self.gif_label = QLabel(self)
        self.movie = QMovie("assets/animation_for_web.gif")  # Replace with the path to your GIF
        self.gif_label.setMovie(self.movie)

        layout.addWidget(self.gif_label)

        self.movie.start()

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.show_main_window)

        self.timer.start(2000)  # 3000 ms for 3 seconds, adjust as needed

    def show_main_window(self):
        self.main_window = PostureWatcherUI()
        self.main_window.show()
        self.close()  # Close the startup animation window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StartUpAnimationWindow()
    window.show()
    sys.exit(app.exec())
