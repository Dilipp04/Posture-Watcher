from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog
from PySide6.QtCore import QPropertyAnimation, QRect, Qt
from PySide6.QtGui import QPainter, QPixmap
from components.alertGiraffe import AnimatedImageDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Posture Monitoring")
        self.resize(400, 300)

        self.button = QPushButton("Simulate Posture State", self)
        self.button.clicked.connect(self.toggle_posture_state)
        self.setCentralWidget(self.button)

        self.bad_posture = False  # Simulated posture state

        # Create and configure the reusable component
        self.image_dialog = AnimatedImageDialog("assets/memoji.png", self)
        screen_geometry = QApplication.primaryScreen().geometry()
        self.image_dialog.configure_positions(screen_geometry)
        self.image_dialog.show()

    def toggle_posture_state(self):
        self.bad_posture = not self.bad_posture
        self.image_dialog.toggle_animation(self.bad_posture)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()

    app.exec()
