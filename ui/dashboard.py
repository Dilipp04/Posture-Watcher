from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QFrame, QHBoxLayout , QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import sys
class Dashboard(QFrame):
    def __init__(self):
        super().__init__()

        # Main layout
        layout = QVBoxLayout(self)
        self.setStyleSheet("background-color: white; border-radius: 10px; padding: 20px;")

        label = QLabel("Dashboard Page")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 60px; color: #013e54;")
        layout.addWidget(label)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec())
