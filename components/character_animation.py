from PySide6.QtWidgets import QApplication, QFrame, QVBoxLayout, QPushButton, QWidget
from PySide6.QtCore import QPropertyAnimation, QRect, Qt, QTimer
from PySide6.QtGui import QPainter, QPixmap

class AnimatedImageWidget(QWidget):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.resize(200, 200)

        # Animation-related attributes
        self.animation = QPropertyAnimation(self, b"geometry")

    def configure_positions(self, screen_geometry,position):
        """Configure the start and end positions for animation."""
        if position == "Left":
            self.start_x =  0 #Left
        elif position =="Right":
            self.start_x = (screen_geometry.width() - self.width()) #right
        else:
            self.start_x = (screen_geometry.width() - self.width()) //2 #Center

        self.start_y = screen_geometry.height()
        self.end_y = screen_geometry.height() - 250

        self.start_geometry = QRect(self.start_x, self.start_y, 200, 200)
        self.end_geometry = QRect(self.start_x, self.end_y, 200, 200)

        # Initialize the widget's position
        self.setGeometry(self.start_geometry)

    def toggle_animation(self, move_up):
        """Animate the widget based on the posture state."""
        target_geometry = self.end_geometry if move_up else self.start_geometry
        self.animation.setDuration(1000)  # 1 second
        self.animation.setStartValue(self.geometry())
        self.animation.setEndValue(target_geometry)
        self.animation.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pixmap = QPixmap(self.image_path).scaled(
            self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        target_rect = self.rect()
        painter.drawPixmap(target_rect, pixmap)
