from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QCheckBox,
    QHBoxLayout, QPushButton, QButtonGroup, QFrame, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class Settings(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color:white;color:black;padding:10px")
        main_layout = QVBoxLayout(self)

        # Settings Title
        title = QLabel("Settings")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        main_layout.addWidget(title, alignment=Qt.AlignLeft)

        # Create QListWidget
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("QListWidget { border: none; margin:10px}")
        main_layout.addWidget(self.list_widget)

        # Add sections to the QListWidget
        self.add_section(
            "Camera",
            "Choose your preferred webcam from the list",
            self.create_camera_dropdown()
        )
        self.add_section(
            "Camera Angle",
            "",
            self.create_toggle_buttons(["Front", "Side"])
        )
        self.add_section(
            "Position",
            "",
            self.create_toggle_buttons(["Left", "Middle", "Right"])
        )
        self.add_section(
            "Play Sound",
            "",
            self.create_toggle_switch()
        )
        self.add_section(
            "Delay",
            "",
            self.create_toggle_buttons(["3s", "10s", "15s"])
        )

    def add_section(self, title, description, widget):
        """Add a section as a QListWidgetItem with a custom widget."""
        container = QWidget()
        container.setStyleSheet("background-color: white; padding: 10px;height: 60px;")
        layout = QHBoxLayout(container)

        # Add title
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 14))
        layout.addWidget(title_label)

        # Add description
        if description:
            desc_label = QLabel(description)
            desc_label.setFont(QFont("Arial", 10))
            desc_label.setStyleSheet("color: gray;")
            layout.addWidget(desc_label)

        # Add custom widget
        layout.addWidget(widget)

        # Create QListWidgetItem
        item = QListWidgetItem()
        item.setSizeHint(container.sizeHint())  # Match the size of the widget
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, container)

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
                    background-color: #013e54;
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




def main():
    app = QApplication([])
    window = Settings()
    window.showMaximized()
    app.exec()

if __name__ == "__main__":
    main()