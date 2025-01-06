from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QCheckBox,
    QHBoxLayout, QPushButton, QButtonGroup
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class SettingsUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setGeometry(200, 200, 600, 400)

        # Main Widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Main Layout
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(20)

        # Settings Title
        title = QLabel("Settings")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        main_layout.addWidget(title, alignment=Qt.AlignLeft)

        # Camera Dropdown Section
        self.add_section(
            main_layout,
            "Camera",
            "Choose your preferred webcam from the list",
            self.create_camera_dropdown()
        )

        # Camera Angle Section
        self.add_section(
            main_layout,
            "Camera Angle",
            "",
            self.create_toggle_buttons(["Front", "Side"])
        )

        # Position Section
        self.add_section(
            main_layout,
            "Position",
            "",
            self.create_toggle_buttons(["left", "middle", "right"])
        )

        # Play Sound Section
        self.add_section(
            main_layout,
            "Play Sound",
            "",
            self.create_toggle_switch()
        )

        # Delay Section
        self.add_section(
            main_layout,
            "Delay",
            "",
            self.create_toggle_buttons(["3s", "10s", "15s"])
        )

    def add_section(self, layout, title, description, widget):
        """Add a labeled section with optional description and widget."""
        section_layout = QHBoxLayout()
        label = QLabel(title)
        label.setFont(QFont("Arial", 14))
        section_layout.addWidget(label)

        if description:
            desc_label = QLabel(description)
            desc_label.setFont(QFont("Arial", 10))
            desc_label.setStyleSheet("color: gray;")
            section_layout.addWidget(desc_label)

        section_layout.addWidget(widget)
        layout.addLayout(section_layout)

    def create_camera_dropdown(self):
        """Create a dropdown menu for camera selection."""
        dropdown = QComboBox()
        dropdown.addItems(["Webcam", "External Camera", "Virtual Camera"])
        dropdown.setStyleSheet("""
            QComboBox {
                font-size: 14px;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
        """)
        return dropdown

    def create_toggle_buttons(self, options):
        """Create a row of toggle buttons."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setSpacing(10)

        button_group = QButtonGroup(container)
        for option in options:
            button = QPushButton(option)
            button.setCheckable(True)
            button.setStyleSheet("""
                QPushButton {
                    font-size: 14px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    padding: 5px 15px;
                    background-color: white;
                }
                QPushButton:checked {
                    background-color: #008CBA;
                    color: white;
                    border: none;
                }
            """)
            layout.addWidget(button)
            button_group.addButton(button)

        return container

    def create_toggle_switch(self):
        """Create a toggle switch styled checkbox."""
        toggle = QCheckBox()
        toggle.setStyleSheet("""
            QCheckBox::indicator {
                width: 40px;
                height: 20px;
                background-color: #ccc;
                border-radius: 10px;
            }
            QCheckBox::indicator:checked {
                background-color: #008CBA;
            }
        """)
        return toggle


if __name__ == "__main__":
    app = QApplication([])
    window = SettingsUI()
    window.show()
    app.exec()
