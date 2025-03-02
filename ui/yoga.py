from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QCheckBox,
    QHBoxLayout, QPushButton, QButtonGroup, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from components.ToggleSwitch import ToggleSwitch
from utilities.state import State

class Yoga(QWidget):
    def __init__(self,state:State):
        super().__init__()

        self.state = state
        self.setStyleSheet("background-color:white;color:black;padding:10px")
        main_layout = QVBoxLayout(self)

        # Settings Title
        title = QLabel("Yoga")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setStyleSheet("margin:10px 10px; padding: 10px;")
        main_layout.addWidget(title, alignment=Qt.AlignLeft)


def main():
    app = QApplication([])
    window = Yoga()
    window.showMaximized()
    app.exec()


if __name__ == "__main__":
    main()
