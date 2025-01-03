from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog
from PySide6.QtCore import QPropertyAnimation, QRect, Qt
from PySide6.QtGui import QPainter, QPixmap

class ImageDialog(QDialog):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.resize(200, 200)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pixmap = QPixmap(self.image_path).scaled(
            self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        target_rect = self.rect()
        painter.drawPixmap(target_rect, pixmap)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Posture Monitoring")
        self.resize(400, 300)

        self.button = QPushButton("Simulate Posture State", self)
        self.button.clicked.connect(self.toggle_posture_state)
        self.setCentralWidget(self.button)

        self.bad_posture = False  # Simulated posture state
        self.image_dialog = None
        self.init_image_dialog()

    def init_image_dialog(self):
        image_path = "memoji.webp"  # Replace with your image file path
        self.image_dialog = ImageDialog(image_path)

        # Start position (off-screen at the bottom)
        screen_geometry = QApplication.primaryScreen().geometry()
        self.start_x = (screen_geometry.width() - self.image_dialog.width()) // 2
        self.start_y = screen_geometry.height()
        self.end_y = screen_geometry.height() - 300

        self.image_dialog.setGeometry(self.start_x, self.start_y, 200, 200)
        self.image_dialog.show()

    def toggle_posture_state(self):
        self.bad_posture = not self.bad_posture
        self.animate_posture_response(self.bad_posture)

    def animate_posture_response(self, is_bad_posture):
        if is_bad_posture:
            # Animate upward when posture is bad
            target_geometry = QRect(self.start_x, self.end_y, 200, 200)
        else:
            # Animate back to the bottom when posture is good
            target_geometry = QRect(self.start_x, self.start_y, 200, 200)

        self.animation = QPropertyAnimation(self.image_dialog, b"geometry")
        self.animation.setDuration(1000)  # 1 second
        self.animation.setStartValue(self.image_dialog.geometry())
        self.animation.setEndValue(target_geometry)
        self.animation.start()

if __name__ == "__main__":
    app = QApplication([])

    # Simulated main window
    window = MainWindow()
    window.show()

    app.exec()
