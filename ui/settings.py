from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QCheckBox,
    QHBoxLayout, QPushButton, QButtonGroup, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from components.ToggleSwitch import ToggleSwitch

class Settings(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color:white;color:black;padding:10px")
        main_layout = QVBoxLayout(self)

        # Settings Title
        title = QLabel("Settings")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setStyleSheet("margin:10px 10px; padding: 10px;")
        main_layout.addWidget(title, alignment=Qt.AlignLeft)

        # Create QListWidget
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("QListWidget { border: none; }")
        self.list_widget.setSpacing(15)  
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
        # Create the main container widget
        container = QWidget()
        container.setStyleSheet("background-color: white; padding: 20px 0px;")

        # Create a horizontal layout for the section
        layout = QHBoxLayout(container)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create a vertical layout for the title and description
        text_layout = QVBoxLayout()
        text_layout.setSpacing(5)  # Spacing between title and description
        text_layout.setContentsMargins(0, 0, 0, 0)

        # Add title
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 14))
        text_layout.addWidget(title_label)

        # Add description (if provided)
        if description:
            desc_label = QLabel(description)
            desc_label.setFont(QFont("Arial", 10))
            desc_label.setStyleSheet("color: gray;")
            desc_label.setWordWrap(True)  # Enable word wrapping
            text_layout.addWidget(desc_label)

        # Add layouts to the horizontal layout
        layout.addLayout(text_layout)  # Add text layout on the left
        layout.addWidget(widget, alignment=Qt.AlignRight)  # Add the widget on the right

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
        dropdown.setFixedSize(230, 30)
        return dropdown

    def create_toggle_buttons(self, options):
        """Create a row of toggle buttons."""
        container = QWidget()
        container.setFixedSize(230, 40)
        container.setStyleSheet("""
            QWidget {
                border: none;
                background-color: #023D53;
                border-radius: 10px;
            }
        """)
        layout = QHBoxLayout(container)
        layout.setSpacing(10)
        layout.setContentsMargins(5, 5, 5, 5)

        button_group = QButtonGroup(container)
        for option in options:
            button = QPushButton(option)
            button.setCheckable(True)
            button.setStyleSheet("""
                QPushButton {
                    font-size: 14px;
                    font-weight: bold;
                    border: none;
                    border-radius: 5px;
                    padding: 5px 15px;
                    background-color: #023D53;
                    color: white;
                }
                QPushButton:checked {
                    background-color: white;
                    color: #023D53;
                    border: none;
                }
            """)
            layout.addWidget(button)
            button_group.addButton(button)

        # Set the first button as checked by default
        if button_group.buttons():
            button_group.buttons()[0].setChecked(True)

        return container

    def create_toggle_switch(self):
        """Create a toggle switch with a rounded button."""
        button_container = QWidget()
        button_container.setFixedSize(230, 40)
        button_container.setStyleSheet(" border-radius: 10px; padding: 5px;")
        button_layout = QHBoxLayout(button_container)
        button_layout.setSpacing(5)
        button_layout.setContentsMargins(0, 0, 0, 0)

        toggle_button = ToggleSwitch(self, width=55, height=30, on_color="#013e54", off_color="lightgray")
        toggle_button.toggled.connect(lambda checked: print("Toggle 1:", "On" if checked else "Off"))
        button_layout.addWidget(toggle_button)

        return button_container

def main():
    app = QApplication([])
    window = Settings()
    window.showMaximized()
    app.exec()


if __name__ == "__main__":
    main()