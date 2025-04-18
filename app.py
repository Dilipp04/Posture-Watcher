from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QProgressBar, QPushButton
from PySide6.QtCore import QTimer, QPropertyAnimation, Qt, Slot
import random

class YogaProgress(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yoga Pose Accuracy")
        self.setGeometry(300, 300, 300, 150)

        self.layout = QVBoxLayout(self)

        # Progress Bar
        self.progress = QProgressBar()
        self.progress.setAlignment(Qt.AlignCenter)
        self.progress.setFormat("Posture Accuracy: %p%")
        self.progress.setValue(0)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #ccc;
                border-radius: 10px;
                text-align: center;
                height: 30px;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 10px;
            }
        """)
        self.layout.addWidget(self.progress)

        # Test Button (simulate new accuracy values)
        self.test_button = QPushButton("Simulate Accuracy Update")
        self.test_button.clicked.connect(self.simulate_accuracy)
        self.layout.addWidget(self.test_button)

        # Animation setup
        self.anim = QPropertyAnimation(self.progress, b"value")
        self.anim.setDuration(400)

    @Slot()
    def simulate_accuracy(self):
        new_accuracy = random.randint(40, 100)
        self.update_progress_bar(new_accuracy)

    def update_progress_bar(self, value):
        self.anim.stop()
        self.anim.setStartValue(self.progress.value())
        self.anim.setEndValue(value)
        self.anim.start()

if __name__ == "__main__":
    app = QApplication([])
    window = YogaProgress()
    window.show()
    app.exec()
